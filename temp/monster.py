# ===========================
# MISCELLANEOUS UTILS SECTION
# ===========================

import time
import sys


def terminate(message):
    # Give stdout time to flush properly
    time.sleep(0.1)
    print('Something went wrong - check logs', file=sys.stderr)
    print('Error:', message, file=sys.stderr)
    input()


# ============================
# DYNAMIC INSTALLATION SECTION
# ============================

import subprocess as sp
import importlib

REQUIREMENTS = {
    'pymongo': 'pymongo',
    'pyperclip': 'pyperclip',
    'imagehash': 'imagehash',
    'requests': 'requests',
    'vk_api': 'vk-api',
    'PyQt5': 'PyQt5',
    'PIL': 'pillow',
    'Qt': 'qt.py',
}

print('Checking required packages...')
for package in REQUIREMENTS:
    try:
        print('Checking package:', package + '...', end=' ')
        importlib.import_module(package)
    except ImportError:
        print('FAIL')
        python = sys.executable
        library = REQUIREMENTS[package]
        cmd = [python, '-m', 'pip', 'install', library]
        if sp.call(cmd) != 0:
            terminate('PIP install command failed')
    else:
        print('OK')

# =============================
# CREDENTIALS RETRIEVAL SECTION
# =============================

import pyperclip
import requests
import json
import os

APP_ID = '7093981'
APP_SECRET = 'fQ01TnqFxLqVtkzmj3iL'
REDIRECT = 'https://example.com/callback'
SCOPE = 'offline,photos'
AUTH_URL = (
        'https://oauth.vk.com/authorize'
        + '?redirect_uri=' + REDIRECT
        + '&client_id=' + APP_ID
        + '&scope=' + SCOPE
)
TOKEN_URL = (
        'https://oauth.vk.com/access_token'
        + '?redirect_uri=' + REDIRECT
        + '&client_secret=' + APP_SECRET
        + '&client_id=' + APP_ID
        + '&code='
)

print('Checking vk credentials...', end=' ')
if not os.path.exists('secret.json'):
    print('FAIL\nRequesting credentials...')
    pyperclip.copy(AUTH_URL)
    print('>>> Auth url is injected to your clipboard')
    print('>>> Open it in browser, authenticate and copy redirect url')
    print('>>> Script will resume automatically')
    print('Waiting for url...', end=' ', flush=True)
    while True:
        time.sleep(1)
        text = pyperclip.paste()
        if text.startswith(REDIRECT):
            print('DONE')
            if 'error' in text:
                terminate('VK authentication failed')
            code = text[text.find('=') + 1:]
            data = requests.get(TOKEN_URL + code).json()
            with open('secret.json', 'w') as file:
                data = {'token': data['access_token'], 'uid': data['user_id']}
                json.dump(data, file)
            break
else:
    print('OK')

with open('secret.json') as file:
    data = json.load(file)
    VK_TOKEN = data['token']
    VK_UID = data['uid']

# ==============================
# INITIAL PHOTO INDEXING SECTION
# ==============================

from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

from vk_api import VkApi, ApiError
from PIL import Image, ImageQt
from hashlib import md5
from io import BytesIO
import imagehash

print('Checking vk api token...', end=' ')
try:
    vk = VkApi(token=VK_TOKEN).get_api()
    data = vk.photos.getAlbums()
except ApiError:
    print('FAIL')
    terminate('Test vk api call failed')
else:
    print('OK')


