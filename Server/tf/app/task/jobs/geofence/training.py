import traceback
import tensorflow as tf
import pandas as pd
from mongoengine import DoesNotExist

from app.geofence.models import Geofence


def retrieve_and_clear_model(geofence_id):
    try:
        geofence = Geofence.objects.get(uu_id=geofence_id)
        geofence.isModelInstalled = False
        if geofence.geoFenceData:
            geofence.geoFenceData.delete()
        if geofence.trainedModel:
            geofence.trainedModel.delete()
        if geofence.geoFenceData or geofence.trainedModel:
            geofence.save()
        return geofence
    except DoesNotExist:
        print("Unable to find geofence with given id")
        return None


class CustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epochs, logs=None):
        if logs and logs.get('accuracy') >= 0.97:
            self.model.stop_training = True
            print(" Reached 97% Accuracy!")


def execute(job_data):
    try:
        geofence_id = job_data.get('geofenceId')
        geofence = retrieve_and_clear_model(geofence_id)
        if geofence.testData and geofence.trainingData:
            train_data = pd.read_csv(geofence.trainingData, sep=" ")
            test_data = pd.read_csv(geofence.testData, sep=" ")
            train_features = train_data[['Lat', 'Long']]
            train_labels = train_data['Out']
            test_features = test_data[['Lat', 'Long']]
            test_labels = test_data['Out']
            model = get_model()
            model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
            callback = CustomCallback()
            model.fit(train_features, train_labels, epochs=200, callbacks=[callback])
            _, _ = model.evaluate(test_features, test_labels)
            geofence.geoFenceData.new_file(encoding='utf-8', content_type='text/plain', file_name='coord.txt')
            write_model_to_file(model, geofence.geoFenceData)
            geofence.geoFenceData.close()
            geofence.save()
    except Exception as _e:
        print(_e.args)
        print(traceback.print_stack())


def get_model():
    return tf.keras.Sequential([
        tf.keras.layers.Dense(5, activation=tf.nn.relu, input_shape=(2,)),
        tf.keras.layers.Dense(10, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.relu),
        tf.keras.layers.Dense(20, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.relu),
        tf.keras.layers.Dense(4, activation=tf.nn.relu),
        tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)
    ])


def write_model_to_file(model, geofence_data):
    for layer in model.layers:
        weights = layer.get_weights()[0]
        for row in weights:
            for col in row:
                geofence_data.write("%s\n" % col)
    for layer in model.layers:
        bias = layer.get_weights()[1]
        for row in bias:
            geofence_data.write("%s\n" % row)
