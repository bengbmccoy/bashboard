"""Initialize Flask app using the application factory function init_app.
Also treats this application factory as a package."""


from flask import Flask
from flask_assets import Environment

# TODO: I am unsure about how useful the below code is, to be looked into
# from ddtrace import patch_all
# patch_all()


def init_app():
    """Construct core Flask application with embedded Dash app."""

    # __name__ is the path of the current Python module, Flask needs to know
    # where it is located to setup paths.
    # instance_relative_config tells the app that config files are not relative
    # to the instance folder.
    app = Flask(__name__, instance_relative_config=False)

    # gets the config information from the Config class that is stored in the
    # config.py file. This class gets the variables from the .env file
    app.config.from_object("config.Config")

    # Creates an Environment object from flask_assets to hold a collection of
    # bundles and configuration. If initialised with an instance of Flask app
    # then webassets Jinja2 extention is automatically registered.
    assets = Environment()

    # the app is passed to Envoronment.init_app to allow usage by multiple
    # applications rather than passing a fixed application object, see url below:
    # https://flask-assets.readthedocs.io/en/latest/#flask_assets.Environment
    assets.init_app(app)

    # gets the context of the current app, in case there are multiple flask apps
    # running at the same time.
    # Import parts of our core Flask app
    with app.app_context():

        # imports and executes routes.py which assigns different URLs to
        # different functions which can render HTML pages from jinja2 templates
        from . import routes

        # import the compile_static_assets function from the assets.py file.
        # This function compiles a bunch of stylesheets when the app variable
        # FLASK_ENV is set to "development"
        from .assets import compile_static_assets

        # Import Dash application init_dashboard(server) function
        from .plotlydash.dashboard import init_dashboard

        # Give the init_dashboard function the existing flask object (app) to be
        # used as the main server that this sub-app will run on.
        app = init_dashboard(app)

        # Compile static assets -
        # THIS WAS TURNED OFF AS IT WAS BREAKING GOOGLE APP ENGINE
        # compile_static_assets(assets)

        # return the fully configured/setup app to the wsgi.py file to be run
        return app
