from tornado.web import Application
from tornado.ioloop import IOLoop

from app.settings import db
from app.urls import urls


def make_app():
    settings = {'db': db}
    return Application(urls, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.instance().start()
