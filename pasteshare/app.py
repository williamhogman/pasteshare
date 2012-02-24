"""
Main application
"""

import tornado.web

import pasteshare.index as index

_settings = {
    "template_path": "templates"
}

application = tornado.web.Application([
    ("/", index.IndexHandler)
    ],**_settings)
