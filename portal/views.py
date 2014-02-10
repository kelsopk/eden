from portal import app

@app.route("/")
def index():
    return "List"