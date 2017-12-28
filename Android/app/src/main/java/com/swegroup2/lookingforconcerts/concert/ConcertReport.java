package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;
import java.util.List;

/**
 * Created by Pınar on 28.12.2017.
 */

public class ConcertReport implements Serializable{

    @SerializedName("concert_report_id")
    @Expose
    public Integer concertReportID;

    @SerializedName("upvoters")
    @Expose
    public List<Integer> upvoters;

    @SerializedName("suggestion")
    @Expose
    public String suggestion;

    @SerializedName("reporter")
    @Expose
    public Integer reporter;

    @SerializedName("concert")
    @Expose
    public Integer concert;

}
