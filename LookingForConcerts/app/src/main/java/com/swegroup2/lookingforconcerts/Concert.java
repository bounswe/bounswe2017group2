package com.swegroup2.lookingforconcerts;

import android.location.Location;
import android.util.Pair;
import java.util.Date;

/**
 * Created by furkan on 9.10.2017.
 */


public class Concert {
    String artistName;
    Location location;
    Date date;
    Pair<Double,Double> priceRange;

    public String getArtistName() {
        return artistName;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Location getLocation() {
        return location;
    }

    public void setLocation(Location location) {
        this.location = location;
    }

    public Pair<Double, Double> getPriceRange() {
        return priceRange;
    }

    public void setPriceRange(Pair<Double, Double> priceRange) {
        this.priceRange = priceRange;
    }

    public void setArtistName(String artistName) {
        this.artistName = artistName;
    }

    public Concert(String artistName, Location location, Date date, Pair<Double,Double> priceRange){
        this.artistName=artistName;
        this.location=location;
        this.date=date;
        this.priceRange=priceRange;
    }

    public Concert(){}
}
