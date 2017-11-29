package com.swegroup2.lookingforconcerts.concert;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RefreshDto;
import com.swegroup2.lookingforconcerts.RefreshResponse;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.login.LoginActivity;
import com.swegroup2.lookingforconcerts.search.ArtistListAdapter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class CreateConcertActivity extends AppCompatActivity implements ArtistListAdapter
        .ArtistListAdapterOnClickHandler {

    EditText concertNameEditText;
    EditText artistNameEditText;
    EditText dateEditText;
    EditText descriptionEditText;
    EditText minPriceEditText;
    EditText maxPriceEditText;
    EditText tagsEditText;
    EditText venueEditText;
    EditText coordinatesEditText;
    Button submitButton;
    Button artistButton;
    private RecyclerView recyclerView;
    private ArtistListAdapter adapter;
    LinearLayout selectedArtistLayout;
    ImageView selectedArtistPicture;
    TextView selectedArtistName;

    String concertName;
    Artist artist;
    String date;
    String description;
    Integer minPrice;
    Integer maxPrice;
    String[] tags;
    String venue;
    String coordinates;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_concert);
        concertNameEditText = (EditText) findViewById(R.id.name_edit);
        artistNameEditText = (EditText) findViewById(R.id.artist_edit);
        dateEditText = (EditText) findViewById(R.id.date_edit);
        descriptionEditText = (EditText) findViewById(R.id.description_edit);
        minPriceEditText = (EditText) findViewById(R.id.min_price_edit);
        maxPriceEditText = (EditText) findViewById(R.id.max_price_edit);
        tagsEditText = (EditText) findViewById(R.id.tags_edit);
        venueEditText = (EditText) findViewById(R.id.venue_edit);
        coordinatesEditText = (EditText) findViewById(R.id.coordinates_edit);
        submitButton = (Button) findViewById(R.id.submit_button);
        artistButton = (Button) findViewById(R.id.artist_button);

        selectedArtistLayout = (LinearLayout) findViewById(R.id.selected_artist);
        selectedArtistName = (TextView) findViewById(R.id.artist_list_name_tv_selected);
        selectedArtistPicture = (ImageView) findViewById(R.id.artist_list_image_selected);

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                concertName = concertNameEditText.getText().toString().trim();
                date = dateEditText.getText().toString();
                description = descriptionEditText.getText().toString().trim();
                //TODO: add validation for prices
                minPrice = Integer.parseInt(minPriceEditText.getText().toString().isEmpty() ? "0" :
                        minPriceEditText.getText().toString());
                maxPrice = Integer.parseInt(maxPriceEditText.getText().toString().isEmpty() ? "0" :
                        maxPriceEditText.getText().toString());
                tags = tagsEditText.getText().toString().trim().split(",");
                venue = venueEditText.getText().toString().trim();
                coordinates = coordinatesEditText.getText().toString().trim();

                if (!isValid()) {
                    Toast.makeText(CreateConcertActivity.this, "Required fields can't be empty!", Toast.LENGTH_LONG).show();
                } else {
                    submitButton.setClickable(false);
                    postRequestMethod();
                }
            }
        });

        artistButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedArtistLayout.setVisibility(View.GONE);
                searchArtist();
            }
        });

        recyclerView = (RecyclerView) findViewById(R.id.artist_list_rv);

        LinearLayoutManager layoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        recyclerView.setLayoutManager(layoutManager);

        adapter = new ArtistListAdapter(this, this);
        recyclerView.setAdapter(adapter);
    }

    private boolean isValid() {
        return !(concertName.isEmpty() || artist == null || date.isEmpty() || venue.isEmpty
                () || coordinates.isEmpty());
    }

    private void postRequestMethod() {
        /*progressDialog = new ProgressDialog(CreateConcertActivity.this);
        progressDialog.setMessage("Lütfen Bekleyiniz");
        progressDialog.show();*/

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        final RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        ConcertDto concertDto = new ConcertDto();
        concertDto.name = concertName;
        concertDto.artist = artist;
        concertDto.date = date;
        concertDto.description = description;
        concertDto.minPrice = minPrice;
        concertDto.maxPrice = maxPrice;
        List<Tag> tagList = new ArrayList<>();
        for (String tag : tags) {
            if (!tag.isEmpty()) {
                Tag temp = new Tag();
                temp.label = tag;
                tagList.add(temp);
            }
        }
        concertDto.tags = tagList;
        ConcertLocation concertLocation = new ConcertLocation();
        concertLocation.venue = venue;
        concertLocation.coordinates = coordinates;
        concertDto.location = concertLocation;
        concertDto.comments = new ArrayList<>();

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);

        Call<ConcertResponse> call = controller.createConcert(concertDto, map);
        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {
                if (response.message().equals("Unauthorized")) {
                    final RefreshDto refreshDto = new RefreshDto();
                    refreshDto.refresh = LoginActivity.refreshToken;
                    Call<RefreshResponse> callRefresh = controller.refresh(refreshDto);
                    callRefresh.enqueue(new Callback<RefreshResponse>() {
                        @Override
                        public void onResponse(Call<RefreshResponse> call, Response<RefreshResponse> response) {
                            LoginActivity.accessToken = response.body().access;
                            postRequestMethod();
                        }

                        @Override
                        public void onFailure(Call<RefreshResponse> call, Throwable t) {
                            Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
                            Intent intent = new Intent(CreateConcertActivity.this, ConcertListActivity.class);
                            startActivity(intent);
                            CreateConcertActivity.this.finish();
                        }
                    });
                }

                Intent intent = new Intent(CreateConcertActivity.this, ConcertListActivity.class);
                startActivity(intent);
                CreateConcertActivity.this.finish();
            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(CreateConcertActivity.this, ConcertListActivity.class);
                startActivity(intent);
                CreateConcertActivity.this.finish();
            }
        });
    }

    private void searchArtist() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Artist artist = new Artist();
        artist.name = artistNameEditText.getText().toString();

//        Map<String, String> map = new HashMap<>();
//        map.put("Connection", "close");

        Call<List<Artist>> call = controller.searchForArtist(artist);
        call.enqueue(new Callback<List<Artist>>() {
            @Override
            public void onResponse(Call<List<Artist>> call, Response<List<Artist>> response) {
                adapter.setArtistData(new ArrayList<Artist>());
                adapter.setArtistData(response.body());
                recyclerView.setVisibility(View.VISIBLE);
            }

            @Override
            public void onFailure(Call<List<Artist>> call, Throwable t) {
                Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public void onClick(Artist artist) {
        recyclerView.setVisibility(View.GONE);

        if (!artist.images.isEmpty()) {
            Picasso.with(this).load(artist.images.get(0).url).into(selectedArtistPicture);
        }
        selectedArtistName.setText(artist.name);
        selectedArtistLayout.setVisibility(View.VISIBLE);

        this.artist = artist;
    }
}




