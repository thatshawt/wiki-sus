from flask import render_template, send_file, request, abort, redirect, url_for
from flaskr import backend
from flaskr.user_list import User_List
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from google.cloud import storage
from copy import copy

import tempfile


backend = backend.Backend()
user_list = User_List()


def make_endpoints(app):

    # - Login Stuff -
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return user_list.retrieve_user(user_id)

    # - Login Stuff -

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html", title='home', current_user=current_user)

    @app.route("/upload", methods=['GET','POST'])
    def upload():
        if request.method == 'GET':
            return render_template("upload.html", title='upload')
        elif request.method == 'POST':
            post_title = str(request.form['post_title'])
            post_content = request.form['content']
            wikiname = backend.upload(post_title, post_content)  
            return render_template("upload.html",
                link="/pages/" + wikiname)

    @app.route("/about")
    @login_required
    def about():
        return render_template("about.html", title='about', current_user=current_user)

    @app.route("/pages/")
    def pages():
        pages = []
        page_names = backend.get_all_page_names()
        for page_name in page_names:
            pages.append({
                "name": page_name,
                "link": "/pages/" + page_name + "/"
            })
        return render_template("pages.html", pages=pages, title='pages', current_user=current_user)

    @app.route("/pages/<page>/")
    def pages2(page):
        content = backend.get_wiki_page(page)

        if content == None:abort(404)

        return render_template("wikipage.html", post_title=page, post_content=content)

    @app.route("/signup", methods=['POST', 'GET'])
    def signup(): # FIXED signup
        if request.method == 'GET':
            return render_template("signup.html", title='signup', image=backend.get_image())
        elif request.method == 'POST':
            username = str(request.form.get("username"))
            password = str(request.form.get("password"))
            answer = backend.sign_up(username, password)
            if answer == 'INVALID': # This is a draft for now. Will improve tomorrow
                return 'INVALID'
            elif answer == 'ALREADY EXISTS':
                return 'USER ALREADY EXISTS'
            return "SUCCESFULL"

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            username = str(request.form.get('username'))
            password = str(request.form.get('password'))
            if backend.sign_in(username, password):
                user = user_list.update_list(username)
                login_user(user)
                return redirect(url_for('home'))

        # If user already authenticated they can't login again
        if not current_user.is_authenticated:
            return render_template('login.html')

        return redirect(url_for('home'))

    @app.route('/logout')
    @login_required
    def logout():
        user_list.remove_user_from_session(current_user.get_id())
        logout_user()
        return redirect(url_for('login'))



    # THESE TWO FUNCTIONS ARE FOR TESTING/DEBUGGING PURPOSES
    @app.route('/session')
    @login_required
    def session():
        if user_list.retrieve_user(current_user.get_id()).username == 'admin':
            return render_template('session.html', users_dictionary=user_list.get_active_users(), available_ids=user_list.get_available_ids(), occupied=user_list.get_active_sessions())
        return 'no access'


    @app.route('/test')
    def test():
        user_list.poblate_users()

        return redirect('/session')
    
    @app.route('/test2')
    def test2():
        user_list.change_user_id('2')
        #return redirect('/session')
        return str(user_list.get_active_sessions())