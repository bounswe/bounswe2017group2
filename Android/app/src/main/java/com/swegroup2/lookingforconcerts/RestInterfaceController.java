package com.swegroup2.lookingforconcerts;


import com.google.gson.JsonObject;

import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.HeaderMap;
import retrofit2.http.POST;
import retrofit2.http.Path;
import retrofit2.http.Query;
import retrofit2.http.QueryMap;

/**
 * Created by furkan on 9.10.2017.
 */

public interface RestInterfaceController {

    @POST("/concert/{id}/newcomment/")
    Call<ConcertResponse> makeComment(@Path("id") int id, @Body ConcertComment comment, @HeaderMap Map<String, String> headermap);

    @POST("/newconcert/")
    Call<ConcertResponse> createConcert(@Body ConcertDto concertDto, @HeaderMap Map<String, String> headermap);

    @GET("/maps/api/place/textsearch/json")
    Call<JsonObject> searchForVenue(@QueryMap Map<String, String> queryMap);

    @GET("/concerts/")
    Call<List<ConcertDto>> getAllConcerts();

    @GET("/user/me/")
    Call<UserDto> getUserProfile(@HeaderMap Map<String, String> headermap);

    @GET("/concert/{id}/subscribe/")
    Call<ConcertResponse> attend(@Path("id") int id, @HeaderMap Map<String, String> headermap);

    @GET("/concerts/search/")
    Call<List<ConcertDto>> searchConcert(@Query("search") String search);

    @POST("/signup/")
    Call<UserResponse> signUp(@Body UserDto userDto);

    @POST("/api/auth/token/refresh/")
    Call<RefreshResponse> refresh(@Body RefreshDto refreshDto);

    @GET("/searchartists/")
    Call<List<Artist>> searchForArtist(@Query("name") String name);

    @POST("/upload_user_image/")
    Call<UserResponse> uploadImage(@Body UserDto userDto );
}