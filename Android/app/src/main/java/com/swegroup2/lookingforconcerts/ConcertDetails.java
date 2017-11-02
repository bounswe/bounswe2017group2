package com.swegroup2.lookingforconcerts;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ConcertDetails extends Fragment {

    private static ConcertDto concertDto;
    TextView name;
    TextView artistName;
    TextView date;
    TextView description;
    TextView minPrice;
    TextView maxPrice;
    TextView location;
    TextView comments;
    EditText commentText;

    Button comment;
    Button back;


    public ConcertDetails() {
        // Required empty public constructor
    }

    public static ConcertDetails newInstance(ConcertDto concertDto) {
        ConcertDetails fragment = new ConcertDetails();
        Bundle args = new Bundle();
        args.putInt("id", concertDto.id);
        args.putString("name", concertDto.name);
        args.putString("artistName", concertDto.artistName);
        args.putString("date", concertDto.date);
        args.putString("description", concertDto.description);
        args.putInt("minPrice", concertDto.minPrice);
        args.putInt("maxPrice", concertDto.maxPrice);
        args.putString("venue", concertDto.location.venue);
        args.putString("coordinates", concertDto.location.coordinates);
        args.putByteArray("comments",serialize(concertDto.comments));


        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            concertDto = new ConcertDto();
            concertDto.id = getArguments().getInt("id");
            concertDto.name = getArguments().getString("name");
            concertDto.artistName = getArguments().getString("artistName");
            concertDto.date = getArguments().getString("date");
            concertDto.description = getArguments().getString("description");
            concertDto.minPrice = getArguments().getInt("minPrice");
            concertDto.maxPrice = getArguments().getInt("maxPrice");

            ConcertLocation loc = new ConcertLocation();
            loc.coordinates = getArguments().getString("coordinates");
            loc.venue = getArguments().getString("venue");
            concertDto.location = loc;


            concertDto.comments= (List<ConcertComment>) deserialize((getArguments().getByteArray("comments")));

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
        comments = (TextView) view.findViewById(R.id.comments);
        back = (Button) view.findViewById(R.id.back_to_list);
        comment = (Button) view.findViewById(R.id.comment);
        commentText= (EditText) view.findViewById(R.id.comment_edittext);

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


        name.setText("Name: " + concertDto.name);
        artistName.setText("Artist Name: " + concertDto.artistName);
        date.setText("Date: " + concertDto.date);
        description.setText("Description: " + concertDto.description);
        minPrice.setText("Min Price: " + concertDto.minPrice);
        maxPrice.setText("Max Price: " + concertDto.maxPrice);
        location.setText("Location: " + concertDto.location.venue + " " + concertDto.location.coordinates);
        String allComments="Comments: \n";

        for(int i=0;i<concertDto.comments.size();i++){
            allComments+=concertDto.comments.get(i).content+"\n";
        }

        comments.setText(allComments);

        // Inflate the layout for this fragment
        return view;
    }

    public void makeComment(String comment){
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://34.210.127.92:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        RestInterfaceController controller = retrofit.create(RestInterfaceController.class);
        ConcertComment concertComment=new ConcertComment();
        concertComment.content=comment;

        String token="";
        try {
            JSONObject jsonObj = new JSONObject(getActivity().getIntent().getStringExtra("json"));
            token = jsonObj.getString("token");
            Log.v("myTag","tokenL: " + jsonObj.getString("token"));


        } catch (JSONException e) {
            e.printStackTrace();
        }

        Map<String, String> map = new HashMap<>();
        map.put("Authorization", "Token " + token);

        Call<ConcertResponse> call = controller.makeComment(concertDto.id,concertComment,map);
        call.enqueue(new Callback<ConcertResponse>() {
            @Override
            public void onResponse(Call<ConcertResponse> call, Response<ConcertResponse> response) {
                Toast.makeText(getActivity(), "COMMENTED", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<ConcertResponse> call, Throwable t) {
                Toast.makeText(getActivity(), "ERROR", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public static byte[] serialize(Object obj){
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        ObjectOutput out = null;
        byte[] data=null;
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

    public static Object deserialize(byte[] data){
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        Object o=null;
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
}
