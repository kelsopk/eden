from portal import app
from flask.templating import render_template

@app.route("/")
def index():
    return render_template('base.html')