import requests
import random

from SendImage import ImageSender

class Memes():
    def get_random_meme():
        print("meme")

        id = random.randint(0, 100)

        url = "http://alpha-meme-maker.herokuapp.com/memes/" + str(id)

        res = requests.get(url)

        print(res.text)

        json = res.json()

        print(json['data']['image'])

        link = json['data']['image']

        return link
