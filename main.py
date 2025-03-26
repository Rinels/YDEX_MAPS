import os
import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design.ui', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_map()

    def load_map(self):
        server = 'https://static-maps.yandex.ru/v1'
        params = {
            'll': '135.746181,-27.483765',
            'spn': '0.5,0.5',
            'l': 'map',
            'size': '600,450',
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        }

        response = requests.get(server, params=params)

        if not response.ok:
            print(f"Ошибка {response.status_code}: {response.reason}")
            print("URL:", response.url)
            sys.exit(1)

        # Сохраняем и отображаем карту
        map_file = "map.png"
        with open(map_file, "wb") as f:
            f.write(response.content)

        self.label.setPixmap(QPixmap(map_file))
        os.remove(map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())