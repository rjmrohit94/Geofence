from app.index import define_v1_routes
from app.geofence.views import GeoFenceApi, GeoFencesApi, GeoFenceCollectionApi


def initialize_routes(api, app):
    api.add_resource(GeoFencesApi, '/api/v1/geofence')
    api.add_resource(GeoFenceCollectionApi, '/api/v1/geofence-collection')
    api.add_resource(GeoFenceApi, '/api/v1/geofence/<fence_id>')

    define_v1_routes(app)

