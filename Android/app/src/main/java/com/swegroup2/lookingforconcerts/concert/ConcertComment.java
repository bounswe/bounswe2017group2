package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class ConcertComment implements Serializable {
    @SerializedName("content")
    @Expose
    public String content;

}
