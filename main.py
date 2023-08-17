from PyQt6.QtWidgets import (
     QApplication, QLineEdit, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox
)
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

import sys

ALLOWED_CHARACTERS = '0123456789'
ICON = 'icon\\png_type\\icon_hourglass.png'
MAX_TIME = 180

class Error(QWidget):
    def __init__(self, text):
        super().__init__()

        self.text = text

    def send_error(self):
        QMessageBox.critical(
            self,
            'Error',
            self.text
        )

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)  # Устанавливаем интервал в 1 секунду

        self.label = QLabel("00:00")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer.start()

    def update_timer(self):
        current_time = self.label.text()
        time_parts = current_time.split(":")
        minutes = int(time_parts[0])
        seconds = int(time_parts[1])

        seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1

        time_string = f"{minutes:02d}:{seconds:02d}"
        self.label.setText(time_string)

class Button(QPushButton):
    def __init__(self, text, parent): #width, height = 280, 70
        super().__init__(text, parent)
        self.setFixedSize(280, 70)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Размер текста
        font = QtGui.QFont()
        font.setPointSize(14)

        # Настройки основного окна
        self.setWindowTitle('Timer')
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.centralwidget = self
        self.centralwidget.setObjectName('centralwidget') # --Не совсем понял, для чего нужна эта строка--
        self.setFixedSize(300, 325)

        # Окно с временем, которое уменьшается каждую секунду
        self.label = QLabel('00:00', self.centralwidget)
        self.label.setFont(font)
        self.label.move(120, 90)
        self.label.setFixedSize(100, 50)

        # Надписи внутри окна
        label = QLabel("Введите количество минут", self.centralwidget)
        label.move(35, 10)
        label.setFixedSize(500, 50)
        label.setFont(font)

        # Кнопка для принятия времени от пользователя
        self.button_set_time = Button('Поставить время', self)
        self.button_set_time.clicked.connect(self.get_time)
        self.button_set_time.setFont(font)
        self.button_set_time.move(10, 140)

        # Кнопка для сброса времени
        self.button_reset = Button('Сбросить время', self)
        self.button_reset.clicked.connect(self.reset_time)
        self.button_reset.setFont(font)
        self.button_reset.move(10, 230)

        # Окно для приема времени от пользователя
        self.input = QLineEdit(self)
        self.input.move(85, 65)

    def reset_time(self):
        '''Останавливает время, появляется возможность ввести новое время'''

        if self.label.text() == '00:00':
            return

        self.input.clear()
        self.timer.timeout.disconnect()
        self.timer.interval = 0
        self.input.setDisabled(False)
        self.label.setText('00:00')

    def get_time(self):
        '''Получение времени от пользователя'''

        def check_valid_cymbols(text: str) -> bool: #Проверка на соответствие символов
            for i in text:
                if i not in ALLOWED_CHARACTERS:
                    return False
            return True

        def check_time(text: str):
            if int(text) > MAX_TIME: return False
            else: return True

        text = self.input.text()

        if check_valid_cymbols(text) == False: # Проверка символов
            # если символы не верные, то появляется окно с ошибкой
            error = Error('В введенных вами символах есть нечисло')
            error.send_error()
            error.show()
            self.input.clear()

        elif check_time(text) == False:
            error = Error(f'Вы ввели больше {MAX_TIME} минут, введите меньше')
            error.send_error()
            error.show()
            self.input.clear()

        elif check_valid_cymbols(text) == True: # Запуск таймера
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(1000)  # обновление каждую секунду
            self.remaining_time = int(text) * 60
            self.input.setDisabled(True)

    def update_timer(self):
        '''Обновление значения таймера на экране'''

        self.minutes = self.remaining_time // 60
        self.seconds = self.remaining_time % 60
        self.label.setText(f'{self.minutes}:{self.seconds:02}')
        self.remaining_time -= 1
        if self.remaining_time < 0: #Конец действия тамера
            self.timer.stop()
            self.label.setText('КОНЕЦ')
            self.input.setDisabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())