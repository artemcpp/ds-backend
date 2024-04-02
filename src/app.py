import logging
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
import logging
import io
from image_provider_client import get_image


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:blue;"><center>Hello, {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    # logging.error(request.json)
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello, {user}!',
    }


# <url>:8080/readPlateNumber : json {im_id: [<image_id>, ...]}
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    if 'im_id' not in request.json:
        return {'error': 'field "im_id" not found'}, 400
    im_ids = request.json['im_id']

    if isinstance(im_ids, int):
        im_ids = [im_ids]
    elif not isinstance(im_ids, list):
        return {'error': f'Wrong type. Should be list or int, but got {type(im_ids)} instead'}
    
    ans = dict()
    for im_id in im_ids:
        num_tries = 5
        for _ in range(num_tries):
            im = get_image(im_id)
            if im:
                break
        
        if im is None:
            logging.error('wrong image id')
            return {'error': f'No image with id={im_id}'}, 400
        im = io.BytesIO(im)

        try:
            res = plate_reader.read_text(im)
        except InvalidImage:
            logging.error('invalid image')
            return {'error': f'invalid image with id={im_id}'}, 400
        ans[im_id] = res

    return {
        'plate_numbers': ans,
    }


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    # app.json.ensure_ascii = False
    app.run(host='0.0.0.0', port=8080, debug=True)
