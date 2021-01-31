"""Compile static assets."""

# gets the context of the currentlty running app that has been set in __init__.py
from flask import current_app as app

# import the Bundle class from flask_assets. A bundle is the unit webassets uses
# to organise groups of media files, which filters to apply and where to strore them
from flask_assets import Bundle


def compile_static_assets(assets):
    """
    Compile stylesheets if in development mode.

    :param assets: Flask-Assets Environment
    :type assets: Environment
    """
    # set auto_build to True, makes sure the bundle is built each time and a
    # cached version is not used/out of date
    assets.auto_build = True

    # set debug to False, changes some behaviours of the app
    assets.debug = False

    # create a Bundle object called less_bundle. A bundle is a collection of
    # files that you would like grouped together with some properties attached
    # to tell webassets how to do its job. This includes things like filters to
    # be applied, or the location where the output file should be stored.
    # The .less files can be found in static/less directory. I am unsure exactly
    # what these do.
    less_bundle = Bundle(
        "less/*.less",
        filters="less,cssmin",
        output="dist/css/styles.css",
        extra={"rel": "stylesheet/less"},
    )

    # register the less_bundle with the assets Environemnt created in __init__.py
    assets.register("less_all", less_bundle)

    # if the FLASK_ENV configured variable is set to development, build the
    # bundle, which means create the file given by the output attribute applying
    # the configured filters etc.
    if app.config["FLASK_ENV"] == "development":
        less_bundle.build()

    # return the assets object
    return assets
