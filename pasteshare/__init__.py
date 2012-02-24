"""
Pasteshare module
"""

if __name__ == '__main__':
    import tornado.ioloop
    import pasteshare.app
    application = pasteshare.app.application
    
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
