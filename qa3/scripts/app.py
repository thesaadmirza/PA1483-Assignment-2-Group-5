import os

from flask import Flask, render_template

app = Flask(__name__)
app.jinja_options = {"cache_size": 0 if os.environ.get("CACHE") == "off" else 400}
app.config["TEMPLATES_AUTO_RELOAD"] = False


@app.get("/")
def index():
    return render_template("list.html", items=range(20))
