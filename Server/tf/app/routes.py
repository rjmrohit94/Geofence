from flask import render_template,request
from app import app
from app.forms import InputForm
import subprocess
import mypython
processed_Lat=[0,0,0,0,0,0,0]
processed_Lon=[0,0,0,0,0,0,0]
iter=0
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
    return render_template('input.html',title='Submit', len=1,form=form , Latitude=0,Longitude=0)
@app.route('/Input', methods=['POST'])
def input_post():
    global iter
    form = InputForm()
    if 'Submit' in request.form:
        Latitude = request.form['Latitude']
        Longitude = request.form['Longitude']
        processed_Lat[iter] = Latitude.upper()
        processed_Lon[iter] = Longitude.upper()
        iter=iter+1
        return render_template('input.html',title='Submit',len=iter, form=form, Latitude=processed_Lat,Longitude=processed_Lon)
    elif 'Train' in request.form:
        Completelist=[]
        for i in range(0,iter):
            Completelist=Completelist+[(float(processed_Lat[i]),float(processed_Lon[i]))]
        mypython.generate_dataset(Completelist)
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