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
        self.load_map()

    def load_map(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        ll = 'll=37.617635,55.755814'
        api_key = 'Ваш ключ'
        size = '650,450'
        map_request = f"{server_address}{ll}&l=map&z={self.mash}&size={size}&apikey={api_key}"
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
        if event.key() == 16777235:
            if self.mash < 17:
                self.mash += 1
                self.load_map()
        elif event.key() == 16777237:
            if self.mash > 1:
                self.mash -= 1
                self.load_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())