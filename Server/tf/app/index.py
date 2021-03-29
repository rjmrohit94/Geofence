# this can be deprecated once REST endpoints and clients are inplace

from flask import render_template, request
from app.forms import InputForm
from ml import mypython

_iter = 0


def define_v1_routes(app):
    processed_lat = [0, 0, 0, 0, 0, 0, 0]
    processed_lon = [0, 0, 0, 0, 0, 0, 0]

    @app.route('/')
    @app.route('/index')
    def index():
        user = {'username': 'George'}
        posts = [
            {
                'author': {'username': 'George'},
                'body': 'Beautiful day in Kerala!'
            },
            {
                'author': {'username': 'Rohit'},
                'body': 'NN is cool!'
            }
        ]
        return render_template('index.html', title='Home', user=user, posts=posts)

    @app.route('/Input')
    def input():
        form = InputForm()
        return render_template('input.html', title='Submit', len=1, form=form, Latitude=0, Longitude=0)

    @app.route('/Input', methods=['POST'])
    def input_post():
        global _iter
        form = InputForm()
        if 'Submit' in request.form:
            latitude = request.form['Latitude']
            longitude = request.form['Longitude']
            processed_lat[_iter] = latitude.upper()
            processed_lon[_iter] = longitude.upper()
            _iter = _iter + 1
            return render_template('input.html', title='Submit', len=_iter, form=form, Latitude=processed_lat,
                                   Longitude=processed_lon)
        elif 'Train' in request.form:
            complete_list = []
            for i in range(0, _iter):
                complete_list = complete_list + [(float(processed_lat[i]), float(processed_lon[i]))]
            mypython.generate_dataset(complete_list)
            mypython.train_neurons()
            user = {'username': 'Training Over'}
            posts = [
                {
                    'author': {'username': 'John'},
                    'body': 'Beautiful day in Kerala!'
                },
                {
                    'author': {'username': 'Rohit'},
                    'body': 'NN is cool!'
                }
            ]
            return render_template('index.html', title='Home', user=user, posts=posts)
