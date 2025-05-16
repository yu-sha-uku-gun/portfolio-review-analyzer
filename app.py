from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reviews = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_csv(file)
            reviews = df["review"].tolist()
    return render_template("index.html", reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True)
