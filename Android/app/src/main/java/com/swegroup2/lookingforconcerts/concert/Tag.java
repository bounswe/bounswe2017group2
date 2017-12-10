package com.swegroup2.lookingforconcerts.concert;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by elifguler on 10.12.2017.
 */

public class Tag implements Serializable {
    @SerializedName("value")
    @Expose
    public String value;

    @SerializedName("context")
    @Expose
    public String context;

    @SerializedName("wikidata_uri")
    @Expose
    public String wikidataUri;
}
