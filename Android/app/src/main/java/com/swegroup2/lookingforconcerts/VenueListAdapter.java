package com.swegroup2.lookingforconcerts;

import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.List;

/**
 * Created by elifguler on 26.11.2017.
 */

public class VenueListAdapter extends RecyclerView.Adapter<VenueListAdapter
        .VenueListAdapterViewHolder>{

    private final VenueListAdapterOnClickHandler mClickHandler;
    private List<ConcertLocation> mVenueData;
    Context context;

    public VenueListAdapter(VenueListAdapterOnClickHandler clickHandler, Context context) {
        mClickHandler = clickHandler;
        this.context = context;
    }

    public void setVenueData(List<ConcertLocation> venueData) {
        mVenueData = venueData;
        notifyDataSetChanged();
    }

    @Override
    public VenueListAdapterViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        Context context = parent.getContext();

        LayoutInflater inflater = LayoutInflater.from(context);

        View view = inflater.inflate(R.layout.venue_list_item, parent, false);

        return new VenueListAdapterViewHolder(view);
    }

    @Override
    public void onBindViewHolder(VenueListAdapterViewHolder holder, int position) {
        ConcertLocation location = mVenueData.get(position);
        holder.mVenueName.setText(location.venue);
        holder.mVenueAddress.setText(location.address);
    }

    @Override
    public int getItemCount() {
        if (mVenueData == null) {
            return 0;
        }

        return mVenueData.size();
    }

    public class VenueListAdapterViewHolder extends RecyclerView.ViewHolder implements View
            .OnClickListener {
        public final TextView mVenueName;
        public final TextView mVenueAddress;


        public VenueListAdapterViewHolder(View view) {
            super(view);

            mVenueName = (TextView) view.findViewById(R.id.venue_list_venue);
            mVenueAddress = (TextView) view.findViewById(R.id.venue_list_address);

            view.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            mClickHandler.onClick(mVenueData.get(getAdapterPosition()));
        }
    }

    public interface VenueListAdapterOnClickHandler {
        void onClick(ConcertLocation location);
    }
}
