# Geofence
The ultimate geofencing tool

Link to the paper: https://iopscience.iop.org/article/10.1088/1742-6596/1831/1/012017
### Dependencies
For Client
1) Android Studio for Client application

For Server
1) Tensorflow
2) Python flask 
## Steps to run Server
1) Make sure the paths are updated in mypython.py
2) export FLASK_APP=microblog.py
3) flask run
4) Now the server should be available in 127.0.0.1:5000 
5) Navigate to input tab and add lattitude and longitude
6) Click on submit to add the point
7) Add minimum 3 points like this
8) And click on train
9) The server will create a coord.txt
10) This file should be copied to the destination of Android App
11) Run the app
