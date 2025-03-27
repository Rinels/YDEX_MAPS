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
        server = 'https://static-maps.yandex.ru/v1?'
        params = {
            'll': '37.617635,55.755814',
            'spn': '0.2,0.2',
            'l': 'map',
            'size': '650,450',
            'apikey': '04e437d7-cc71-4689-b13e-217c78e3bd83'
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