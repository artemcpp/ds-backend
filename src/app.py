import logging
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
import logging
import io


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello {user}',
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {
        'plate_number': res,
    }


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
