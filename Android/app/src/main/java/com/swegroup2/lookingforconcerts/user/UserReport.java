package com.swegroup2.lookingforconcerts.user;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by Pınar on 28.12.2017.
 */

public class UserReport implements Serializable{

    @SerializedName("user_report_id")
    @Expose
    public Integer userReportID;

    @SerializedName("reporter")
    @Expose
    public Integer reporter;

    @SerializedName("reported")
    @Expose
    public Integer reported;

    @SerializedName("reason")
    @Expose
    public String reason;
}
