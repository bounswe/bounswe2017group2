package com.swegroup2.lookingforconcerts;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

/**
 * Created by furkan on 16.11.2017.
 */

public class RefreshResponse {
    @SerializedName("access")
    @Expose()
    public String access;
}