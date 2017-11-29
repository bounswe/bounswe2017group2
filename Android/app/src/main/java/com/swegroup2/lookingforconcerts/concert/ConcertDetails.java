package com.swegroup2.lookingforconcerts.concert;

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

import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.RestInterfaceController;
import com.swegroup2.lookingforconcerts.login.LoginActivity;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
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
    public static Button attend;

    Button comment;
    Button back;


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
        comments = (TextView) view.findViewById(R.id.comments);
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

        if (ConcertListActivity.userDto.concerts.contains(concertDto.id)) {
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
        date.setText("Date: " + concertDto.date);
        description.setText("Description: " + concertDto.description);
        minPrice.setText("Min Price: " + concertDto.minPrice);
        maxPrice.setText("Max Price: " + concertDto.maxPrice);
        location.setText("Location: " + concertDto.location.venue + " " + concertDto.location.coordinates);
        String allComments = "Comments: \n";

        for (int i = 0; i < concertDto.comments.size(); i++) {
            allComments += concertDto.comments.get(i).content + "\n";
        }

        comments.setText(allComments);


        // Inflate the layout for this fragment
        return view;
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
                Log.d("FS", t.getMessage());
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
}
