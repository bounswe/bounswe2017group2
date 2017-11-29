package com.swegroup2.lookingforconcerts.search;

import android.annotation.TargetApi;
import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;
import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.concert.Artist;
import com.swegroup2.lookingforconcerts.concert.Image;

import java.util.List;

/**
 * Created by elifguler on 16.11.2017.
 */

public class ArtistListAdapter extends RecyclerView.Adapter<ArtistListAdapter
        .ArtistListAdapterViewHolder> {
    private final ArtistListAdapterOnClickHandler mClickHandler;
    private List<Artist> mArtistData;
    Context context;

    public ArtistListAdapter(ArtistListAdapterOnClickHandler clickHandler, Context context) {
        mClickHandler = clickHandler;
        this.context = context;
    }

    public void setArtistData(List<Artist> artistData) {
        mArtistData = artistData;
        notifyDataSetChanged();
    }

    @Override
    public ArtistListAdapterViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        Context context = parent.getContext();

        LayoutInflater inflater = LayoutInflater.from(context);

        View view = inflater.inflate(R.layout.artist_list_item, parent, false);

        return new ArtistListAdapterViewHolder(view);
    }

    @Override
    @TargetApi(24)
    public void onBindViewHolder(ArtistListAdapterViewHolder holder, int position) {
        Artist artist = mArtistData.get(position);

        if (artist != null) {
            holder.mArtistName.setText(artist.name);
            List<Image> images = mArtistData.get(position).images;
            if (images != null && !images.isEmpty())
                Picasso.with(context).load(mArtistData.get(position).images.get(0).url).into(holder.mArtistPicture);
        }
    }

    @Override
    public int getItemCount() {
        if (mArtistData == null) {
            return 0;
        }

        return mArtistData.size();
    }

    public class ArtistListAdapterViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        public final TextView mArtistName;
        public final ImageView mArtistPicture;


        public ArtistListAdapterViewHolder(View view) {
            super(view);

            mArtistName = (TextView) view.findViewById(R.id.artist_list_name_tv);
            mArtistPicture = (ImageView) view.findViewById(R.id.artist_list_image);

            view.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            mClickHandler.onClick(mArtistData.get(getAdapterPosition()));
        }
    }

    public interface ArtistListAdapterOnClickHandler {
        void onClick(Artist artist);
    }
}
