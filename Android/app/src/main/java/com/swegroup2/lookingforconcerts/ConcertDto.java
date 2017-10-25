package com.swegroup2.lookingforconcerts;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

/**
 * Created by furkan on 9.10.2017.
 */


public class ConcertDto {
    @SerializedName("name")
    @Expose()
    public String name;

    @SerializedName("artist")
    @Expose()
    public String artistName;

//    @SerializedName("latitude")
//    @Expose()
//    public Double latitude;
//
//    @SerializedName("longtitude")
//    @Expose()
//    public Double longtitude;

    @SerializedName("date_time")
    @Expose()
    public String date;

    @SerializedName("description")
    @Expose()
    public String description;

    @SerializedName("price_min")
    @Expose()
    public Integer minPrice;

    @SerializedName("price_max")
    @Expose()
    public Integer maxPrice;

    @SerializedName("tags")
    @Expose()
    public List<Tag> tags;
}

class Tag {
    @SerializedName("value")
    @Expose
    public String value;
}
