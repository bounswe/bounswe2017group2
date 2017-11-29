package com.swegroup2.lookingforconcerts;

import android.annotation.TargetApi;
import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.List;

/**
 * Created by Pınar on 28.11.2017.
 */

public class SearchListAdapter extends RecyclerView.Adapter<SearchListAdapter.SearchListAdapterViewHolder> {

    private final SearchListAdapterOnClickHandler mClickHandler;
    private List<ConcertDto> mConcertData;
    Context context;

    public SearchListAdapter(SearchListAdapterOnClickHandler clickHandler, Context context) {
        mClickHandler = clickHandler;
        this.context = context;
    }

    public void setConcertData(List<ConcertDto> concertData) {
        mConcertData = concertData;
        notifyDataSetChanged();
    }

    @Override
    public SearchListAdapterViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        Context context = parent.getContext();

        LayoutInflater inflater = LayoutInflater.from(context);

        View view = inflater.inflate(R.layout.search_list_item, parent, false);

        return new SearchListAdapterViewHolder(view);
    }

    @Override
    @TargetApi(24)
    public void onBindViewHolder(SearchListAdapterViewHolder holder, int position) {
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

    public class SearchListAdapterViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        public final TextView mConcertName;
       public final TextView mArtistName;
        public final TextView mConcertDate;


        public SearchListAdapterViewHolder(View view) {
            super(view);

            mConcertName = (TextView) view.findViewById(R.id.search_concert_name_tv);
            mArtistName = (TextView) view.findViewById(R.id.search_artist_name_tv);
            mConcertDate = (TextView) view.findViewById(R.id.search_date_tv);

            view.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            mClickHandler.onClick(mConcertData.get(getAdapterPosition()));
        }
    }

    public interface SearchListAdapterOnClickHandler {
        void onClick(ConcertDto concertDto);
    }
}

