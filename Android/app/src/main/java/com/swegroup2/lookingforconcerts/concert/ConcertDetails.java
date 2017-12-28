package com.swegroup2.lookingforconcerts.concert;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.RatingBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.login.LoginActivity;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.util.HashMap;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ConcertDetails extends Fragment implements com.google.android.gms.maps.OnMapReadyCallback{

    private static ConcertDto concertDto;
    TextView name;
    TextView artistName;
    TextView date;
    TextView description;
    TextView minPrice;
    TextView maxPrice;
    TextView location;
    MapView mapView;
    TextView sellerUrl;
    TextView comments;
    TextView rateDetails;
    int rateCount = 0;
    EditText commentText;
    RatingBar ratingBar;
    Button attend;
    ImageView concertImage;

    Button comment;
    Button back;
    Button rateSubmit;

    Ratings ratings = new Ratings();
    int atmospehere = 0;
    int costumes = 0;
    int quality = 0;
    int stage = 0;


    public ConcertDetails() {
        // Required empty public constructor
    }

    public static ConcertDetails newInstance(ConcertDto concertDto) {
        ConcertDetails fragment = new ConcertDetails();
        Bundle args = new Bundle();
        args.putByteArray("concert", serialize(concertDto));

        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            concertDto = new ConcertDto();
            concertDto = (ConcertDto) deserialize((getArguments().getByteArray("concert")));

        }

    }

    @Override
    public View onCreateView(final LayoutInflater inflater, final ViewGroup container,
                             final Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_concert_details, container, false);
        name = (TextView) view.findViewById(R.id.name);
        artistName = (TextView) view.findViewById(R.id.artistName);
        date = (TextView) view.findViewById(R.id.date);
        description = (TextView) view.findViewById(R.id.description);
        minPrice = (TextView) view.findViewById(R.id.minPrice);
        maxPrice = (TextView) view.findViewById(R.id.maxPrice);
        location = (TextView) view.findViewById(R.id.location);
        mapView = (MapView) view.findViewById(R.id.mapView);
        sellerUrl = (TextView) view.findViewById(R.id.seller_url);
        comments = (TextView) view.findViewById(R.id.comments);
        rateDetails = (TextView) view.findViewById(R.id.detailed_ratings);
        ratingBar = (RatingBar) view.findViewById(R.id.ratingBar);
        rateSubmit = (Button) view.findViewById(R.id.rate_submit);
        back = (Button) view.findViewById(R.id.back_to_list);
        comment = (Button) view.findViewById(R.id.comment);
        attend = (Button) view.findViewById(R.id.attend);
        commentText = (EditText) view.findViewById(R.id.comment_edittext);



        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getFragmentManager().popBackStack();
            }
        });

        comment.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                makeComment(commentText.getText().toString());
            }
        });

        if (ConcertListActivity.userDto != null && ConcertListActivity.userDto.concerts.contains
                (concertDto
                .id)) {
            attend.setText("UNATTEND");
        }

        attend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (attend.getText().toString().equals("ATTEND")) {
                    attend();
                } else {
                    unAttend();
                }
            }
        });


        name.setText("Name: " + concertDto.name);
        if (concertDto.artist != null) {
            artistName.setText("Artist Name: " + concertDto.artist.name);
        }

        if (concertDto.artist.images!=null){
            new DownloadImageTask((ImageView) view.findViewById(R.id.concert_image))
                    .execute(concertDto.artist.images.get(0).url);
        }

        date.setText("Date: " + concertDto.date);
        description.setText("Description: " + concertDto.description);
        minPrice.setText("Min Price: " + concertDto.minPrice);
        maxPrice.setText("Max Price: " + concertDto.maxPrice);
        location.setText("Location: " + concertDto.location.venue);
        mapView.onCreate(savedInstanceState);
        mapView.getMapAsync(this);
        if (concertDto.sellerUrl != null) {
            sellerUrl.setText("Ticket Link: " + concertDto.sellerUrl);
        } else {
            sellerUrl.setText("Ticket link not available.");
        }
        String allComments = "Comments: \n";

        for (int i = 0; i < concertDto.comments.size(); i++) {
            allComments += concertDto.comments.get(i).content + "\n";
        }

        comments.setText(allComments);

        ratingBar.setStepSize((float) 1.0);


        for (int i = 0; i < concertDto.ratings.size(); i++) {
            atmospehere += concertDto.ratings.get(i).concert_atmosphere;
            costumes += concertDto.ratings.get(i).artist_costumes;
            quality += concertDto.ratings.get(i).music_quality;
            stage += concertDto.ratings.get(i).stage_show;
        }

        int size = concertDto.ratings.size();
        if (size != 0) {
            atmospehere = atmospehere / size;
            costumes = costumes / size;
            quality = quality / size;
            stage = stage / size;
        }

        ratingBar.setProgress(atmospehere);

        ratingBar.setOnRatingBarChangeListener(new RatingBar.OnRatingBarChangeListener() {
            @Override
            public void onRatingChanged(RatingBar ratingBar, float rating, boolean fromUser) {
                if (ConcertListActivity.userDto.concerts.contains(concertDto.id) && fromUser) {
                    if (rateCount == 0) {
                        ratings.concert_atmosphere = (int) ratingBar.getRating();
                        rateDetails.setText("Rate for Artist Costumes");
                        ratingBar.setProgress(costumes);
                    } else if (rateCount == 1) {
                        ratings.artist_costumes = (int) ratingBar.getRating();
                        rateDetails.setText("Rate for Music Quality");
                        ratingBar.setProgress(quality);
                    } else if (rateCount == 2) {
                        ratings.music_quality = (int) ratingBar.getRating();
                        rateDetails.setText("Rate for Stage Show");
                        ratingBar.setProgress(stage);
                    } else if (rateCount == 3) {
                        ratings.stage_show = (int) ratingBar.getRating();
                        rateDetails.setText("Rate for Concert Atmosphere");
                        ratingBar.setProgress(atmospehere);
                    } else {
                        rateSubmit.setEnabled(true);
                        rateCount = -1;
                        rateDetails.setText("Rate for Concert Atmosphere");
                        ratingBar.setProgress(atmospehere);
                    }
                    rateCount++;
                }
            }
        });

        ratingBar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });
        rateSubmit.setEnabled(false);
        rateSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                rate();
            }
        });

        // Inflate the layout for this fragment
        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        mapView.onResume();
    }

    @Override
    public void onPause() {
        super.onPause();
        mapView.onPause();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        mapView.onDestroy();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        mapView.onLowMemory();
    }

    public void rate() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);
        Call<ConcertResponse> call = controller.rate(ratings, concertDto.id, map);
        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {
                rateDetails.setText("THANKS!");
                ConcertListActivity.getProfileInfo(getActivity());
                Toast.makeText(getActivity(), "RATED", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(getActivity(), "RATE ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void makeComment(String comment) {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);
        ConcertComment concertComment = new ConcertComment();
        concertComment.content = comment;


        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);

        Call<ConcertResponse> call = controller.makeComment(concertDto.id, concertComment, map);
        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {
                Toast.makeText(getActivity(), "COMMENTED", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(getActivity(), t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }


    public void attend() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);
        Call<Void> call = controller.attend(concertDto.id, map);
        call.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                attend.setText("UNATTEND");
                ConcertListActivity.getProfileInfo(getActivity());
                Toast.makeText(getActivity(), "ATTEND", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Toast.makeText(getActivity(), "ATTEND ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void unAttend() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);
        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Bearer " + LoginActivity.accessToken);
        Call<ConcertResponse> call = controller.unAttend(concertDto.id, map);
        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {
                attend.setText("ATTEND");
                ConcertListActivity.getProfileInfo(getActivity());
                Toast.makeText(getActivity(), "UNATTEND", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(getActivity(), "UNATTEND ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }


    public static byte[] serialize(Object obj) {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        ObjectOutput out = null;
        byte[] data = null;
        try {
            out = new ObjectOutputStream(bos);
            out.writeObject(obj);
            out.flush();
            data = bos.toByteArray();

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                bos.close();
            } catch (IOException ex) {
                // ignore close exception
            }
        }
        return data;
    }

    public static Object deserialize(byte[] data) {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        Object o = null;
        ObjectInput in = null;
        try {
            in = new ObjectInputStream(bis);
            o = in.readObject();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (in != null) {
                    in.close();
                }
            } catch (IOException ex) {
                // ignore close exception
            }
        }

        return o;
    }

    private class DownloadImageTask extends AsyncTask<String, Void, Bitmap> {
        ImageView bmImage;

        public DownloadImageTask(ImageView bmImage) {
            this.bmImage = bmImage;
        }

        protected Bitmap doInBackground(String... urls) {
            String urldisplay = urls[0];
            Bitmap mIcon11 = null;
            try {
                InputStream in = new java.net.URL(urldisplay).openStream();
                mIcon11 = BitmapFactory.decodeStream(in);
            } catch (Exception e) {
                Log.e("Error", e.getMessage());
                e.printStackTrace();
            }
            return mIcon11;
        }

        protected void onPostExecute(Bitmap result) {
            bmImage.setImageBitmap(result);
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        //TODO: fix after backend latlng update
        String[] latlng = concertDto.location.coordinates.split(" ");
        LatLng placeLocation = new LatLng(Double.valueOf(latlng[0]), Double.valueOf(latlng[1]));
        googleMap.addMarker(new MarkerOptions().position(placeLocation));
        googleMap.moveCamera(CameraUpdateFactory.newLatLng(placeLocation));
        googleMap.animateCamera(CameraUpdateFactory.zoomTo(14), 1000, null);
        mapView.onResume();
    }
}
