package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;
import java.util.List;


/**
 * Created by furkan on 9.10.2017.
 */


public class ConcertDto implements Serializable {

    @SerializedName("concert_id")
    @Expose()
    public Integer id;

    @SerializedName("name")
    @Expose()
    public String name;

    @SerializedName("artist")
    @Expose()
    public Artist artist;

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
    public List<ConcertComment> comments;

    @SerializedName("attendees")
    @Expose()
    public List<Integer> attendees;

    @SerializedName("ratings")
    @Expose()
    public List<Ratings> ratings;

    @SerializedName("seller_url")
    @Expose()
    public String sellerUrl;

    @SerializedName("image")
    @Expose()
    public String image;
}

class Tag implements Serializable {
    @SerializedName("value")
    @Expose
    public String value;

    @SerializedName("context")
    @Expose
    public String context;
}


class Ratings implements Serializable {
    @SerializedName("concert_atmosphere")
    @Expose
    public Integer concert_atmosphere;
    @SerializedName("artist_costumes")
    @Expose
    public Integer artist_costumes;
    @SerializedName("music_quality")
    @Expose
    public Integer music_quality;
    @SerializedName("stage_show")
    @Expose
    public Integer stage_show;
    @SerializedName("owner")
    @Expose
    public Integer owner;
    @SerializedName("concert")
    @Expose
    public Integer concert;

}

