from jinja2 import Environment, FileSystemLoader
import os
import datetime

def export_insight_html(top_influencers_df, campaign_summary_df, output_path="insights/summary.html"):
    os.makedirs("insights", exist_ok=True)

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

    # Save HTML to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
