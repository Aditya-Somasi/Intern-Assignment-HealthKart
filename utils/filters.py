import pandas as pd

def apply_filters(influencers, posts, tracking, payouts,
                  platform_filter, brand_filter, persona_filter, date_range, name_filter):
    # Filter influencers by platform, persona, and name
    filtered_influencers = influencers[
        influencers["platform"].isin(platform_filter) &
        influencers["persona"].isin(persona_filter) &
        influencers["name"].isin(name_filter)
    ]

    # Filter by date range
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

    filtered_tracking = tracking[
        (tracking["source"].isin(brand_filter)) &
        (tracking["influencer_id"].isin(filtered_influencers["id"])) &
        (tracking["date"] >= start_date) &
        (tracking["date"] <= end_date)
    ]

    filtered_posts = posts[
        (posts["influencer_id"].isin(filtered_influencers["id"])) &
        (posts["date"] >= start_date) &
        (posts["date"] <= end_date)
    ]

    filtered_payouts = payouts[payouts["influencer_id"].isin(filtered_influencers["id"])]

    return filtered_influencers, filtered_posts, filtered_tracking, filtered_payouts
