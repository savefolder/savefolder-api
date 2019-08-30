from pymongo import MongoClient
from vk_api import VkApi
from json import dump, load
from time import sleep

MONGO_URI = 'mongodb+srv://admin:kqgreSUTGdTPx2dg@test-lecwk.mongodb.net/test?retryWrites=true&w=majority'
VK_TOKEN = '6e6170bd03725acbea14984e48f7d2f2bbf71c953381aa10f279e34bbade13355aab6990441a76db01496'

client = MongoClient(MONGO_URI)
db = client.get_database('test')
vk = VkApi(token=VK_TOKEN).get_api()


def fetch_photos():
    items = []
    offset = 0
    while True:
        raw = vk.photos.get(
            album_id='saved',
            count=1000,
            offset=offset
        )
        if not raw['items']: return items
        items.extend(raw['items'])
        offset += 1000
        sleep(0.5)


def dump_photos(data):
    for photo in data:
        best = max(photo['sizes'], key=lambda x: x['width'])
        photo['url'] = best['url']
        photo['size'] = [best['width'], best['height']]
        del photo['sizes']
        del photo['album_id']
        del photo['owner_id']
        del photo['text']
        del photo['date']

    file = open('photos.json', 'w')
    dump(data, file)
    file.close()


def send_index_to_db():
    items = load(open('index.json'))
    entries = []
    for item in items:
        entry = {
            'rid': item['id'],
            'owner': 'abs',
            'url': item['url'],
            'tags': item['tags'],
            'used': 0,
            'size': {
                'w': item['size'][0],
                'h': item['size'][1]
            },
        }
        entries.append(entry)

    return db.images.insert_many(entries)
