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

    @SerializedName("location")
    @Expose()
    public ConcertLocation location;

    @SerializedName("comments")
    @Expose()
    public List<String> comments;
}

class Tag {
    @SerializedName("label")
    @Expose
    public String label;
}

class ConcertLocation {
    @SerializedName("venue")
    @Expose
    public String venue;

    @SerializedName("coordinates")
    @Expose
    public String coordinates;
}
