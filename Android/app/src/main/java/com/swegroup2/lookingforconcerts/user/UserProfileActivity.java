package com.swegroup2.lookingforconcerts.user;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ListView;
import android.widget.TextView;

import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.concert.ConcertDto;
import com.swegroup2.lookingforconcerts.concert.ConcertListActivity;
import com.swegroup2.lookingforconcerts.login.LoginActivity;

import java.util.ArrayList;
import java.util.List;

public class UserProfileActivity extends AppCompatActivity {

    List<ConcertDto> pastConcerts = new ArrayList<>();
    List<ConcertDto> futureConcerts = new ArrayList<>();
    String today = "";

    ConcertHistoryListAdapter concertHistoryListAdapter;
    FutureConcertListAdapter futureConcertListAdapter;
    ListView concertHistory;
    TextView nameSurname;
    TextView birthDate;
    TextView dateJoined;
    TextView followers;
    TextView following;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_profile);
        fillConcerts(ConcertListActivity.userDto.concerts);
        concertHistory = (ListView) findViewById(R.id.concert_history);
        concertHistoryListAdapter = new ConcertHistoryListAdapter(this, pastConcerts);
        concertHistory.setAdapter(concertHistoryListAdapter);

        nameSurname = (TextView) findViewById(R.id.name_surname);
        nameSurname.setText(ConcertListActivity.userDto.firstName + " " + ConcertListActivity.userDto.lastName);

        birthDate = (TextView) findViewById(R.id.birth_date);
        birthDate.setText("Birth Date: " + ConcertListActivity.userDto.birthDate);

        dateJoined = (TextView) findViewById(R.id.date_joined);
        dateJoined.setText("Date Joined: " + ConcertListActivity.userDto.dateJoined);

        followers = (TextView) findViewById(R.id.followers);
        followers.setText("Followers: " + ConcertListActivity.userDto.followers.size());

        following = (TextView) findViewById(R.id.following);
        following.setText("Following: " + ConcertListActivity.userDto.following.size());


    }

    private void fillConcerts(List<Integer> userConcerts) {
        for (int userConcertId : userConcerts) {
            for (ConcertDto concert : ConcertListActivity.concerts) {
                if (concert.id == userConcertId) {
                    pastConcerts.add(concert);
                }
            }
        }
    }
}
