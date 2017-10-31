package com.swegroup2.lookingforconcerts;



import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;

import retrofit2.http.POST;

/**
 * Created by furkan on 9.10.2017.
 */

public interface RestInterfaceController {

    @POST("/newconcert/")
    Call<ConcertResponse> createConcert(@Body ConcertDto concertDto);

    @GET("/concerts")
    Call<List<ConcertDto>> getAllConcerts();

}
