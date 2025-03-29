import os
import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design.ui', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mash = 10
        self.longitude = 37.617635
        self.latitude = 55.755814
        self.load_map()

    def load_map(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '04e437d7-cc71-4689-b13e-217c78e3bd83'
        size = '650,450'
        map_request = f"{server_address}ll={self.longitude},{self.latitude}&l=map&z={self.mash}&size={size}&apikey={api_key}"
        response = requests.get(map_request)
        if not response.ok:
            print(f"Ошибка {response.status_code}: {response.reason}")
            print("URL:", response.url)
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as f:
            f.write(response.content)

        self.label.setPixmap(QPixmap(self.map_file))
        os.remove(self.map_file)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)

        move_factor = 0.2 / (2 ** (self.mash - 10))

        if event.key() == Qt.Key.Key_Up:
            self.latitude += move_factor
            if self.latitude > 85:
                self.latitude = 85
            self.load_map()

        elif event.key() == Qt.Key.Key_Down:
            self.latitude -= move_factor
            if self.latitude < -85:
                self.latitude = -85
            self.load_map()

        elif event.key() == Qt.Key.Key_Left:
            self.longitude -= move_factor
            if self.longitude < -180:
                self.longitude += 360
            self.load_map()

        elif event.key() == Qt.Key.Key_Right:
            self.longitude += move_factor
            if self.longitude > 180:
                self.longitude -= 360
            self.load_map()

        elif event.key() == Qt.Key.Key_PageUp:
            if self.mash < 17:
                self.mash += 1
                self.load_map()

        elif event.key() == Qt.Key.Key_PageDown:
            if self.mash > 1:
                self.mash -= 1
                self.load_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())