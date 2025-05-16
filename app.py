from flask import Flask, render_template, request
import pandas as pd
from textblob import TextBlob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reviews = None
    sentiment_counts = None
    chart_path = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_csv(file)
            reviews = df["review"].tolist()

            # 感情分析
            sentiments = []
            for review in reviews:
                blob = TextBlob(review)
                polarity = blob.sentiment.polarity
                if polarity > 0.1:
                    sentiments.append("ポジティブ")
                elif polarity < -0.1:
                    sentiments.append("ネガティブ")
                else:
                    sentiments.append("ニュートラル")
            
            # 集計
            sentiment_counts = pd.Series(sentiments).value_counts()

            # 円グラフ描画
            plt.figure(figsize=(5,5))
            sentiment_counts.plot.pie(autopct='%1.1f%%', startangle=90)
            chart_path = os.path.join("static", "sentiment_pie.png")
            plt.savefig(chart_path)
            plt.close()

    return render_template("index.html", reviews=reviews, chart_path=chart_path)

if __name__ == "__main__":
    app.run(debug=True)
