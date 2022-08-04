import requests


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return res.json()


    def greeting(self, user: str):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            json={
                'user': user,
            },
        )

        return res.json()


if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    with open('./images/9965.jpg', 'rb') as im:
        res = client.read_plate_number(im)
        print(res)
