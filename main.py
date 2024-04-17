from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import pandas as pd
import yfinance as yf

DJIA = ["AAPL", "MSFT", "UNH", "JNJ", "V", "WMT", "JPM", "PG", "CVX", "HD",
        "MRK", "KO", "CSCO", "MCD", "NKE", "DIS", "VZ", "AMGN", "HON", "IBM",
        "CRM", "GS", "CAT", "INTC", "AXP", "BA", "MMM", "TRV", "DD", "WBA"]


def get_stock(list1, start_time, end_time):
    df = pd.DataFrame()
    for i in range(len(list1)):
        data = yf.download(list1[i], start=start_time, end=end_time)
        price = data["Close"]
        df = pd.concat([df, price], axis=1)
    df.columns = list1
    df = df.reset_index()
    df = df.rename(columns={"index": "Date"})
    return df


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    pathname = "./data/"
    filename = "DJIA.csv"
    namefile = pathname+filename
    if request.method == "POST":
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        stock = request.form["snm"]
        if stock == "DJIA":
            stock_list = DJIA
        else:
            stock_list = stock.split(" ")
        file = get_stock(stock_list, start_time, end_time)
        file.to_csv(namefile, index=False)
        return send_from_directory('data', filename, as_attachment=True)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
