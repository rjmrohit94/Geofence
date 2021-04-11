from app import mongo as db
from app.common.model import not_null


class GeoCoordinate(db.EmbeddedDocument):
    latitude = db.StringField(required=True, validation=not_null)
    longitude = db.StringField(required=True, validation=not_null)


class WrapperRect(db.EmbeddedDocument):
    maxX = db.StringField(required=True, validation=not_null)
    minX = db.StringField(required=True, validation=not_null)
    maxY = db.StringField(required=True, validation=not_null)
    minY = db.StringField(required=True, validation=not_null)


class Geofence(db.Document):
    uu_id = db.StringField(required=True, primary_key=True)
    coordinates = db.ListField(db.EmbeddedDocumentField('GeoCoordinate'))
    wrapperRect = db.EmbeddedDocumentField('WrapperRect')
    status = db.BooleanField(default=False)
    testData = db.FileField()
    trainingData = db.FileField()
    geoFenceData = db.FileField()  # cord.txt
    trainedModel = db.FileField()  # geofence_predictor

    meta = {'strict': False}


