from serving.starter import AppStarter


class App(AppStarter):
    scan_paths = ['api']


app = App.config()

if __name__ == '__main__':
    app.run()
