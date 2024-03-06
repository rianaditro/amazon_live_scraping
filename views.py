from flask import Blueprint,render_template, request, redirect, url_for, send_file

from scrap import main

import pandas


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
