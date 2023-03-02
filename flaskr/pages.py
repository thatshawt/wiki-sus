from flask import render_template, send_file, request
from flaskr import backend
from google.cloud import storage

import tempfile

backend = backend.Backend()

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html")

    @app.route("/upload", methods=['GET','POST'])
    def upload():
        if request.method == 'GET':
            return render_template("upload.html")
        elif request.method == 'POST':
            wikiname = request.form['wikiname']

            with tempfile.NamedTemporaryFile() as tmp:
                f = request.files['file']
                f.save(tmp)
                tmp.seek(0)
                backend.upload(wikiname, tmp)
                
                return render_template("upload.html",
                    link="/pages/" + wikiname)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/pages")
    def pages():
        pages = []
        page_names = backend.get_all_page_names()
        for page_name in page_names:
            pages.append({
                "name": page_name,
                "link": "/pages/" + page_name + "/"
            })
        return render_template("pages.html", pages=pages)

