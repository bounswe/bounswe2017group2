package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Ratings implements Serializable {
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
