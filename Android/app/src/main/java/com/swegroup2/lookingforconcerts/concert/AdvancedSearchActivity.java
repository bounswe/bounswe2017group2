package com.swegroup2.lookingforconcerts.concert;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.adapters.SearchListAdapter;
import com.swegroup2.lookingforconcerts.login.LoginActivity;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by Pınar on 13.12.2017.
 */

public class AdvancedSearchActivity extends AppCompatActivity implements SearchListAdapter.SearchListAdapterOnClickHandler {
    private RecyclerView searchRecyclerView;

    private SearchListAdapter searchAdapter;

    private TextView advancedSearchText;

    private EditText concertNameText;
    private EditText artistNameText;
    private EditText locationVenueText;
    private EditText tagValueText;
    private EditText minPriceText;
    private EditText maxPriceText;

    private Button advancedSearchButton;

    private LinearLayout selectedConcertLayout;
    private TextView selectedConcertName;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_advanced_search);

        searchRecyclerView = (RecyclerView) findViewById(R.id.search_list_rv);

        searchAdapter = new SearchListAdapter(this, this);
        searchRecyclerView.setAdapter(searchAdapter);

        advancedSearchText = (TextView) findViewById(R.id.advanced_search_text);

        concertNameText = (EditText) findViewById(R.id.concert_name_text);
        artistNameText = (EditText) findViewById(R.id.artist_name_text);
        locationVenueText = (EditText) findViewById(R.id.location_venue_text);
        tagValueText = (EditText) findViewById(R.id.tag_value_text);
        minPriceText = (EditText) findViewById(R.id.min_price_text);
        maxPriceText = (EditText) findViewById(R.id.max_price_text);

        advancedSearchButton = (Button) findViewById(R.id.advanced_search_button);
        advancedSearchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedConcertLayout.setVisibility(View.GONE);
                advancedSearch();
            }
        });

        selectedConcertLayout = (LinearLayout) findViewById(R.id.selected_concert);
        selectedConcertName = (TextView) findViewById(R.id.concertlist_name_tv_selected);

        LinearLayoutManager searchLayoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        searchRecyclerView.setLayoutManager(searchLayoutManager);

        searchAdapter = new SearchListAdapter(this, this);
        searchRecyclerView.setAdapter(searchAdapter);
    }

    @Override
    public void onClick(ConcertDto concertDto) {
        getSupportFragmentManager()
                .beginTransaction()
                .setCustomAnimations(R.anim.enter_from_right, R.anim.exit_to_right)
                .replace(R.id.layout_advanced_search, new ConcertDetails().newInstance(concertDto))
                .add(R.id.layout_advanced_search, new ConcertDetails())
                .addToBackStack(null)
                .commit();

    }


    private void advancedSearch() {
        LoginActivity.refresh(this);
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        String concertName = concertNameText.getText().toString();
        String artistName = artistNameText.getText().toString();
        String locationVenue = locationVenueText.getText().toString();
        String tagValue = tagValueText.getText().toString();
        String minPrice = minPriceText.getText().toString();
        String maxPrice = maxPriceText.getText().toString();

        Call<List<ConcertDto>> call = controller.advancedSearch(concertName, artistName, locationVenue,
                tagValue, minPrice, maxPrice);
        call.enqueue(new Callback<List<ConcertDto>>() {
            @Override
            public void onResponse(Call<List<ConcertDto>> call, Response<List<ConcertDto>> response) {
                searchAdapter.setConcertData(new ArrayList<ConcertDto>());
                searchAdapter.setConcertData(response.body());
                searchRecyclerView.setVisibility(View.VISIBLE);
                //Toast.makeText(AdvancedSearchActivity.this, response.body().toString(), Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<List<ConcertDto>> call, Throwable t) {
                Toast.makeText(AdvancedSearchActivity.this, "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
