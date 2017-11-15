package com.swegroup2.lookingforconcerts;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

/**
 * Created by Pınar on 15.11.2017.
 */

public class UserDto {


    @SerializedName("email")
    @Expose()
    public String email;

    @SerializedName("password")
    @Expose()
    public String password;

    @SerializedName("first_name")
    @Expose()
    public String first_name;

    @SerializedName("last_name")
    @Expose()
    public String last_name;

    @SerializedName("age")
    @Expose()
    public Integer age;

    @SerializedName("date_joined")
    @Expose()
    public Integer date_joined;

    @SerializedName("is_active")
    @Expose()
    public Boolean is_active;

    @SerializedName("avatar")
    @Expose()
    public String avatar;

    @SerializedName("comments")
    @Expose()
    public List<ConcertComment> comments;
}
