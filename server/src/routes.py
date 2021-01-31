"""Routes for parent Flask app.
Currently this only includes the home/index page of the URL
"""

# gets the context of the currentlty running app that has been set in __init__.py
from flask import current_app as app

# import the function to render a template from a template folder with the given
# context
from flask import render_template

# use the route() decorator to tell Flask what URL should trigger the below function
# in this case it is the home/index URL
@app.route("/")
def home():
    """Landing page, based on index.jinja2 file which acts as the homepage"""
    return render_template(
        "index.jinja2",
        title="Welcome to Ben's website!",
        description="Some fun application developed by Ben McCoy for personal projects.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )
