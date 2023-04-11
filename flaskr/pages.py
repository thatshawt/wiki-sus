from flask import render_template, send_file, request, abort, redirect, url_for, flash
from flaskr import backend
from flaskr.user_list import User_List
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from google.cloud import storage
from copy import copy

import tempfile
import base64

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
        return render_template("main.html",
                               title='home',
                               current_user=current_user)

    @app.route("/upload", methods=['GET', 'POST'])
    @login_required
    def upload():
        if request.method == 'GET':
            return render_template("upload.html", title='upload')
        elif request.method == 'POST':
            post_title = str(request.form['post_title'])
            post_content = request.form['content']

            image = request.files['post_image']
            image_string = base64.b64encode(image.read())

            wikiname = backend.upload(post_title, post_content, image_string)
            return render_template("upload.html", link="/pages/" + wikiname)

    @app.route("/about")
    def about():
        return render_template("about.html",
                               title='about',
                               current_user=current_user,
                               salomon_image=backend.get_image("salomon_image"),
                               david_image=backend.get_image("david_image"),
                               carson_image=backend.get_image("carson_image"))

    @app.route("/pages/")
    def pages():
        pages = []
        page_names = backend.get_all_page_names()
        for page_name in page_names:
            pages.append({
                "name": page_name,
                "link": "/pages/" + page_name + "/"
            })
        return render_template("pages.html",
                               pages=pages,
                               title='pages',
                               current_user=current_user)

    @app.route("/pages/<page>/")
    def pages2(page):
        content = backend.get_wiki_page(page)
        author = backend.get_author(page)

        if content == None:
            abort(404)

        return render_template("wikipage.html",
                               post_title=page,
                               post_content=content,
                               post_image=backend.get_image(page),
                               post_author=author)

    @app.route("/signup", methods=['POST', 'GET'])
    def signup():  # FIXED signup
        if request.method == 'GET':
            return render_template("signup.html", title='signup')
        elif request.method == 'POST':
            username = str(request.form.get("username"))
            password = str(request.form.get("password"))
            answer = backend.sign_up(username, password)
            if answer == 'INVALID':  # This is a draft for now. Will improve tomorrow
                flash(
                    'Invalid format. Try Again! You must use valid characters/numbers. User must be 5 characters or more. Password 8 characters or more.'
                )
                return redirect(url_for('signup'))
            elif answer == 'ALREADY EXISTS':
                flash('User already exists. Try a different one!')
                return redirect(url_for('signup'))
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
            else:
                flash('User or password is not correct. Try again!')
                return redirect(url_for('login'))

        # If user already authenticated they can't login again
        if not current_user.is_authenticated:
            return render_template('login.html', title='login')

        return redirect(url_for('home'))

    @app.route('/logout')
    @login_required
    def logout():
        user_list.remove_user_from_session(current_user.get_id())
        logout_user()
        return redirect(url_for('login'))


    @app.route('/messages', methods=['POST', 'GET'])
    @login_required
    def messages():
        if request.method == 'GET':
            message_list = backend.get_user_message_list(user_list.retrieve_user(current_user.get_id()))
            return render_template('messages.html', message_list=message_list)
        return 0

    @app.route('/send_message', methods=['POST', 'GET'])    
    @login_required
    def send_message():
        return 0

    # THESE FUNCTIONS ARE FOR TESTING/DEBUGGING PURPOSES
    @app.route('/session')
    @login_required
    def session():
        if user_list.retrieve_user(current_user.get_id()).username == 'admin':
            return render_template(
                'session.html',
                users_dictionary=user_list.get_active_users(),
                available_ids=user_list.get_available_ids(),
                occupied=user_list.get_active_sessions())
        return 'no access'

    @app.route('/test')
    @login_required
    def test():
        if user_list.retrieve_user(current_user.get_id()).username == 'admin':
            user_list.poblate_users()
            flash(str(current_user.username))
            return redirect(url_for('session'))
        else:
            return 'ACCESS DENIED'

    @app.route('/test2')
    @login_required
    def test2():
        if user_list.retrieve_user(current_user.get_id()).username == 'admin':
            user_list.change_user_id('2')
            return redirect('/session')
        else:
            return 'ACCESS DENIED'

    @app.route('/test3')
    @login_required
    def test3():
        if user_list.retrieve_user(current_user.get_id()).username == 'admin':
            sender = user_list.retrieve_user(5)
            receiver = user_list.retrieve_user(1)
            backend.create_message('Hello World! TEST', sender, receiver)
            return redirect('/session')
        else:
            return 'ACCESS DENIED'
