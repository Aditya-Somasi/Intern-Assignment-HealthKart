from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os
import datetime

def export_insight_pdf(top_influencers_df, campaign_summary_df, output_path="insights/summary.pdf"):
    os.makedirs("insights", exist_ok=True)

    # Convert to dict
    top_influencers = top_influencers_df.head(5).to_dict(orient="records")
    campaign_summary = campaign_summary_df.to_dict(orient="records")

    # Load Jinja2 Template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("insight_template.html")
    html = template.render(
        top_influencers=top_influencers,
        campaign_summary=campaign_summary,
        date=datetime.datetime.today().strftime("%Y-%m-%d")
    )

    # Render HTML to PDF using xhtml2pdf
    with open(output_path, "w+b") as f:
        pisa.CreatePDF(html, dest=f)

    return output_path
