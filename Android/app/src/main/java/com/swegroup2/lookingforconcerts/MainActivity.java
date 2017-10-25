package com.swegroup2.lookingforconcerts;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity{

    EditText artistName;
    EditText location;
    EditText date;
    EditText time;
    Button submit;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        artistName= (EditText) findViewById(R.id.artist_edit);
        location= (EditText) findViewById(R.id.location_edit);
        date= (EditText) findViewById(R.id.date_edit);
        time= (EditText) findViewById(R.id.time_edit);
        submit= (Button) findViewById(R.id.submit_button);
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });
    }

    public void createConcert(){

    }

    private void postRequestMethod() {

        /*progressDialog = new ProgressDialog(MainActivity.this);
        progressDialog.setMessage("Lütfen Bekleyiniz");
        progressDialog.show();*/


        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("URL")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller= retrofit.create(RestInterfaceController.class);

        ConcertDto concertDto= new ConcertDto();


        concertDto.artistName=artistName.getText().toString();



        Call<ConcertResponse> call=controller.createConcert(concertDto);


        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {

            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(MainActivity.this,"ERROR",Toast.LENGTH_SHORT).show();

            }
        });
    }
}




