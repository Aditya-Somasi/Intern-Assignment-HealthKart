
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from datetime import datetime
from PIL import Image



sys.path.append(os.path.abspath("utils"))
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{b64_data}"


from utils.io_helpers import load_all_data
from utils.filters import apply_filters
from utils.metrics import calculate_roas
from utils.pdf_export import export_insight_html
## to export the PDF locally, from utils.pdf_export_local import export_insight_pdf

# --- Theme Toggle ---
# theme = st.sidebar.radio("Theme", ["Light", "Dark"])
# def get_plot_theme():
#     return "plotly_dark" if theme == "Dark" else "plotly_white"

# if theme == "Dark":
#     st.markdown("""
#         <style>
#         .main {
#             background-color: #0e1117;
#             color: white;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# --- Display Logo and Title ---
logo_path = "assets/healthkart_logo.jpeg"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    image_base64 = get_base64_image("assets/healthkart_logo.jpeg")
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 16px;">
            <img src="{image_base64}" width="60" style="margin-bottom: 0;" />
            <h1 style="margin-bottom: 0;">HealthKart Influencer Campaign Dashboard</h1>
        </div>
        """, unsafe_allow_html=True)

else:
    st.title("HealthKart Influencer Campaign Dashboard")

st.markdown("Track your influencer campaigns across platforms, brands, and personas with insights into performance, ROI, and payouts.")

# --- Upload Section ---
st.subheader("Upload Your Campaign Data (Optional)")
tabs = st.tabs(["🧑‍🤝‍🧑 Influencers", "📢 Posts", "📦 Tracking", "💰 Payouts"])

uploaded_influencers = tabs[0].file_uploader("Upload influencers.csv", type="csv", key="inf")
uploaded_posts = tabs[1].file_uploader("Upload posts.csv", type="csv", key="post")
uploaded_tracking = tabs[2].file_uploader("Upload tracking_data.csv", type="csv", key="track")
uploaded_payouts = tabs[3].file_uploader("Upload payouts.csv", type="csv", key="pay")

def preview_csv(file, label, required_columns, save_name):
    if file:
        sample = pd.read_csv(file, nrows=1)
        file.seek(0)
        parse_date_cols = ["date"] if "date" in sample.columns else None
        df = pd.read_csv(file, parse_dates=parse_date_cols)

        if not all(col in df.columns for col in required_columns):
            st.error(f"{label} CSV is missing required columns: {required_columns}")
            return None

        st.success(f"{label} uploaded: {df.shape[0]} rows")
        st.dataframe(df.head(), use_container_width=True)

        with open(f"data/{save_name}", "wb") as f:
            f.write(file.getbuffer())

        return df
    return None

with tabs[0]:
    influencers = preview_csv(uploaded_influencers, "Influencers",
                              ["id", "name", "platform", "persona"], "influencers_uploaded.csv")
with tabs[1]:
    posts = preview_csv(uploaded_posts, "Posts",
                        ["influencer_id", "platform", "date", "reach"], "posts_uploaded.csv")
with tabs[2]:
    tracking = preview_csv(uploaded_tracking, "Tracking",
                           ["source", "campaign", "influencer_id", "date", "orders", "revenue"], "tracking_data_uploaded.csv")
with tabs[3]:
    payouts = preview_csv(uploaded_payouts, "Payouts",
                          ["influencer_id", "basis", "rate", "orders", "total_payout"], "payouts_uploaded.csv")

if not all([influencers is not None, posts is not None, tracking is not None, payouts is not None]):
    st.warning("Some files not uploaded — using default data from /data.")
    influencers, posts, tracking, payouts = load_all_data()

# --- Sidebar Filters ---
st.sidebar.title("Filter Campaigns")
platform_filter = st.sidebar.multiselect("Platform", influencers['platform'].unique(), default=list(influencers['platform'].unique()))
brand_filter = st.sidebar.multiselect("Brand", tracking['source'].unique(), default=list(tracking['source'].unique()))
persona_filter = st.sidebar.multiselect("Persona", influencers['persona'].unique(), default=list(influencers['persona'].unique()))
name_filter = st.sidebar.multiselect("Influencer Name", influencers['name'].unique(), default=list(influencers['name'].unique()))

min_date = tracking['date'].min()
max_date = tracking['date'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

filtered_influencers, filtered_posts, filtered_tracking, filtered_payouts = apply_filters(
    influencers, posts, tracking, payouts,
    platform_filter, brand_filter, persona_filter, date_range, name_filter
)

# --- Summary KPIs ---
st.subheader("📌 Campaign Summary Cards")
st.metric("Total Revenue", f"₹{int(filtered_tracking['revenue'].sum()):,}")
st.metric("Total Orders", int(filtered_tracking['orders'].sum()))
st.metric("Top Persona", filtered_influencers['persona'].mode()[0] if not filtered_influencers.empty else "N/A")

# --- Campaign Performance ---
st.subheader("📊 Campaign Revenue Summary")
campaign_summary = filtered_tracking.groupby("campaign").agg({"orders": "sum", "revenue": "sum"}).reset_index()
st.dataframe(campaign_summary, use_container_width=True)
fig = px.bar(campaign_summary, x="campaign", y="revenue", title="Revenue by Campaign", color="campaign", template="plotly")
st.plotly_chart(fig, use_container_width=True)

# --- ROAS ---
st.subheader("💡 ROI and Incremental ROAS")
top_influencers = calculate_roas(filtered_tracking, filtered_payouts, influencers)
st.dataframe(top_influencers.sort_values("roas", ascending=False), use_container_width=True)

# --- Top 5 ROAS Chart ---
st.subheader("🏆 Top 5 Influencers by ROAS")
top_5 = top_influencers.sort_values("roas", ascending=False).head(5)
fig_top = px.bar(top_5, x='name', y='roas', color='platform', text_auto='.2s', title='Top 5 ROAS Performers', template="plotly")
st.plotly_chart(fig_top, use_container_width=True)

# --- Heatmap ---
st.subheader("🔥 Persona vs Platform ROAS Heatmap")
heatmap_data = top_influencers.pivot_table(values="roas", index="persona", columns="platform", aggfunc="mean").fillna(0)
fig_heatmap = px.imshow(heatmap_data, text_auto=".2f", color_continuous_scale="blues", title="Avg ROAS by Persona & Platform")
st.plotly_chart(fig_heatmap, use_container_width=True)

# --- ROAS Trend ---
st.subheader("📈 ROAS Trend Over Time")
roas_by_month = filtered_tracking.copy()
roas_by_month["month"] = roas_by_month["date"].dt.to_period("M").dt.to_timestamp()
monthly = roas_by_month.groupby("month").agg({"revenue": "sum"}).reset_index()
fig_line = px.line(monthly, x="month", y="revenue", title="Monthly Revenue Trend", template=get_plot_theme())
st.plotly_chart(fig_line, use_container_width=True)

# --- Engagement ---
st.subheader("📣 Post Engagement Overview")
post_summary = filtered_posts.groupby("platform").agg({"reach": "mean", "likes": "mean", "comments": "mean"}).reset_index()
fig2 = px.bar(post_summary, x="platform", y=["reach", "likes", "comments"], barmode="group", template=get_plot_theme())
st.plotly_chart(fig2, use_container_width=True)

# --- Payouts ---
st.subheader("💰 Payout Breakdown")
payout_display = filtered_payouts.merge(influencers, left_on="influencer_id", right_on="id")
payout_display = payout_display[["name", "basis", "rate", "orders", "total_payout", "platform", "persona"]]
st.dataframe(payout_display.sort_values("total_payout", ascending=False), use_container_width=True)

# --- Exports ---
st.subheader("📤 Export Data")
st.download_button("Download Campaign Summary (CSV)", campaign_summary.to_csv(index=False), file_name="campaign_summary.csv")

st.subheader("📄 Download Insight Summary (HTML)")
if st.button("Generate Insight Summary"):
    html_path = export_insight_html(top_influencers, campaign_summary)
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.download_button("⬇️ Download Insight Summary (HTML)", html_content, file_name="healthkart_summary.html", mime="text/html")
    
    
## To export the PDF locally, uncomment the following lines:
    
# if st.button("📄 Download Insight Summary (PDF)"):
#     pdf_path = export_insight_pdf(top_influencers, campaign_summary)
#     if pdf_path:
#         with open(pdf_path, "rb") as f:
#             st.download_button("⬇️ Download PDF", f, file_name="healthkart_summary.pdf")
#     else:
#         st.error("PDF generation failed.")

# --- Footer ---
st.markdown("---")
st.markdown("*Built by Aditya using Streamlit with ❤️ for HealthKart*")
