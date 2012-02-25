"""
Main application
"""

import tornado.web as web
import pasteshare.index as index
import pasteshare.pastes as pastes
_settings = {
    "template_path": "templates"
}

application = web.Application([
    ("/", index.IndexHandler),
    ("/pastes/([0-9]+)",pastes.PasteHandler),
    (r"/img/(.*)", web.StaticFileHandler, {"path": "img"}),
    (r"/css/(.*)", web.StaticFileHandler, {"path": "css"})
    ],**_settings)
