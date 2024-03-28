from flask import Flask, jsonify, request
import requests
import logging
from models.plate_reader import PlateReader
import io

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s')

app = Flask(__name__)
plate_reader = PlateReader.load_from_file("/app/model_weights/plate_reader_model.pth")

def download_image(img_id):
    url = f"http://178.154.220.122:7777/images/{img_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        return None

@app.route('/read_plate_single', methods=['GET'])
def read_plate_single():
    img_id = request.args.get('img_id')
    if img_id is None:
        logging.error('img_id parameter is required')
        return jsonify({"error": "img_id parameter is required"}), 400
    
    img_stream = download_image(img_id)
    if img_stream is None:
        logging.error('Failed to download image')
        return jsonify({"error": "Failed to download image"}), 500
    
    plate_number = plate_reader.read_text(img_stream)
    return jsonify({"plate_number": plate_number})

@app.route('/read_plate_multiple', methods=['POST'])
def read_plate_multiple():
    img_ids = request.json.get('img_ids')
    if not img_ids:
        logging.error('img_ids parameter is required')
        return jsonify({"error": "img_ids parameter is required"}), 400

    results = []
    for img_id in img_ids:
        img_stream = download_image(img_id)
        if img_stream is None:
            results.append({"img_id": img_id, "error": "Failed to download image"})
            continue
        plate_number = plate_reader.read_text(img_stream)
        results.append({"img_id": img_id, "plate_number": plate_number})

    return jsonify(results)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s')
    app.run(host='0.0.0.0', port=8080, debug=True)
