package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import com.swegroup2.lookingforconcerts.user.UserDto;

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
    public List<UserDto> attendees;

    @SerializedName("ratings")
    @Expose()
    public List<Ratings> ratings;

    @SerializedName("seller_url")
    @Expose()
    public String sellerUrl;

    @SerializedName("image")
    @Expose()
    public String image;

    @SerializedName("reports")
    @Expose()
    public List<Integer> reports;
}


