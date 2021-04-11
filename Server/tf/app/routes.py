from flask import send_file

from app.index import define_v1_routes
from app.common.utils.grid_fs import get_file
from app.geofence.views import GeoFenceApi, GeoFencesApi, GeoFenceCollectionApi
from app.task.views import TasksApi, TaskApi


def initialize_routes(api, app):
    api.add_resource(GeoFencesApi, '/api/v1/geofence')
    api.add_resource(GeoFenceCollectionApi, '/api/v1/geofence-collection')
    api.add_resource(GeoFenceApi, '/api/v1/geofence/<fence_id>')

    api.add_resource(TasksApi, '/api/v1/job')
    api.add_resource(TaskApi, '/api/v1/job/<job_id>')

    define_v1_routes(app)

    @app.route('/api/v1/grid-file/<file_id>')
    def get_image(file_id):
        return send_file(get_file(file_id),
                         mimetype='text/plain',
                         as_attachment=True,
                         attachment_filename='%s.txt' % file_id)

