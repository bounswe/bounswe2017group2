package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import com.swegroup2.lookingforconcerts.user.UserDto;

import java.io.Serializable;

public class ConcertComment implements Serializable {
    @SerializedName("content_id")
    @Expose
    public Integer contentID;

    @SerializedName("content")
    @Expose
    public String content;

    @SerializedName("owner")
    @Expose
    public UserDto owner;

}
