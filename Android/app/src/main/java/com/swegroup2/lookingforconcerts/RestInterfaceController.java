package com.swegroup2.lookingforconcerts;


import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

/**
 * Created by furkan on 9.10.2017.
 */

public interface RestInterfaceController {

    @POST("url")
    Call<ConcertResponse> createConcert(@Body ConcertDto concertDto);
}
