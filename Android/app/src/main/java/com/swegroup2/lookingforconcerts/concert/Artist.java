package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;
import java.util.List;

public class Artist implements Serializable {
    @SerializedName("name")
    @Expose
    public String name;
    @SerializedName("spotify_id")
    @Expose
    public String spotifyId;
    @SerializedName("concerts")
    @Expose
    public List<Integer> concerts;
    @SerializedName("images")
    @Expose
    public List<Image> images;

}
