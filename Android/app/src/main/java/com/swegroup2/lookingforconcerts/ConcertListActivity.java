package com.swegroup2.lookingforconcerts;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.List;

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
        logoutButton = (Button) findViewById(R.id.logout_btn);

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

    public void createConcert(View view) {
        Intent intent = new Intent(this, CreateConcertActivity.class);
        String refreshToken="";
        String accessToken="";
        try {
            JSONObject jsonObj = new JSONObject(getIntent().getStringExtra("json"));
            refreshToken = jsonObj.getString("refresh");
            accessToken = jsonObj.getString("access");
            Log.v("myTag","refresh: " + refreshToken);
            Log.v("myTag","access: " + accessToken);


        } catch (JSONException e) {
            e.printStackTrace();
        }
        intent.putExtra("refresh", refreshToken);
        intent.putExtra("access", accessToken);

        startActivity(intent);
        finish();
    }

    public void logoutFunc(View view){
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
        finish();
    }
}
