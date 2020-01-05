"""
Django + Paddle Made Easy.
"""
import pkg_resources

__version__ = pkg_resources.require("dj-paddle")[0].version

default_app_config = "djpaddle.apps.DjpaddleConfig"
