from app import mongo as db
from app.common.model import not_null


class GeoCoordinate(db.EmbeddedDocument):
    latitude = db.StringField(required=True, validation=not_null)
    longitude = db.StringField(required=True, validation=not_null)


class Geofence(db.Document):
    uu_id = db.StringField(required=True, primary_key=True)
    coordinates = db.ListField(db.EmbeddedDocumentField('GeoCoordinate'))
    status = db.BooleanField(default=False)

    meta = {'strict': False}
