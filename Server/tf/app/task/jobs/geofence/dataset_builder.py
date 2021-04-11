import traceback

from mongoengine import DoesNotExist

from app.geofence.models import Geofence, WrapperRect
from app.task.jobs.geofence.utils import get_fencing_polygon, random_point_within


def retrieve_and_clear_model(geofence_id):
    try:
        geofence = Geofence.objects.get(uu_id=geofence_id)
        geofence.isModelInstalled = False
        if geofence.testData:
            geofence.testData.delete()
        if geofence.trainingData:
            geofence.trainingData.delete()
        if geofence.geoFenceData:
            geofence.geoFenceData.delete()
        if geofence.trainedModel:
            geofence.trainedModel.delete()
        if geofence.testData or geofence.trainedModel or geofence.geoFenceData or geofence.trainingData:
            geofence.save()
        return geofence
    except DoesNotExist:
        print("Unable to find geofence with given id")
        return None


def execute(job_data):
    try:
        geofence_id = job_data.get('geofenceId')
        geofence = retrieve_and_clear_model(geofence_id)
        if geofence and geofence.coordinates:
            print("preparing testData ...")
            geofence.testData.new_file(encoding='utf-8', content_type='text/csv', file_name='testData.csv')
            prepare_and_write_data(geofence, geofence.testData)
            geofence.testData.close()
            print("preparing trainingData ...")
            geofence.trainingData.new_file(encoding='utf-8', content_type='text/csv', file_name='training.csv')
            prepare_and_write_data(geofence, geofence.trainingData)
            geofence.trainingData.close()
            geofence.save()
    except Exception as _e:
        print(_e.args)
        print(traceback.print_stack())


def prepare_and_write_data(geofence, file):
    polygon = get_fencing_polygon(geofence.coordinates)
    min_x, min_y, max_x, max_y = polygon.bounds
    wrapper_rect = WrapperRect(maxX=str(max_x), minX=str(min_x), maxY=str(max_y), minY=str(min_y))
    geofence.wrapperRect = wrapper_rect
    points = (random_point_within(polygon) for _ in range(20000))
    file.write('{}\n'.format("{} {} {}".format("Lat", "Long", "Out")))
    for point in points:
        check = int(point.within(polygon))
        point_x = float(point.x - min_x) / (max_x - min_x)
        point_y = float(point.y - min_y) / (max_y - min_y)
        file.write('{}\n'.format("{} {} {}".format(point_x, point_y, check)))
