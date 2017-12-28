package com.swegroup2.lookingforconcerts.concert;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.squareup.picasso.Picasso;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RefreshDto;
import com.swegroup2.lookingforconcerts.RefreshResponse;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.Secret;
import com.swegroup2.lookingforconcerts.adapters.TagListAdapter;
import com.swegroup2.lookingforconcerts.adapters.VenueListAdapter;
import com.swegroup2.lookingforconcerts.login.LoginActivity;
import com.swegroup2.lookingforconcerts.adapters.ArtistListAdapter;

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
        .ArtistListAdapterOnClickHandler, VenueListAdapter.VenueListAdapterOnClickHandler, TagListAdapter.TagListAdapterOnClickHandler, DatePickerDialog.OnDateSetListener{

    EditText concertNameEditText;
    EditText artistNameEditText;
    TextView dateTextView;
    Button dateButton;
    EditText descriptionEditText;
    EditText minPriceEditText;
    EditText maxPriceEditText;
    EditText tagEditText;
    EditText venueEditText;
    EditText ticketLinkEditText;
    Button submitButton;
    Button artistButton;
    Button venueButton;
    Button tagButton;

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

    RecyclerView tagRecyclerView;
    TagListAdapter tagAdapter;
    LinearLayout selectedTagLayout;
    TextView selectedTag;

    String concertName;
    Artist artist;
    String date = "";
    String description;
    Integer minPrice;
    Integer maxPrice;
    List<Tag> tags;
    ConcertLocation location;
    String ticketLink;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_concert);
        concertNameEditText = (EditText) findViewById(R.id.name_edit);
        artistNameEditText = (EditText) findViewById(R.id.artist_edit);
        dateTextView = (TextView) findViewById(R.id.date_tv);
        dateButton = (Button) findViewById(R.id.date_button);
        descriptionEditText = (EditText) findViewById(R.id.description_edit);
        minPriceEditText = (EditText) findViewById(R.id.min_price_edit);
        maxPriceEditText = (EditText) findViewById(R.id.max_price_edit);
        tagEditText = (EditText) findViewById(R.id.tag_edit);
        venueEditText = (EditText) findViewById(R.id.venue_edit);
        ticketLinkEditText = (EditText) findViewById(R.id.link_edit);
        submitButton = (Button) findViewById(R.id.submit_button);
        artistButton = (Button) findViewById(R.id.artist_button);
        venueButton = (Button) findViewById(R.id.venue_button);
        tagButton = (Button) findViewById(R.id.tag_button);

        selectedArtistLayout = (LinearLayout) findViewById(R.id.selected_artist);
        selectedArtistName = (TextView) findViewById(R.id.artist_list_name_tv_selected);
        selectedArtistPicture = (ImageView) findViewById(R.id.artist_list_image_selected);

        selectedVenueLayout = (LinearLayout) findViewById(R.id.selected_venue);
        selectedVenueName = (TextView) findViewById(R.id.venue_list_venue_selected);
        selectedVenueLocation = (TextView) findViewById(R.id.venue_list_address_selected);

        selectedTagLayout = (LinearLayout) findViewById(R.id.selected_tags);
        selectedTag = (TextView) findViewById(R.id.tag_list_tag_selected);

        tags = new ArrayList<>();

        dateButton.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.N)
            @Override
            public void onClick(View view) {
                DatePickerDialog dialog = new DatePickerDialog(CreateConcertActivity.this);
                dialog.setOnDateSetListener(CreateConcertActivity.this);
                dialog.show();
            }
        });

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                concertName = concertNameEditText.getText().toString().trim();
                description = descriptionEditText.getText().toString().trim();
                //TODO: add validation for prices
                minPrice = Integer.parseInt(minPriceEditText.getText().toString().isEmpty() ? "0" :
                        minPriceEditText.getText().toString());
                maxPrice = Integer.parseInt(maxPriceEditText.getText().toString().isEmpty() ? "0" :
                        maxPriceEditText.getText().toString());
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

        tagButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                searchTag();
            }
        });

        artistRecyclerView = (RecyclerView) findViewById(R.id.artist_list_rv);
        venueRecyclerView = (RecyclerView) findViewById(R.id.venue_list_rv);
        tagRecyclerView = (RecyclerView) findViewById(R.id.tag_list_rv);

        LinearLayoutManager artistLayoutManager = new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false);
        artistRecyclerView.setLayoutManager(artistLayoutManager);

        LinearLayoutManager venueLayoutManager = new LinearLayoutManager(this,
                LinearLayoutManager.VERTICAL, false);
        venueRecyclerView.setLayoutManager(venueLayoutManager);

        LinearLayoutManager tagLayoutManager = new LinearLayoutManager(this, LinearLayoutManager
                .VERTICAL, false);
        tagRecyclerView.setLayoutManager(tagLayoutManager);

        artistAdapter = new ArtistListAdapter(this, this);
        artistRecyclerView.setAdapter(artistAdapter);

        venueAdapter = new VenueListAdapter(this, this);
        venueRecyclerView.setAdapter(venueAdapter);

        tagAdapter = new TagListAdapter(this, this);
        tagRecyclerView.setAdapter(tagAdapter);

    }

    private boolean isValid() {
        return !(concertName.isEmpty() || artist == null || date.isEmpty() || location == null);
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
        concertDto.tags = tags;
        concertDto.location = location;
        concertDto.comments = new ArrayList<>();
        if (!ticketLink.equals("")) {
            concertDto.sellerUrl = ticketLink;
        }

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
                            if (response.body() != null) {
                                LoginActivity.accessToken = response.body().access;
                                postRequestMethod();
                            }
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

        String name = artistNameEditText.getText().toString().replace(' ', '+').trim();

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
        map.put("query", venueEditText.getText().toString().replace(' ', '+').trim());
        map.put("key", Secret.GOOGLE_PLACES_API_KEY);
        map.put("region", "tr");

        Call<JsonElement> call = controller.searchForVenue(map);
        call.enqueue(new Callback<JsonElement>() {
            @Override
            public void onResponse(Call<JsonElement> call, Response<JsonElement> response) {
                List<ConcertLocation> list = getLocationFromJSON(response.body());
                venueAdapter.setVenueData(new ArrayList<ConcertLocation>());
                venueAdapter.setVenueData(list);
                venueRecyclerView.setVisibility(View.VISIBLE);
            }

            private List<ConcertLocation> getLocationFromJSON(JsonElement body) {
                List<ConcertLocation> list = new ArrayList<>();

                try {
                    JsonArray results = body.getAsJsonObject().getAsJsonArray("results");

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
            public void onFailure(Call<JsonElement> call, Throwable t) {
                Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void searchTag() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        final RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        // TODO: check for what to do when there are spaces in the tag entered
        String tag = tagEditText.getText().toString().replaceAll(" ", "%20").trim();
        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);

        Call<List<Tag>> call = controller.searchTags(tag, map);
        call.enqueue(new Callback<List<Tag>>() {
            @Override
            public void onResponse(Call<List<Tag>> call, Response<List<Tag>> response) {
                if (response.message().equals("Unauthorized")) {
                    final RefreshDto refreshDto = new RefreshDto();
                    refreshDto.refresh = LoginActivity.refreshToken;
                    Call<RefreshResponse> callRefresh = controller.refresh(refreshDto);
                    callRefresh.enqueue(new Callback<RefreshResponse>() {
                        @Override
                        public void onResponse(Call<RefreshResponse> call, Response<RefreshResponse> response) {
                            LoginActivity.accessToken = response.body().access;
                            searchTag();
                        }

                        @Override
                        public void onFailure(Call<RefreshResponse> call, Throwable t) {
                            Toast.makeText(CreateConcertActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    });
                }

                tagAdapter.setTagData(new ArrayList<Tag>());
                tagAdapter.setTagData(response.body());
                tagRecyclerView.setVisibility(View.VISIBLE);
            }

            @Override
            public void onFailure(Call<List<Tag>> call, Throwable t) {
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

        this.location = location;
    }

    @Override
    public void onClick(Tag tag) {
        tagRecyclerView.setVisibility(View.GONE);

        selectedTag.setText(selectedTag.getText() + "* " + tag.value + " (" + tag.context + ")" +
                "\n");
        selectedTagLayout.setVisibility(View.VISIBLE);

        tags.add(tag);
    }

    @Override
    public void onDateSet(DatePicker datePicker, int year, int month, int dayOfMonth) {
        String s = year + "-" + month + "-" + dayOfMonth;
        dateTextView.setText("Date: " + s);
        dateTextView.setVisibility(View.VISIBLE);
        date = s;
    }
}




