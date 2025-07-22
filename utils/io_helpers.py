import pandas as pd

def load_all_data():
    influencers = pd.read_csv("data/influencers.csv")
    posts = pd.read_csv("data/posts.csv", parse_dates=['date'])
    tracking = pd.read_csv("data/tracking_data.csv", parse_dates=['date'])
    payouts = pd.read_csv("data/payouts.csv")
    return influencers, posts, tracking, payouts
