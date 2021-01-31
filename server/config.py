"""
Flask config file.
This file uses the os package to set the BASE_DIR path as the current directory,
then it uses the load_dotenv function to read the .env file from the current
directory which contains a bunch of environment variable.
Lastly a Config class is defined which collects the variables from the .env file
and sets them as variables.
"""

# allows script to access environment variable and paths
from os import environ, path

# allows the loading of .env files into a virtual environment
from dotenv import load_dotenv

# get the path of the base directory from the path to this file
BASE_DIR = path.abspath(path.dirname(__file__))

# reads the .env file and adds them to the environment variables
load_dotenv(path.join(BASE_DIR, ".env"))


class Config:
    """Flask configuration variables."""

    # General Config variables set in .env file
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Assets set in .env file
    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")
