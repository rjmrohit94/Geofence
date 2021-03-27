import tensorflow as tf
import pandas as pd
from tensorflow import keras
#import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point, LineString
import random
import csv

def random_point_within(poly):
    min_x, min_y, max_x, max_y = poly.bounds

    x = random.uniform(min_x, max_x)
    #x_line = LineString([(x, min_y), (x, max_y)])
    #x_line_intercept_min, x_line_intercept_max = x_line.intersection(poly).xy[1].tolist()
    y = random.uniform(min_y, max_y)

    return Point([x, y])
def generate_dataset(Completeset):
    poly = Polygon(Completeset)
    min_x, min_y, max_x, max_y = poly.bounds
    with open('/home/jarvis/Downloads/tf/coord.txt', 'w') as textFile:
        textFile.write(str(min_x) +'\n')
        textFile.write(str(min_y) +'\n')
        textFile.write(str(max_x) +'\n')
        textFile.write(str(max_y) +'\n')
    textFile.close()
    #print [min_x, min_y, max_x, max_y]
    points = [random_point_within(poly) for i in range(20000)]
    checks = [int(point.within(poly)) for point in points]
    #print (checks[2])
    tmp =[]
    for point in points:
        tmp = tmp + [ [str(point).split('(')[1].split(')')[0]]]
    #print row
    #print [[str(float((i[0].split(' ')[0]))/165.4279876)+' '+ str(float((i[0].split(' ')[1]))/-47.65345814)] for i in tmp]
    row = [[str((float((i[0].split(' ')[0]))-min_x)/(max_x-min_x))+' '+ str((float((i[0].split(' ')[1]))-min_y)/(max_y-min_y))+' ' + str(checks[j]) ] for i,j in zip(tmp,range(len(checks)))]
    row.insert(0,['Lat Long Out'])
    #print float(row[:][0].split(' ')[0])/165.4279876
    #row = [[str(float((i[0].split(' ')[0])))+' '+ str(float((i[0].split(' ')[1])))+' ' + str(checks[j]) ] for i,j in zip(tmp,range(len(checks)))]
    with open('/home/jarvis/Downloads/tf/testdata.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(row)
    csvFile.close()
    points = [random_point_within(poly) for i in range(20000)]
    checks = [int(point.within(poly)) for point in points]
    #print (checks[2])
    tmp =[]
    for point in points:
        tmp = tmp + [ [str(point).split('(')[1].split(')')[0]]]
    #print row
    #print [[str(float((i[0].split(' ')[0]))/165.4279876)+' '+ str(float((i[0].split(' ')[1]))/-47.65345814)] for i in tmp]
    row = [[str((float((i[0].split(' ')[0]))-min_x)/(max_x-min_x))+' '+ str((float((i[0].split(' ')[1]))-min_y)/(max_y-min_y))+' ' + str(checks[j]) ] for i,j in zip(tmp,range(len(checks)))]
    row.insert(0,['Lat Long Out'])
    #print float(row[:][0].split(' ')[0])/165.4279876
    #row = [[str(float((i[0].split(' ')[0])))+' '+ str(float((i[0].split(' ')[1])))+' ' + str(checks[j]) ] for i,j in zip(tmp,range(len(checks)))]
    with open('/home/jarvis/Downloads/tf/traindata.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(row)
    csvFile.close()
def train_neurons():
    traindata= pd.read_csv("/home/jarvis/Downloads/tf/traindata.csv",sep=" ")
    testdata= pd.read_csv("/home/jarvis/Downloads/tf/testdata.csv",sep=" ")
    train_features = traindata[['Lat','Long']]
    train_labels = traindata['Out']
    #print(train_labels[:6])
    #print(train_features[:6])
    test_features = testdata[['Lat','Long']]
    test_labels = testdata['Out']
    #print(test_labels[:6])
    #print(test_features[:6])
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(5,activation=tf.nn.relu,input_shape=(2,)),
        #tf.keras.layers.Dense(5,activation=tf.nn.sigmoid),
        tf.keras.layers.Dense(10,activation=tf.nn.relu),
        tf.keras.layers.Dense(10,activation=tf.nn.relu),
        tf.keras.layers.Dense(20,activation=tf.nn.relu),
        tf.keras.layers.Dense(10,activation=tf.nn.relu),
        tf.keras.layers.Dense(4,activation=tf.nn.relu),
        tf.keras.layers.Dense(1,activation=tf.nn.sigmoid)
    ])
    model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])
    #model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    class myCallbacks(tf.keras.callbacks.Callback):
        def on_epoch_end(self,epochs,logs={}):
            if(logs.get('accuracy')>=0.97):
                self.model.stop_training= True
                print(" Reached 97% Accuracy!")
    callbacks = myCallbacks()
    model.fit(train_features,train_labels,epochs =200,callbacks = [callbacks])
    loss,acc=model.evaluate(test_features,test_labels)
    model.save("/home/jarvis/Downloads/tf/geofence_predictor1.h5")
    for layer in model.layers:
        weights = layer.get_weights()[0]
        bias=layer.get_weights()[1]
        #print(weights.shape)
        with open('/home/jarvis/Downloads/tf/coord.txt', 'a+') as fw:
            for roww in weights:
                for colw in roww:
                    #print(colw)
                    fw.write("%s\n" % colw)
        print(bias.shape)
    for layer in model.layers:
        bias=layer.get_weights()[1]
        with open('/home/jarvis/Downloads/tf/coord.txt', 'a+') as f:
            for rowb in bias:
                #print(rowb)
             #   for col in rowb:
                f.write("%s\n" % rowb)
