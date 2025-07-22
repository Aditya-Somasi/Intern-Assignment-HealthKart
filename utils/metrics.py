import pandas as pd

def calculate_roas(tracking_df, payouts_df, influencers_df):
    merged = pd.merge(tracking_df, payouts_df, on="influencer_id", how="inner")
    merged["roas"] = merged["revenue"] / (merged["total_payout"] + 1)  # avoid div by 0
    summary = merged.groupby("influencer_id").agg({
        "revenue": "sum",
        "total_payout": "sum",
        "roas": "mean"
    }).reset_index()
    enriched = pd.merge(summary, influencers_df, left_on="influencer_id", right_on="id")
    return enriched[["name", "platform", "persona", "revenue", "total_payout", "roas"]]
