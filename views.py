from flask import Blueprint,render_template, request, redirect, url_for
from scrap import main


bp = Blueprint("main",__name__)

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/scraping',methods=["GET","POST"])
def scraping():
    keyword = request.form["keyword"]
    items = main(keyword)

    return render_template("/scraping.html", items=items)


