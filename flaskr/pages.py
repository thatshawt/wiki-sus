from flask import render_template, send_file, request, abort
from flaskr import backend
from google.cloud import storage

import tempfile

backend = backend.Backend()

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html", title='home')

    @app.route("/upload", methods=['GET','POST'])
    def upload():
        if request.method == 'GET':
            return render_template("upload.html", title='upload')
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
        return render_template("about.html", title='about')

    @app.route("/pages/")
    def pages():
        pages = []
        page_names = backend.get_all_page_names()
        for page_name in page_names:
            pages.append({
                "name": page_name,
                "link": "/pages/" + page_name + "/"
            })
        return render_template("pages.html", pages=pages, title='pages')

    @app.route("/pages/<page>/")
    def pages2(page):
        content = backend.get_wiki_page(page)

        if content == None:abort(404)

        wikipage = {
            "content": content,
            "name": page
        }

        return render_template("wikipage.html", wikipage=wikipage)

    @app.route("/signup", methods=['POST', 'GET'])
    def signup(): # FIXED signup
        if request.method == 'GET':
            return render_template("signup.html", title='signup')
        elif request.method == 'POST':
            username = str(request.form.get("username"))
            password = str(request.form.get("password"))
            answer = backend.sign_up(username, password)
            if answer == 'INVALID': # This is a draft for now. Will improve tomorrow
                return 'INVALID'
            elif answer == 'ALREADY EXISTS':
                return 'USER ALREADY EXISTS'
            return "SUCCESFULL"