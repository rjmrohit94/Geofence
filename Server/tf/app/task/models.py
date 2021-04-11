import redis
import rq
from app import mongo as db
from app import app
from app.common.model import not_null
from app.common.error import ValidationError


GEOFENCE_TRAINING_JOB = 'GEOFENCE_TRAINING_JOB'
GEOFENCE_DATASET_BUILDER_JOB = 'GEOFENCE_DATASET_BUILDER_JOB'
GEOFENCE = 'GEOFENCE'

JOB_TYPES = (GEOFENCE_TRAINING_JOB, GEOFENCE_DATASET_BUILDER_JOB)

JOB_MAPS = {
    GEOFENCE_TRAINING_JOB: 'geofence.training.execute',
    GEOFENCE_DATASET_BUILDER_JOB: 'geofence.dataset_builder.execute',
}


READY_TO_START = 'READY_TO_START'
IN_PROGRESS = 'IN_PROGRESS'
COMPLETED_SUCCESSFULLY = 'COMPLETED'
FAILED = 'FAILED'
PARTIAL_SUCCESS = 'PARTIAL_SUCCESS'

JOB_STATUS = (READY_TO_START, IN_PROGRESS, COMPLETED_SUCCESSFULLY, FAILED, PARTIAL_SUCCESS)


class Task(db.Document):
    job_id = db.StringField(required=True, validation=not_null, primary_key=True)
    name = db.StringField(required=True, validation=not_null)
    type = db.StringField(choices=JOB_TYPES)
    description = db.StringField()
    progress = db.IntField(default=0)
    totalItemsSubmitted = db.IntField(default=0)
    completedItems = db.IntField(default=0)
    failedItems = db.IntField(default=0)
    failedItemData = db.ListField(db.DictField())
    complete = db.BooleanField(default=False)
    status = db.StringField(choices=JOB_STATUS, default=READY_TO_START)

    meta = {'strict': False}

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.job_id, connection=app.redis)
        except (redis.exceptions.RedisError,):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100

    @staticmethod
    def launch_task(name, description, job_type, *args, **kwargs):
        if job_type not in JOB_TYPES:
            raise ValidationError('Unsupported Job type')
        rq_job = app.task_queue.enqueue('app.task.jobs.' + JOB_MAPS.get(job_type), *args, **kwargs)
        task = Task(job_id=rq_job.get_id(), name=name, description=description)
        task.save()
        return task.job_id


