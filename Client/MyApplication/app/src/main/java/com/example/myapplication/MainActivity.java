package com.example.myapplication;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.tasks.OnSuccessListener;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import java.util.Locale;


public class MainActivity extends AppCompatActivity{
    private double lat=0.0,lng=0.0;
    private int returnFromGeo = -1;
    private FusedLocationProviderClient fusedLocationClient;
    private  TextView locationtv;
    private GeoIntel gi;
    private TextView geofencetv;
    private LocationManager locationManager;
    static {
        System.loadLibrary("geoIntelligence");
    }

    @Override
    protected void onStart() {
        super.onStart();
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED)
        {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this, android.Manifest.permission.ACCESS_FINE_LOCATION)){
               ActivityCompat.requestPermissions(this, new String[] {
                                Manifest.permission.ACCESS_FINE_LOCATION,
                                Manifest.permission.ACCESS_COARSE_LOCATION },
                        10);
            }
            else{
                //Requesting permission
                ActivityCompat.requestPermissions(this, new String[] {
                                Manifest.permission.ACCESS_FINE_LOCATION,
                                Manifest.permission.ACCESS_COARSE_LOCATION },
                        10);
            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        geofencetv= (TextView)findViewById(R.id.textViewGeoOut);
        Button buttonCustomInput;
        locationtv = (TextView)findViewById(R.id.textView);
        buttonCustomInput = (Button)findViewById(R.id.buttonCheckCustomInput);
        buttonCustomInput.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText ed;
                gi = new GeoIntel();
                ed = (EditText)findViewById(R.id.editTextLatitude);
                if(ed.getText().toString().matches("")){
                    geofencetv.setText("Invalid Input");
                }
                else {
                    lat = Double.parseDouble(ed.getText().toString());
                }
                EditText ed2;
                ed2 = (EditText)findViewById(R.id.editTextLongitude);
                if(ed2.getText().toString().matches("")){
                    geofencetv.setText("Invalid Input");
                }
                else {
                    lng = Double.parseDouble(ed2.getText().toString());
                }
                if(gi.calculateFence(lat,lng) == 0 ){
                    geofencetv.setText(""+lat+","+lng+"is "+ " Out");
                }
                else if(gi.calculateFence(lat,lng) == 1 ){
                    geofencetv.setText(""+lat+","+lng+"is "+ "In");
                }
                else if(gi.calculateFence(lat,lng) == 101 ){
                    geofencetv.setText("Config file Missing, Check Storage permissions");
                }
                else if(gi.calculateFence(lat,lng) == 102 ){
                    geofencetv.setText("Invalid Input");
                }
            }
        });

        Button getLocation;
        getLocation = (Button)findViewById(R.id.buttonCurrentLocation);
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        getLocation.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fusedLocationClient.getLastLocation().addOnSuccessListener(MainActivity.this, new OnSuccessListener<Location>() {
                    @Override
                    public void onSuccess(Location location) {
                        // Got last known location. In some rare situations this can be null.
                        if (location != null) {
                            // Logic to handle location object
                            Log.d(location.toString(), "Got location");
                            lat = location.getLatitude();
                            lng = location.getLongitude();
                        }
                    }
                });
                locationtv.setVisibility(View.VISIBLE);
                locationtv.setText(String.format(Locale.US, "%s -- %s", lat, lng));
                gi = new GeoIntel();
                if(gi.calculateFence(lat,lng) == 0 ){
                    geofencetv.setText(""+lat+","+lng+"is "+ " Out");
                }
                else if(gi.calculateFence(lat,lng) == 1 ){
                    geofencetv.setText(""+lat+","+lng+"is "+ "In");
                }
                else if(gi.calculateFence(lat,lng) == 101 ){
                    geofencetv.setText("Config file Missing, Check Storage permissions");
                }
                else if(gi.calculateFence(lat,lng) == 102 ){
                    geofencetv.setText("Invalid Input");
                }

            }
        });
    }

    //public native int calculateFence(double lat, double longi);

}
