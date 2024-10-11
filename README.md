# SockPuppet

Simple Flask-SocketIO implementation in Python with a simple React webpage as its client.

## Start Server
```sh
gunicorn --bind=0.0.0.0:1234 --worker-class eventlet -w 1 --log-level info app:app
```

## Start Client
```sh
npm start
```