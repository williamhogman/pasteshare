"""
Code to run when run as module
"""

import tornado.ioloop
import pasteshare.app

application = pasteshare.app.application
    
application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
