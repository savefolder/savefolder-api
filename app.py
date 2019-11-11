from core.app import Application

app = Application()

# TODO: DECOUPLE MONGO & REDIS INITIALIZATION
import views

app.router.register(views)

if __name__ == '__main__':
    app.run()
