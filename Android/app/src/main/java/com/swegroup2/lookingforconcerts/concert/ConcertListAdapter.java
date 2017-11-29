package com.swegroup2.lookingforconcerts.concert;

import android.annotation.TargetApi;
import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.swegroup2.lookingforconcerts.R;

import java.util.List;

/**
 * Created by elifguler on 23.10.2017.
 */

public class ConcertListAdapter extends RecyclerView.Adapter<ConcertListAdapter.ConcertListAdapterViewHolder> {

    private final ConcertListAdapterOnClickHandler mClickHandler;
    private List<ConcertDto> mConcertData;

    public ConcertListAdapter(ConcertListAdapterOnClickHandler clickHandler) {
        mClickHandler = clickHandler;
    }

    public void setConcertData(List<ConcertDto> concertData) {
        mConcertData = concertData;
        notifyDataSetChanged();
    }

    @Override
    public ConcertListAdapterViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        Context context = parent.getContext();

        LayoutInflater inflater = LayoutInflater.from(context);

        View view = inflater.inflate(R.layout.list_item, parent, false);

        return new ConcertListAdapterViewHolder(view);
    }

    @Override
    @TargetApi(24)
    public void onBindViewHolder(ConcertListAdapterViewHolder holder, int position) {
        ConcertDto concert = mConcertData.get(position);

        if (concert.artist != null) {
            holder.mArtistName.setText(concert.artist.name);
        }
        holder.mConcertName.setText(concert.name);
        holder.mConcertDate.setText(concert.date);
    }

    @Override
    public int getItemCount() {
        if (mConcertData == null) {
            return 0;
        }

        return mConcertData.size();
    }

    public class ConcertListAdapterViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        public final TextView mConcertName;
        public final TextView mArtistName;
        public final TextView mConcertDate;


        public ConcertListAdapterViewHolder(View view) {
            super(view);

            mConcertName = (TextView) view.findViewById(R.id.concert_name_tv);
            mArtistName = (TextView) view.findViewById(R.id.artist_name_tv);
            mConcertDate = (TextView) view.findViewById(R.id.date_tv);

            view.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            mClickHandler.onClick(mConcertData.get(getAdapterPosition()));
        }
    }

    public interface ConcertListAdapterOnClickHandler {
        void onClick(ConcertDto concertDto);
    }
}

