package com.swegroup2.lookingforconcerts.adapters;

import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.swegroup2.lookingforconcerts.R;
import com.swegroup2.lookingforconcerts.concert.Tag;

import java.util.List;

/**
 * Created by elifguler on 10.12.2017.
 */

public class TagListAdapter extends RecyclerView.Adapter<TagListAdapter
        .TagListAdapterViewHolder>{
    private final TagListAdapterOnClickHandler mClickHandler;
    private List<Tag> mTagData;
    Context context;

    public TagListAdapter(TagListAdapterOnClickHandler clickHandler, Context context) {
        mClickHandler = clickHandler;
        this.context = context;
    }

    public void setTagData(List<Tag> tagData) {
        mTagData = tagData;
        notifyDataSetChanged();
    }

    @Override
    public TagListAdapterViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        Context context = parent.getContext();

        LayoutInflater inflater = LayoutInflater.from(context);

        View view = inflater.inflate(R.layout.tag_list_item, parent, false);

        return new TagListAdapterViewHolder(view);
    }

    @Override
    public void onBindViewHolder(TagListAdapterViewHolder holder, int position) {
        Tag tag = mTagData.get(position);
        holder.mTagValue.setText(tag.value);
        holder.mTagContext.setText(tag.context);
    }

    @Override
    public int getItemCount() {
        if (mTagData == null) {
            return 0;
        }

        return mTagData.size();
    }

    public class TagListAdapterViewHolder extends RecyclerView.ViewHolder implements View
            .OnClickListener {
        public final TextView mTagValue;
        public final TextView mTagContext;


        public TagListAdapterViewHolder(View view) {
            super(view);

            mTagValue = (TextView) view.findViewById(R.id.tag_list_value_tv);
            mTagContext = (TextView) view.findViewById(R.id.tag_list_context_tv);

            view.setOnClickListener(this);
        }

        @Override
        public void onClick(View view) {
            mClickHandler.onClick(mTagData.get(getAdapterPosition()));
        }
    }

    public interface TagListAdapterOnClickHandler {
        void onClick(Tag tag);
    }
}
