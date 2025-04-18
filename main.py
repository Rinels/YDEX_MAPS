import os
import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mash = 10
        self.longitude = 37.617635
        self.latitude = 55.755814
        self.point0 = 0
        self.point1 = 0

        self.current_theme = "light"
        self.point = False

        self.findOpen.clicked.connect(self.find)
        self.radioButton.toggled.connect(self.theme)
        self.cleanButton.clicked.connect(self.clean)

        self.load_map()

    def load_map(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '04e437d7-cc71-4689-b13e-217c78e3bd83'
        size = '650,450'
        map_request = (
            f"{server_address}"
            f"ll={self.longitude},{self.latitude}"
            f"&l=map&z={self.mash}"
            f"&size={size}"
            f"&theme={self.current_theme}"
        )
        if self.point:
            map_request += f"&pt={self.point0},{self.point1},pm2rdm&apikey={api_key}"
        else:
            map_request += f"&apikey={api_key}"
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

    def theme(self):
        if self.radioButton.isChecked():
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.load_map()

    def clean(self):
        self.point = False
        self.addressLine.clear()
        self.load_map()

    def find(self):
        self.search_window = SearchWindow(self)
        self.search_window.exec()

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
                

class SearchWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        uic.loadUi('SearchWindow.ui', self)

        self.index = ""
        self.address = ""

        self.findButton.clicked.connect(self.search)
        self.indexButton.toggled.connect(self.toggle_index)

    def toggle_index(self):
        if self.indexButton.isChecked() and self.index:
            self.main_window.addressLine.setText(f'{self.address} Индекс: {self.index}')
        else:
            self.main_window.addressLine.setText(self.address)

    def search(self):
        self.main_window.point = True
        server_address = 'http://geocode-maps.yandex.ru/1.x/?'
        api_key = '8013b162-6b42-4997-9691-77b7074026e0'
        geocoder_request = f'{server_address}apikey={api_key}&geocode={self.searchEdit.text()}&format=json'
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"].split()
            toponym_index = ""
            address_data = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]
            if "postal_code" in address_data:
                toponym_index = address_data["postal_code"]
            self.main_window.longitude = float(toponym_coodrinates[0])
            self.main_window.latitude = float(toponym_coodrinates[1])

            self.main_window.point0 = float(toponym_coodrinates[0])
            self.main_window.point1 = float(toponym_coodrinates[1])

            self.index = toponym_index
            self.address = toponym_address

            self.main_window.addressLine.setText(self.address)

            self.main_window.load_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())