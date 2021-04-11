import io
import gridfs
from bson import ObjectId
from app import mongo as mongo_db


def get_file(dataset_doc_id):
    _fs = gridfs.GridFS(mongo_db.Document._get_db())
    dataset_fd = _fs.get(ObjectId(dataset_doc_id))
    content = io.BytesIO(dataset_fd.read())
    return content
