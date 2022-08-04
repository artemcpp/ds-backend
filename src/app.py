from flask import Flask
import logging


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1><center>Hello!</center></h1>'


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.run(host='0.0.0.0', port=8080, debug=True)
