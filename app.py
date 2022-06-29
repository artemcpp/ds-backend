from flask import Flask
from flask import request
import logging
import io

from model import PlateReader

MODEL_PATH='./data/number_reading_resnet18.pth'
TEST_IMAGE='./data/9965.jpg'

app = Flask(__name__)

plate_reader: PlateReader


def load_model():
    global plate_reader
    plate_reader = PlateReader.load_from_file(MODEL_PATH)


def test_model():
    with open(TEST_IMAGE, 'rb') as im:
        assert plate_reader.read_text(im), 'о101но750'
        logging.info('all tests PASSED')


app = Flask(__name__)


@app.route('/')
def hello():
    user = request.args.get('user')
    return f'<h1><center>Hello {user}!</center></h1>'


@app.route('/greeting', methods=['POST'])
def greeting():
    return {'message': request.json.get('user')}


@app.route("/readPlateNumber", methods=['POST'])
def read_plate_number():
    im = request.get_data()
    res = plate_reader.read_text(io.BytesIO(im))
    return {
        'plateNumber': res,
    }


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    load_model()
    logging.info('model loaded')
    test_model()

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
