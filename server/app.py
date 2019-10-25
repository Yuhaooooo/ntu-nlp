from serving.starter import AppStarter


class App(AppStarter):
    scan_paths = ['model']


app = App.config()

if __name__ == '__main__':
    app.run()
