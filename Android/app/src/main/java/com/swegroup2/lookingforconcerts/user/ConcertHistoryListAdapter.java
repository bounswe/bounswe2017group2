package com.swegroup2.lookingforconcerts.user;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.concert.ConcertDto;

import java.util.List;

/**
 * Created by furkan on 27.11.2017.
 */

public class ConcertHistoryListAdapter extends BaseAdapter {
    Context context;
    List<ConcertDto> pastConcerts;

    public ConcertHistoryListAdapter(Context context, List<ConcertDto> pastConcerts) {
        this.context = context;
        this.pastConcerts = pastConcerts;
    }


    @Override
    public int getCount() {
        return pastConcerts.size();
    }

    @Override
    public Object getItem(int position) {
        return pastConcerts.get(position);
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {

        ViewHolder holder;
        if (convertView == null) {
            LayoutInflater layoutInflater = (LayoutInflater) this.context.getSystemService("layout_inflater");
            convertView = layoutInflater.inflate(R.layout.user_concert_list_item, parent, false);
            holder = new ViewHolder();
            holder.concertName = (TextView) convertView.findViewById(R.id.user_concert_name);
            holder.artistName = (TextView) convertView.findViewById(R.id.user_artist_name);
            holder.date = (TextView) convertView.findViewById(R.id.user_date);
            convertView.setTag(holder);
        } else {
            holder = (ViewHolder) convertView.getTag();
        }


        if (pastConcerts.get(position).artist != null) {
            holder.artistName.setText(pastConcerts.get(position).artist.name);
        }
        holder.concertName.setText(pastConcerts.get(position).name);
        if (pastConcerts.get(position).date != null) {
            holder.date.setText(pastConcerts.get(position).date);
        }


        return convertView;
    }

    private static class ViewHolder {
        public TextView concertName;
        public TextView artistName;
        public TextView date;


        private ViewHolder() {
        }
    }
}

