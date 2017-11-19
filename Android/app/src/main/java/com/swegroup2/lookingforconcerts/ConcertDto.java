package com.swegroup2.lookingforconcerts;

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
}

class Tag implements Serializable {
    @SerializedName("label")
    @Expose
    public String label;
}

class ConcertLocation implements Serializable {
    @SerializedName("venue")
    @Expose
    public String venue;

    @SerializedName("coordinates")
    @Expose
    public String coordinates;
}

class ConcertComment implements Serializable {
    @SerializedName("content")
    @Expose
    public String content;
}

class Artist implements Serializable {
    @SerializedName("name")
    @Expose
    public String name;
    @SerializedName("spotify_id")
    @Expose
    public String spotifyId;
    @SerializedName("images")
    @Expose
    public List<Image> images;

}

class Image implements Serializable {
    @SerializedName("url")
    @Expose
    public String url;
    @SerializedName("height")
    @Expose
    public Integer height;
    @SerializedName("width")
    @Expose
    public Integer width;
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

