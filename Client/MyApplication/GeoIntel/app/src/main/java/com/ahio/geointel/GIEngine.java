package com.ahio.geointel;


public class GIEngine{
    public  GIEngine(){

    }

    public native int calculateFence(double lat,double lng);
    static {
        System.loadLibrary("geointel");
    }

}
