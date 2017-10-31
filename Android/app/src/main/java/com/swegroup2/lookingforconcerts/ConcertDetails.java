package com.swegroup2.lookingforconcerts;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

public class ConcertDetails extends Fragment {

    private static ConcertDto concertDto;
    TextView name;
    TextView artistName;
    TextView date;
    TextView description;
    TextView minPrice;
    TextView maxPrice;
    TextView location;
    Button back;


    public ConcertDetails() {
        // Required empty public constructor
    }

    public static ConcertDetails newInstance(ConcertDto concertDto) {
        ConcertDetails fragment = new ConcertDetails();
        Bundle args = new Bundle();
        args.putString("name", concertDto.name);
        args.putString("artistName", concertDto.artistName);
        args.putString("date", concertDto.date);
        args.putString("description", concertDto.description);
        args.putInt("minPrice", concertDto.minPrice);
        args.putInt("maxPrice", concertDto.maxPrice);
        args.putString("venue", concertDto.location.venue);
        args.putString("coordinates", concertDto.location.coordinates);

        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            concertDto = new ConcertDto();
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

        }

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_concert_details, container, false);
        name = (TextView) view.findViewById(R.id.name);
        artistName = (TextView) view.findViewById(R.id.artistName);
        date = (TextView) view.findViewById(R.id.date);
        description = (TextView) view.findViewById(R.id.description);
        minPrice = (TextView) view.findViewById(R.id.minPrice);
        maxPrice = (TextView) view.findViewById(R.id.maxPrice);
        location = (TextView) view.findViewById(R.id.location);
        back = (Button) view.findViewById(R.id.back_to_list);

        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getFragmentManager().popBackStack();
            }
        });


        name.setText("Name: " + concertDto.name);
        artistName.setText("Artist Name: " + concertDto.artistName);
        date.setText("Date: " + concertDto.date);
        description.setText("Description: " + concertDto.description);
        minPrice.setText("Min Price: " + concertDto.minPrice);
        maxPrice.setText("Max Price: " + concertDto.maxPrice);
        location.setText("Location: " + concertDto.location.venue + " " + concertDto.location.coordinates);

        // Inflate the layout for this fragment
        return view;
    }
}
