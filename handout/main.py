from .gui import App


def main(parser):
    app = App(parser)
    app.window.mainloop()
    return app
