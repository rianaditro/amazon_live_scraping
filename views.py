from flask import Blueprint,render_template, request, redirect, url_for, send_file
from pathlib import Path

from scrap import main, download

import pandas

BASE_DIR = Path(__file__).resolve().parent


bp = Blueprint("main",__name__)

@bp.route('/')
def index():
    return render_template("homepage.html")

@bp.route('/scraping',methods=["GET","POST"])
def scraping():
    print(request.form)
    keyword = request.form["keyword"]
    print(keyword)
    items = main(keyword)
    # items = [{
    #     "product_name":"sample1",
    #     "product_url":"sample1",
    #     "image":"sample1",
    #     "price":"sample1",
    #     "rating":"sample1"},
    #     {
    #     "product_name":"sample2",
    #     "product_url":"sample2",
    #     "image":"sample2",
    #     "price":"sample2",
    #     "rating":"sample2"},
    #     {
    #     "product_name":"sample3",
    #     "product_url":"sample3",
    #     "image":"sample3",
    #     "price":"sample3",
    #     "rating":"sample3"}]
    
    df = pandas.DataFrame(items)
    df.to_csv("result.csv",index=False)
    df.to_excel("result.xlsx",index=False)

    return render_template("/scraping.html", items=items)

@bp.route('/download_csv')
def download_csv():
    return send_file("result.csv")

@bp.route('/download_excel')
def download_excel():
    return send_file("result.xlsx")
