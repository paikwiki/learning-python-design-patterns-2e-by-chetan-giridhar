# MVC 패턴 예시 - 토네이도 웹 애플리케이션 프레임워크
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
import sqlite3


def _execute(query):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    res = cur.execute(query)
    conn.commit()
    return res


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        query = "SELECT * FROM task"
        todos = _execute(query)
        self.render(
            "index.html",
            todos=todos,
        )


class NewHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument("name", None)
        query = "CREATE TABLE IF NOT EXISTS task (id INTEGER \
            PRIMARY KEY, name TEXT, status NUMERIC) "
        _execute(query)
        query = f"INSERT INTO task (name, status) \
            VALUES ('{name}', {1})"
        _execute(query)
        self.redirect("/")

    def get(self):
        self.render("new.html")


class UpdateHandler(tornado.web.RequestHandler):
    def get(self, id, status):
        query = f"UPDATE task SET status={int(status)} WHERE \
            id={int(id)}"
        _execute(query)
        self.redirect("/")


class DeleteHandler(tornado.web.RequestHandler):
    def get(self, id):
        query = f"DELETE from task WHERE id={id}"
        _execute(query)
        self.redirect("/")


class RunApp(tornado.web.Application):
    def __init__(self):
        Handlers = [
            (r"/", IndexHandler),
            (r"/todo/new", NewHandler),
            (r"/todo/update/(\d+)/status/(\d+)", UpdateHandler),
            (r"/todo/delete/(\d+)", DeleteHandler),
        ]
        settings = dict(
            debug=True,
            template_path="templates",
            static_path="static",
        )
        tornado.web.Application.__init__(self, Handlers, **settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(RunApp())
    http_server.listen(5005)
    tornado.ioloop.IOLoop.instance().start()
