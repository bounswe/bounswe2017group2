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
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.swegroup2.lookingforconcerts.SearchListAdapter;
import com.swegroup2.lookingforconcerts.login.LoginActivity;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RefreshDto;
import com.swegroup2.lookingforconcerts.RefreshResponse;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.user.UserDto;
import com.swegroup2.lookingforconcerts.user.UserProfileActivity;

import org.w3c.dom.Text;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static com.swegroup2.lookingforconcerts.login.LoginActivity.accessToken;
import static com.swegroup2.lookingforconcerts.login.LoginActivity.refreshToken;

public class ConcertListActivity extends AppCompatActivity implements ConcertListAdapter.ConcertListAdapterOnClickHandler, SearchListAdapter.SearchListAdapterOnClickHandler {
    private RecyclerView recyclerView;
    private RecyclerView horizontalRecyclerView;
    private RecyclerView searchRecyclerView;
    private ConcertListAdapter adapter;
    private ConcertListAdapter horizontalAdapter;
    private SearchListAdapter searchAdapter;
    private Button createConcertButton;
    private Button logoutButton;
    private TextView recommendationText;
    public static List<ConcertDto> concerts;
    public static UserDto userDto;
    static Button profile;

    private SearchView mSearch;

    private Button spotifyButton;


    private EditText concertSearch;
    private Button concertSearchButton;

    LinearLayout selectedConcertLayout;
    TextView selectedConcertName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_concert_list);


        recyclerView = (RecyclerView) findViewById(R.id.concert_list_rv);
       horizontalRecyclerView = (RecyclerView) findViewById(R.id.recommendation_rv);

        LinearLayoutManager layoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        recyclerView.setLayoutManager(layoutManager);

        adapter = new ConcertListAdapter(this);
        recyclerView.setAdapter(adapter);

        LinearLayoutManager horizontalLayoutManager = new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false);
        horizontalRecyclerView.setLayoutManager(horizontalLayoutManager);

        horizontalAdapter = new ConcertListAdapter(this);
        horizontalRecyclerView.setAdapter(horizontalAdapter);

        recommendationText = (TextView) findViewById(R.id.recommendation_text);

        createConcertButton = (Button) findViewById(R.id.create_concert_btn);
        profile = (Button) findViewById(R.id.profile);


        spotifyButton = (Button) findViewById(R.id.spotifyButton);


        concertSearch = (EditText) findViewById(R.id.search_edit);
        concertSearch.clearFocus();
        concertSearchButton = (Button) findViewById(R.id.search_button);

        selectedConcertLayout = (LinearLayout) findViewById(R.id.selected_concert);
        selectedConcertName = (TextView) findViewById(R.id.concertlist_name_tv_selected);

        concertSearchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedConcertLayout.setVisibility(View.GONE);
                searchConcert();
            }
        });

        searchRecyclerView = (RecyclerView) findViewById(R.id.search_list_rv);

        LinearLayoutManager searchLayoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        searchRecyclerView.setLayoutManager(searchLayoutManager);

        searchAdapter = new SearchListAdapter(this, this);
        searchRecyclerView.setAdapter(searchAdapter);


        getConcerts();
        getProfileInfo(this);
        getRecommendedConcerts();


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
                     }

        );
    }

    public void getRecommendedConcerts() {
        LoginActivity.refresh(this);
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);

        Call<List<ConcertDto>> call = controller.getRecommendedConcerts(map);

        call.enqueue(new Callback<List<ConcertDto>>() {
                         @Override
                         public void onResponse(Call<List<ConcertDto>> call, Response<List<ConcertDto>> response) {
                             concerts = response.body();
                             horizontalAdapter.setConcertData(concerts);
                         }

                         @Override
                         public void onFailure(Call<List<ConcertDto>> call, Throwable t) {
                             Toast.makeText(ConcertListActivity.this, "ERROR", Toast.LENGTH_SHORT).show();
                         }
                     }

        );
    }

    private void searchConcert() {
        refresh();
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        String search = concertSearch.getText().toString();

        Call<List<ConcertDto>> call = controller.searchConcert(search);
        call.enqueue(new Callback<List<ConcertDto>>() {
            @Override
            public void onResponse(Call<List<ConcertDto>> call, Response<List<ConcertDto>> response) {
                searchAdapter.setConcertData(new ArrayList<ConcertDto>());
                searchAdapter.setConcertData(response.body());
                searchRecyclerView.setVisibility(View.VISIBLE);
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

    public void spotifyConnect(View view) {

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
