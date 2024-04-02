import requests

host = '178.154.220.122:7777'

def get_image(image_id):
    response = requests.get(
        f'http://{host}/images/{str(image_id)}',
        timeout=0.5,
        
    )
    if response.status_code == 200:
        im = response.content
        return im
    
    return None