class StrangeSlider(QLabel):
    SIZE = QSize(800, 150)
    MAX_WIDTH = 400
    EASING = QEasingCurve.OutCubic
    DURATION = 500
    MARGIN = 20

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(self.SIZE)
        self.canvas = QPixmap(self.SIZE)
        self.canvas.fill(QColor(0, 0, 0, 0))
        self.setPixmap(self.canvas)
        self.animation = QVariantAnimation(self)
        self.animation.setEasingCurve(self.EASING)
        self.animation.setDuration(self.DURATION)
        self.animation.valueChanged.connect(self.animate)

    def animate(self, x):
        try:
            point = QPoint(x, 0)
            rect = QRect(point, self.size())
            cropped = self.canvas.copy(rect)
            self.setPixmap(cropped)
        except Exception as err:
            print(err)

    def push(self, image):
        if self.animation.state() == QAbstractAnimation.Running:
            # Force currently running animation to end properly
            self.animation.setCurrentTime(self.DURATION)
            QApplication.processEvents()
        # Convert & resize image
        new = ImageQt.toqpixmap(image)
        new = new.scaledToHeight(self.SIZE.height())
        if new.width() > self.MAX_WIDTH:
            # Image is too wide - need to resize again
            new = new.scaledToWidth(self.MAX_WIDTH)
            offset = (self.height() - new.height()) // 2
            placeholder = QPixmap(new.width(), self.height())
            placeholder.fill(QColor(0, 0, 0, 0))
            painter = QPainter(placeholder)
            painter.drawPixmap(0, offset, new)
            new = placeholder
        # Prepare new "canvas"
        width = self.width() + new.width() + self.MARGIN
        canvas = QPixmap(width, self.height())
        canvas.fill(QColor(0, 0, 0, 0))
        # Paste old & new pixmaps on canvas
        painter = QPainter(canvas)
        painter.drawPixmap(0, 0, self.pixmap())
        painter.drawPixmap(self.width() + self.MARGIN, 0, new)
        # Update & start animation
        self.canvas = canvas
        self.animation.setStartValue(0)
        self.animation.setEndValue(new.width() + self.MARGIN)
        self.animation.setCurrentTime(0)
        self.animation.start()


class PhotoLoader(QThread):
    fetched = Signal(object)

    def __init__(self, parent):
        super().__init__(parent)
        # Get photos count to use in progressbar
        data = vk.photos.get(album_id='saved', count=0)
        self.count = data['count']

    def run(self):
        # Get raw photos data
        items = []
        offset = 0
        while True:
            raw = vk.photos.get(
                album_id='saved',
                count=1000,
                offset=offset
            )
            if not raw['items']: break
            items.extend(raw['items'])
            offset += 1000
            time.sleep(0.5)
        # Fetch & process each item
        photos = []
        for item in items:
            best = max(item['sizes'], key=lambda x: x['width'])
            while True:
                try:
                    body = requests.get(best['url']).content
                    image = Image.open(BytesIO(body))
                    image.load()
                    image.split()
                    image.verify()
                except Exception as err:
                    print('Corrupted image - retrying...', file=sys.stderr)
                    print('Error: ', err, file=sys.stderr)
                    time.sleep(1)
                    continue
                else:
                    break
            photos.append({
                'owner': VK_UID,
                'rid': item['id'],
                'url': best['url'],
                'size': {
                    'w': image.width,
                    'h': image.height,
                },
                'hashes': {
                    'md5': str(md5(image.tobytes()).hexdigest()),
                    'ahash': str(imagehash.average_hash(image)),
                    'phash': str(imagehash.phash(image)),
                    'dhash': str(imagehash.dhash(image)),
                    'whash': str(imagehash.whash(image)),
                },
            })
            self.fetched.emit(image)
            time.sleep(0.2)
        # Dump to disk
        with open('photos.json', 'w') as file:
            json.dump(photos, file)
            print('gg', file=sys.stderr)
            QApplication.exit(0)


class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fetching metadata...')
        self.slider = StrangeSlider(self)
        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)
        self.lay = QVBoxLayout(self)
        self.lay.addWidget(self.slider)
        self.lay.addWidget(self.progress)
        self.setFixedSize(self.sizeHint())
        self.loader = PhotoLoader(self)
        self.progress.setMaximum(self.loader.count)
        self.loader.fetched.connect(self.fetched)
        self.loader.start()

    def fetched(self, image):
        self.slider.push(image)
        value = self.progress.value() + 1
        self.progress.setValue(value)
        total = self.progress.maximum()
        self.setWindowTitle('Fetching photos... %s of %s' % (value, total))


# ====================
# YEAH... MAIN SECTION
# ====================

app = QApplication(sys.argv)
loading = LoadingWindow()
loading.show()
app.exec()
