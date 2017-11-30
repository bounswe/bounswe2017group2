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

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.squareup.picasso.Picasso;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RefreshDto;
import com.swegroup2.lookingforconcerts.RefreshResponse;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.Secret;
import com.swegroup2.lookingforconcerts.VenueListAdapter;
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
        .ArtistListAdapterOnClickHandler, VenueListAdapter.VenueListAdapterOnClickHandler {

    EditText concertNameEditText;
    EditText artistNameEditText;
    EditText dateEditText;
    EditText descriptionEditText;
    EditText minPriceEditText;
    EditText maxPriceEditText;
    EditText tagsEditText;
    EditText venueEditText;
    EditText ticketLinkEditText;
    Button submitButton;
    Button artistButton;
    Button venueButton;

    RecyclerView artistRecyclerView;
    ArtistListAdapter artistAdapter;
    LinearLayout selectedArtistLayout;
    ImageView selectedArtistPicture;
    TextView selectedArtistName;

    RecyclerView venueRecyclerView;
    VenueListAdapter venueAdapter;
    LinearLayout selectedVenueLayout;
    TextView selectedVenueName;
    TextView selectedVenueLocation;

    String concertName;
    Artist artist;
    String date;
    String description;
    Integer minPrice;
    Integer maxPrice;
    String[] tags;
    String venue;
    String coordinates;
    String ticketLink;

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
        ticketLinkEditText = (EditText) findViewById(R.id.link_edit);
        submitButton = (Button) findViewById(R.id.submit_button);
        artistButton = (Button) findViewById(R.id.artist_button);
        venueButton = (Button) findViewById(R.id.venue_button);

        selectedArtistLayout = (LinearLayout) findViewById(R.id.selected_artist);
        selectedArtistName = (TextView) findViewById(R.id.artist_list_name_tv_selected);
        selectedArtistPicture = (ImageView) findViewById(R.id.artist_list_image_selected);

        selectedVenueLayout = (LinearLayout) findViewById(R.id.selected_venue);
        selectedVenueName = (TextView) findViewById(R.id.venue_list_venue_selected);
        selectedVenueLocation = (TextView) findViewById(R.id.venue_list_address_selected);

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
                ticketLink = ticketLinkEditText.getText().toString().trim();

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

        venueButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedVenueLayout.setVisibility(View.GONE);
                searchVenue();
            }
        });

        artistRecyclerView = (RecyclerView) findViewById(R.id.artist_list_rv);
        venueRecyclerView = (RecyclerView) findViewById(R.id.venue_list_rv);

        LinearLayoutManager artistLayoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        artistRecyclerView.setLayoutManager(artistLayoutManager);

        LinearLayoutManager venueLayoutManager = new LinearLayoutManager(this,
                LinearLayoutManager.VERTICAL, false);
        venueRecyclerView.setLayoutManager(venueLayoutManager);

        artistAdapter = new ArtistListAdapter(this, this);
        artistRecyclerView.setAdapter(artistAdapter);

        venueAdapter = new VenueListAdapter(this, this);
        venueRecyclerView.setAdapter(venueAdapter);

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
                temp.value = tag;
                tagList.add(temp);
            }
        }
        concertDto.tags = tagList;
        ConcertLocation concertLocation = new ConcertLocation();
        concertLocation.venue = venue;
        concertLocation.coordinates = coordinates;
        concertDto.location = concertLocation;
        concertDto.comments = new ArrayList<>();
        concertDto.sellerUrl = ticketLink;

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

        String name = artistNameEditText.getText().toString();

        Call<List<Artist>> call = controller.searchForArtist(name);
        call.enqueue(new Callback<List<Artist>>() {
            @Override
            public void onResponse(Call<List<Artist>> call, Response<List<Artist>> response) {
                artistAdapter.setArtistData(new ArrayList<Artist>());
                artistAdapter.setArtistData(response.body());
                artistRecyclerView.setVisibility(View.VISIBLE);
            }

            @Override
            public void onFailure(Call<List<Artist>> call, Throwable t) {
                Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void searchVenue() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://maps.googleapis.com/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Map<String, String> map = new HashMap<>();
        map.put("query", venueEditText.getText().toString().trim());
        map.put("key", Secret.GOOGLE_PLACES_API_KEY);

        Call<JsonObject> call = controller.searchForVenue(map);
        call.enqueue(new Callback<JsonObject>() {
            @Override
            public void onResponse(Call<JsonObject> call, Response<JsonObject> response) {
                List<ConcertLocation> list = getLocationFromJSON(response.body());
                venueAdapter.setVenueData(new ArrayList<ConcertLocation>());
                venueAdapter.setVenueData(list);
                venueRecyclerView.setVisibility(View.VISIBLE);
            }

            private List<ConcertLocation> getLocationFromJSON(JsonObject body) {
                List<ConcertLocation> list = new ArrayList<>();

                try {
                    JsonArray results = body.getAsJsonArray("results");

                    for (int i = 0; i < results.size(); i++) {
                        JsonObject result = results.get(i).getAsJsonObject();

                        ConcertLocation location = new ConcertLocation();
                        location.address = result.get("formatted_address").getAsString();
                        location.venue = result.get("name").getAsString();

                        JsonObject geometry = result.get("geometry").getAsJsonObject();
                        JsonObject loc = geometry.get("location").getAsJsonObject();
                        double lat = loc.get("lat").getAsDouble();
                        double lng = loc.get("lng").getAsDouble();
                        location.coordinates = "" + lat + " " + lng;

                        list.add(location);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

                return list;
            }

            @Override
            public void onFailure(Call<JsonObject> call, Throwable t) {
                Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public void onClick(Artist artist) {
        artistRecyclerView.setVisibility(View.GONE);

        if (!artist.images.isEmpty()) {
            Picasso.with(this).load(artist.images.get(0).url).into(selectedArtistPicture);
        }
        selectedArtistName.setText(artist.name);
        selectedArtistLayout.setVisibility(View.VISIBLE);

        this.artist = artist;
    }

    @Override
    public void onClick(ConcertLocation location) {
        venueRecyclerView.setVisibility(View.GONE);

        selectedVenueName.setText(location.venue);
        selectedVenueLocation.setText(location.address);
        selectedVenueLayout.setVisibility(View.VISIBLE);

        this.venue = location.venue;
        this.coordinates = location.coordinates;
    }
}




