
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QVBoxLayout, QSystemTrayIcon, QStyle, QMenu, QAction, QLabel
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from google import genai
import sys
from PyQt5.QtGui import QPainter


# API Key'i gir
client = genai.Client(api_key="AIzaSyDVN386y_WYLyzuV3iygXVdaUJJvRHZs4Y")


def optimizeThis(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f'''
        SANA AZ SONRA VERECEĞİM CÜMLEYİ, OPTİMİZE ET,
        NOKTALAMA İŞARETLİNİ VE YAZIM KURALLARINI DÜZELT,
        CÜMLENİN DÜZELTİLMİŞ HALİNİ SADECE CEVAP OLARAK DÖNDÜR
        düzletilecek cümle : {text}
        ''',
    )
    return response.text


class LoadingCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 40)  # Yuvarlağın boyutu
        self.setStyleSheet("background-color: orange; border-radius: 20px;")  # Yuvarlak şekli
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#FF9800"))
        painter.drawEllipse(0, 0, 40, 40)


class FloatingWindow(QWidget):
    def __init__(self, original_text):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)

        screen_geometry = QApplication.desktop().availableGeometry()
        self.resize(400, 100)
        self.move(screen_geometry.width() - 420, screen_geometry.height() - 120)

        layout = QVBoxLayout()

        # Yuvarlak dönen animasyon
        self.circle = LoadingCircle()
        layout.addWidget(self.circle, alignment=Qt.AlignCenter)

        self.text_display = QTextEdit()
        self.text_display.setText("Metin optimize ediliyor...")
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet(
            "background-color: #121212; color: white; border-radius: 12px; padding: 10px;")
        self.text_display.setFont(QFont("Segoe UI", 13))
        layout.addWidget(self.text_display)

        self.setLayout(layout)
        self.show()

        # Yuvarlak animasyon
        self.animation = QPropertyAnimation(self.circle, b"rotation")
        self.animation.setDuration(2000)  # Süreyi ayarla
        self.animation.setLoopCount(-1)  # Sonsuz döngü
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.start()

        # Optimize işlemini arka planda başlat
        QTimer.singleShot(100, lambda: self.optimize_and_update(original_text))

    def optimize_and_update(self, text):
        try:
            optimized = optimizeThis(text)
            self.text_display.setText(optimized)
        except Exception as e:
            self.text_display.setText(f"[HATA] optimize edilemedi:\n{e}")

        # Animasyonu durdur
        self.animation.stop()
        QTimer.singleShot(5000, self.close)


class ClipboardListenerApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon.fromTheme("edit-copy", self.style().standardIcon(QStyle.SP_FileDialogInfoView)))
        self.tray.setVisible(True)

        menu = QMenu()
        exit_action = QAction("Çıkış")
        exit_action.triggered.connect(self.quit)
        menu.addAction(exit_action)
        self.tray.setContextMenu(menu)

        self.clipboard().dataChanged.connect(self.on_clipboard_change)

    def on_clipboard_change(self):
        text = self.clipboard().text()
        if text.strip():
            self.show_floating_popup(text)

    def show_floating_popup(self, text):
        self.popup = FloatingWindow(text)
        self.popup.show()


if __name__ == '__main__':
    app = ClipboardListenerApp(sys.argv)
    sys.exit(app.exec_())
