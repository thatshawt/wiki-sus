from flask import render_template


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # this is not a placeholder :P
        return render_template("main.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/pages/")
    def pages():
        #TODO: this is just a placeholder
        return render_template("main.html")

