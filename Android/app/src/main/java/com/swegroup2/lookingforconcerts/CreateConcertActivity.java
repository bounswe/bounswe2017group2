package com.swegroup2.lookingforconcerts;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class CreateConcertActivity extends AppCompatActivity {

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

    String concertName;
    String artistName;
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

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                concertName = concertNameEditText.getText().toString().trim();
                artistName = artistNameEditText.getText().toString().trim();
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
                    postRequestMethod();
                }
            }
        });
    }

    private boolean isValid() {
        return !(concertName.isEmpty() || artistName.isEmpty() || date.isEmpty() || venue.isEmpty
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

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        ConcertDto concertDto = new ConcertDto();
        concertDto.name = concertName;
        concertDto.artist.name = artistName;
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
        map.put("Authorization", "Token " + getIntent().getStringExtra("token"));

        Call<ConcertResponse> call = controller.createConcert(concertDto, map);
        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {
                Intent intent = new Intent(CreateConcertActivity.this, ConcertListActivity.class);
                startActivity(intent);
                CreateConcertActivity.this.finish();
            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(CreateConcertActivity.this, "ERROR", Toast.LENGTH_SHORT).show();

                Intent intent = new Intent(CreateConcertActivity.this, ConcertListActivity.class);
                startActivity(intent);
                CreateConcertActivity.this.finish();
            }
        });
    }
}




