package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Image implements Serializable {
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
