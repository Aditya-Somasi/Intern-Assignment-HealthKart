import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)
np.random.seed(42)

# Define platforms and brands
platforms = ["Instagram", "YouTube", "Twitter"]
brands = ["MuscleBlaze", "HKVitals", "Gritzo"]
categories = ["Fitness", "Nutrition", "Lifestyle", "Bodybuilding", "Vitamins"]

# Influencer personas
personas = ["Athlete", "Gym Trainer", "Nutritionist", "Fitness Blogger"]

# Generate Influencers
def generate_influencers(n=300):
    influencers = []
    for i in range(1, n + 1):
        gender = random.choice(["Male", "Female"])
        platform = random.choice(platforms)
        category = random.choice(categories)
        followers = np.random.randint(5000, 200000)
        persona = random.choice(personas)
        influencers.append({
            "id": i,
            "name": fake.name(),
            "category": category,
            "gender": gender,
            "follower_count": followers,
            "platform": platform,
            "persona": persona
        })
    return pd.DataFrame(influencers)

# Generate Posts
def generate_posts(influencers_df, n=1000):
    posts = []
    for _ in range(n):
        influencer = influencers_df.sample(1).iloc[0]
        date = fake.date_between(start_date='-90d', end_date='today')
        reach = int(influencer['follower_count'] * np.random.uniform(0.3, 1.1))
        posts.append({
            "influencer_id": influencer['id'],
            "platform": influencer['platform'],
            "date": date,
            "url": fake.url(),
            "caption": fake.sentence(),
            "reach": reach,
            "likes": int(reach * random.uniform(0.05, 0.2)),
            "comments": int(reach * random.uniform(0.01, 0.05))
        })
    return pd.DataFrame(posts)

# Generate Tracking Data
def generate_tracking_data(influencers_df, n=3000):
    tracking = []
    for _ in range(n):
        influencer = influencers_df.sample(1).iloc[0]
        brand = random.choice(brands)
        user_id = fake.uuid4()
        product = brand + " Product " + str(random.randint(1, 10))
        date = fake.date_between(start_date='-60d', end_date='today')
        orders = np.random.randint(1, 5)
        revenue = round(orders * np.random.uniform(500, 2000), 2)
        tracking.append({
            "source": brand,
            "campaign": f"{brand}_Campaign_{random.randint(1, 5)}",
            "influencer_id": influencer['id'],
            "user_id": user_id,
            "product": product,
            "date": date,
            "orders": orders,
            "revenue": revenue
        })
    return pd.DataFrame(tracking)

# Generate Payouts
def generate_payouts(influencers_df):
    payouts = []
    for _, row in influencers_df.iterrows():
        basis = random.choice(["post", "order"])
        rate = round(random.uniform(200, 1000), 2) if basis == "post" else round(random.uniform(100, 500), 2)
        orders = np.random.randint(10, 100)
        total = round(orders * rate, 2) if basis == "order" else round(rate * np.random.randint(5, 20), 2)
        payouts.append({
            "influencer_id": row["id"],
            "basis": basis,
            "rate": rate,
            "orders": orders,
            "total_payout": total
        })
    return pd.DataFrame(payouts)

# Save to CSV
def save_data():
    os.makedirs("data", exist_ok=True)

    influencers_df = generate_influencers()
    influencers_df.to_csv("data/influencers.csv", index=False)

    posts_df = generate_posts(influencers_df)
    posts_df.to_csv("data/posts.csv", index=False)

    tracking_df = generate_tracking_data(influencers_df)
    tracking_df.to_csv("data/tracking_data.csv", index=False)

    payouts_df = generate_payouts(influencers_df)
    payouts_df.to_csv("data/payouts.csv", index=False)

    print("✅ All datasets generated successfully in data folder!")

if __name__ == "__main__":
    save_data()
