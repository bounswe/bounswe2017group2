package com.swegroup2.lookingforconcerts;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

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

    private Button profile;

    String refreshToken = "";
    String accessToken = "";

    UserDto userProfileInfo = new UserDto();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_concert_list);

        refreshToken = getIntent().getStringExtra("refresh");
        accessToken = getIntent().getStringExtra("access");
        Log.v("myTag", "refresh: " + refreshToken);
        Log.v("myTag", "access: " + accessToken);

        recyclerView = (RecyclerView) findViewById(R.id.concert_list_rv);

        LinearLayoutManager layoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        recyclerView.setLayoutManager(layoutManager);

        adapter = new ConcertListAdapter(this);
        recyclerView.setAdapter(adapter);

        createConcertButton = (Button) findViewById(R.id.create_concert_btn);
        profile = (Button) findViewById(R.id.profile);

        //logoutButton = (Button) findViewById(R.id.logout_btn);

        getConcerts();
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

    private void getConcerts() {
        refresh();
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Call<List<ConcertDto>> call = controller.getAllConcerts();

        call.enqueue(new Callback<List<ConcertDto>>() {
            @Override
            public void onResponse(Call<List<ConcertDto>> call, Response<List<ConcertDto>> response) {
                adapter.setConcertData(response.body());
            }

            @Override
            public void onFailure(Call<List<ConcertDto>> call, Throwable t) {
                Toast.makeText(ConcertListActivity.this, "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void refresh() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        RefreshDto refreshDto = new RefreshDto();
        refreshDto.refresh = refreshToken;

        Call<RefreshResponse> call = controller.refresh(refreshDto);

        call.enqueue(new Callback<RefreshResponse>() {
            @Override
            public void onResponse(Call<RefreshResponse> call, Response<RefreshResponse> response) {
                if (!accessToken.equals(response.body().access)) {
                    accessToken = response.body().access;
                    Log.d("FS", "accessToken " + accessToken);
                }
            }

            @Override
            public void onFailure(Call<RefreshResponse> call, Throwable t) {
                Toast.makeText(ConcertListActivity.this, "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void profile(View view) {
        refresh();
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + accessToken);

        Call<UserDto> call = controller.getUserProfile(map);

        call.enqueue(new Callback<UserDto>() {
            @Override
            public void onResponse(Call<UserDto> call, Response<UserDto> response) {

                Toast.makeText(ConcertListActivity.this,response.body().username, Toast.LENGTH_LONG).show();
            }

            @Override
            public void onFailure(Call<UserDto> call, Throwable t) {
                Toast.makeText(ConcertListActivity.this, "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void createConcert(View view) {
        Intent intent = new Intent(this, CreateConcertActivity.class);

        intent.putExtra("refresh", refreshToken);
        intent.putExtra("access", accessToken);

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
