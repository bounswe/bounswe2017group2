package com.swegroup2.lookingforconcerts;

import java.util.Date;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

/**
 * Created by furkan on 9.10.2017.
 */


public class ConcertDto {
    @SerializedName("artistName")
    @Expose()
    public String artistName;

    @SerializedName("latitude")
    @Expose()
    public Double latitude;

    @SerializedName("longtitude")
    @Expose()
    public Double longtitude;

    @SerializedName("date")
    @Expose()
    public Date date;

    @SerializedName("date")
    @Expose()
    public Double minPrice;

    @SerializedName("date")
    @Expose()
    public Double maxPrice;
}
