from flask import Flask,Blueprint, render_template,request
import re
from scraper import get_mp3_url

app =Flask(__name__)
downloader_bp = Blueprint("downloader",__name__)
@downloader_bp.route("/", methods = ["GET","POST"])
def index():
    if request.method == "POST":
        golha_url = request.form.get("golha_url","").strip()
        if not golha_url:
            return render_template("index.html", error="Please enter a Golha Url :)")
        if not re.match(r"https?://(www\.)?golha\.co\.uk/en/programme/\d+", golha_url, re.IGNORECASE):
            return render_template("index.html", error="Invalid URL! Must be like https://www.golha.co.uk/en/programme/465", golha_url=golha_url)
        mp3_url, error = get_mp3_url(golha_url)
        if mp3_url:
            return render_template("index.html", mp3_url=mp3_url, golha_url=golha_url)
        return render_template("index.html", error=error, golha_url=golha_url)
    
    # GET: Show empty form
    return "/index.html"

# Register Blueprint
app.register_blueprint(downloader_bp)

if __name__ == "__main__":
    app.run( host='0.0.0.0', port=8000,debug=True)


