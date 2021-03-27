package com.example.myapplication;

public class GeoIntel {
    static {
        System.loadLibrary("geoIntelligence");
    }
    public native int calculateFence(double lat, double longi);

}
