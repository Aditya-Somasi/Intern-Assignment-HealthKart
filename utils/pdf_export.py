import pdfkit
from jinja2 import Environment, FileSystemLoader
import datetime
import os



config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def export_insight_pdf(top_influencers_df, campaign_summary_df, output_path="insights/summary.pdf"):
    # Convert to dict
    top_influencers = top_influencers_df.head(5).to_dict(orient="records")
    campaign_summary = campaign_summary_df.to_dict(orient="records")

    # Load HTML template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("insight_template.html")
    html = template.render(
        top_influencers=top_influencers,
        campaign_summary=campaign_summary,
        date=datetime.datetime.today().strftime("%Y-%m-%d")
    )

    os.makedirs("insights", exist_ok=True)
    pdfkit.from_string(html, output_path, configuration=config)
    return output_path
