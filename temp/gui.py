from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from pymongo import MongoClient
from PIL import Image, ImageQt
from hashlib import md5
from io import BytesIO
import imagehash
import requests
import json


MONGO_URI = 'mongodb+srv://admin:kqgreSUTGdTPx2dg@test-lecwk.mongodb.net/test?retryWrites=true&w=majority'


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # Build UI
        self.lay = QVBoxLayout(self)
        self.piclabel = QLabel(self)
        self.piclabel.setAlignment(Qt.AlignCenter)
        self.textbox = QLineEdit(self)
        self.textbox.returnPressed.connect(self.next)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.lay.addWidget(self.piclabel)
        self.lay.addWidget(self.textbox)
        self.lay.addWidget(self.label)
        self.lay.setStretch(0, 1)
        # Prepare stuff
        self.input = iter(reversed(json.load(open('photos.json'))))
        self.output = json.load(open('index.json'))
        self.seen = set(i['id'] for i in self.output)
        self.db = MongoClient(MONGO_URI).get_database('test')
        self.item = None
        self.image = None
        self.hashes = None

    def next(self):
        if self.item is not None: self.save()
        try: self.item = next(self.input)
        except StopIteration: return self.close()
        if self.item['id'] in self.seen: return self.next()
        body = requests.get(self.item['url']).content
        self.image = Image.open(BytesIO(body))
        self.hashes = {
            'md5': str(md5(self.image.tobytes()).hexdigest()),
            'ahash': str(imagehash.average_hash(self.image)),
            'phash': str(imagehash.phash(self.image)),
            'dhash': str(imagehash.dhash(self.image)),
            'whash': str(imagehash.whash(self.image)),
        }

        pixmap = ImageQt.toqpixmap(self.image)
        pixmap = pixmap.scaledToWidth(min(self.image.width, 800))
        self.piclabel.setPixmap(pixmap)
        text = 'MD5: ' + self.hashes['md5'] + '\n'
        text += 'A-Hash: ' + self.hashes['ahash'] + '\n'
        text += 'P-Hash: ' + self.hashes['phash'] + '\n'
        text += 'D-Hash: ' + self.hashes['dhash'] + '\n'
        text += 'W-Hash: ' + self.hashes['whash']
        self.label.setText(text)

    def save(self):
        tags = self.textbox.text()
        self.textbox.clear()
        if not tags: return
        self.item['hashes'] = self.hashes
        self.item['tags'] = tags
        self.output.append(self.item)
        self.seen.add(self.item['id'])

    def closeEvent(self, e):
        file = open('index.json', 'w')
        json.dump(self.output, file)
        return super().closeEvent(e)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
