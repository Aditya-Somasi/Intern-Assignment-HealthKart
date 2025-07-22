# 💼 HealthKart Influencer Campaign Dashboard

An interactive Streamlit dashboard for tracking and analyzing the ROI of influencer campaigns across platforms and brands.  
You can upload your own data or use the simulated datasets provided.



## 📌 Features

✅ **Data Simulation** (via Faker in `scripts/`)  
✅ **CSV Upload Support** (load your own influencer, post, tracking, and payout data)  
✅ **Filtering** by Platform, Brand, Persona, and Date Range  
✅ **Insights**:
- Campaign revenue summary
- ROAS & incremental ROI calculations
- Top 5 influencers bar chart
- Persona vs Platform ROAS heatmap
- Post engagement overview
- Payout tracking

✅ **Export Options**:
- Download campaign summary as CSV
- Download insights as a summary PDF

✅ **Modular Code** (organized under `utils/` and `templates/`)  

---



## ⚙️ Setup Instructions

### 1. Clone or download the project

### 2. Install Python dependencies
pip install -r requirements.txt

### 3. Generate Sample Data (Optional)
python scripts/generate_data.py

### 4. Run the Dashboard
streamlit run main.py

---
### 📁 Upload Custom Data
You can upload your own CSV files directly from the sidebar:

-> Influencers CSV
Columns: id, name, category, gender, follower_count, platform, persona

-> Posts CSV
Columns: influencer_id, platform, date, url, caption, reach, likes, comments

-> Tracking Data CSV
Columns: source, campaign, influencer_id, user_id, product, date, orders, revenue

-> Payouts CSV
Columns: influencer_id, basis, rate, orders, total_payout

If no files are uploaded, default data from the /data folder is used.

---
### 🖨️ Export Options
### ✅ 1. HTML Summary (Deployed Online)
Fully supported in Streamlit Cloud:

Click "Generate Insight Summary"

Preview the report inside the app

Download as .html

Use Print to PDF from your browser to export as PDF

### 🖥️ 2. PDF Summary (Offline Use Only)
If you're running locally, enable full PDF generation by uncommenting the lines in main.py.

### 📌 Note: PDF export with xhtml2pdf is not supported on Streamlit Cloud.

--- 

### 📁 Folder Structure
.
├── assets/
│   └── healthkart_logo.jpeg
├── data/
│   └── [sample or uploaded CSVs]
├── insights/
│   └── [exported PDFs or HTML summaries]
├── templates/
│   └── insight_template.html
├── utils/
│   ├── filters.py
│   ├── io_helpers.py
│   ├── metrics.py
│   ├── pdf_export.py              # HTML Export (Cloud-safe)
│   └── pdf_export_local.py        # Local PDF Export (Offline use only)
└── main.py


---
### 📄 Sample Outputs

-> 📊 Campaign Summary: Revenue & Orders per campaign

-> 💰 Payout Report: Influencer-wise payout tracking

-> 📈 ROAS Insights: ROAS + Top 5 influencer bar chart

-> 🔥 Persona Heatmap: Average ROAS by persona & platform

-> 📄 Insight PDF: Downloadable 1-page summary

---

### 🧠 Assumptions

-> Influencers may be paid per post or per order

-> ROAS = Total Revenue / Total Payout (incremental assumed through filters)

-> Revenue + post engagement are simulated using realistic ranges

---

#### 🧑‍💻 Built With

-> Python

-> Streamlit

-> Pandas

-> Plotly

-> Faker

-> xhtml2pdf (for offline user) + jinja2

---
🙌 Author
Made by Aditya with Streamlit, Plotly, Pandas & ❤️



