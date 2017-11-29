package com.swegroup2.lookingforconcerts.concert;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.SearchView;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.swegroup2.lookingforconcerts.login.LoginActivity;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RefreshDto;
import com.swegroup2.lookingforconcerts.RefreshResponse;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.user.UserDto;
import com.swegroup2.lookingforconcerts.user.UserProfileActivity;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ConcertListActivity extends AppCompatActivity implements ConcertListAdapter.ConcertListAdapterOnClickHandler {
    private RecyclerView recyclerView;
    private ConcertListAdapter adapter;
    private Button createConcertButton;
    private Button logoutButton;
    public static List<ConcertDto> concerts;
    public static UserDto userDto;
    static Button profile;

    private SearchView mSearch;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_concert_list);


        recyclerView = (RecyclerView) findViewById(R.id.concert_list_rv);

        LinearLayoutManager layoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        recyclerView.setLayoutManager(layoutManager);

        adapter = new ConcertListAdapter(this);
        recyclerView.setAdapter(adapter);

        createConcertButton = (Button) findViewById(R.id.create_concert_btn);
        profile = (Button) findViewById(R.id.profile);
        profile.setClickable(false);

        getConcerts();
        getProfileInfo(this);


    }

    @Override
    public void onClick(ConcertDto concertDto) {
        getSupportFragmentManager()
                .beginTransaction()
                .setCustomAnimations(R.anim.enter_from_right, R.anim.exit_to_right)
                .replace(R.id.layout_concert_list, new ConcertDetails().newInstance(concertDto))
                .add(R.id.layout_concert_list, new ConcertDetails())
                .addToBackStack(null)
                .commit();
    }

    public void getConcerts() {
        LoginActivity.refresh(this);
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Call<List<ConcertDto>> call = controller.getAllConcerts();

        call.enqueue(new Callback<List<ConcertDto>>() {
            @Override
            public void onResponse(Call<List<ConcertDto>> call, Response<List<ConcertDto>> response) {
                concerts = response.body();
                adapter.setConcertData(concerts);

            }

            @Override
            public void onFailure(Call<List<ConcertDto>> call, Throwable t) {
                Toast.makeText(ConcertListActivity.this, "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public static void getProfileInfo(final Context context) {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);

        Call<UserDto> call = controller.getUserProfile(map);

        call.enqueue(new Callback<UserDto>() {
            @Override
            public void onResponse(Call<UserDto> call, Response<UserDto> response) {
                userDto = response.body();
                profile.setClickable(true);
            }

            @Override
            public void onFailure(Call<UserDto> call, Throwable t) {
                Toast.makeText(context, "PROFILE ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public static void profile(View view) {
        Intent intent = new Intent(view.getContext(), UserProfileActivity.class);
        view.getContext().startActivity(intent);
    }

    public void createConcert(View view) {
        Intent intent = new Intent(this, CreateConcertActivity.class);
        startActivity(intent);
        finish();
    }

    public void logoutFunc(View view) {
        Intent intent = new Intent(this, LoginActivity.class);
        SharedPreferences preferences = PreferenceManager
                .getDefaultSharedPreferences(getApplicationContext());
        preferences.edit().remove("token").commit();
        startActivity(intent);
        finish();
    }
}
