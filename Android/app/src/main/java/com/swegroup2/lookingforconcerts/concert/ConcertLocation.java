package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class ConcertLocation implements Serializable {
    @SerializedName("venue")
    @Expose
    public String venue;

    @SerializedName("coordinates")
    @Expose
    public String coordinates;

    public String address;
}
