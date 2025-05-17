import time
#! Derlerken 'pip install -q -U google-genai' yada 'pip install -q -U google-genai --break-system-packages' kullanın 
import keyboard
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QVBoxLayout, QSystemTrayIcon, QStyle,
    QMenu, QAction, QLabel, QPushButton
)
from PyQt5.QtGui import QFont, QColor, QIcon, QPainter
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from google import genai
import sys
from pynput.keyboard import Key, Controller

from model import radar


IS_CAPTURED = False # DEBUG, DEFOULD = False

def capture():
    global IS_CAPTURED
    #* Kısayol kullanıldığında seçilen metni yakalamak için kopyalamayı simüle eder
    #* Kopyalanan metin = text => show_floating_popup(text)
    IS_CAPTURED = True
    #keyboard = Controller()

    keyboard.press('ctrl')
    keyboard.press('c')
    keyboard.release('c')
    keyboard.release('ctrl')

    '''
    with keyboard.pressed(Key.ctrl):
        #! emülasyon çalışmıyor, ctrl+c basılmıyor <--
        print('emülatör çalışıyor')
        keyboard.press('c')
        keyboard.release('c')
    '''

import keyboard #! Linuxda yöneticilik gerektirir 
keyboard.add_hotkey('ctrl+alt+o', capture)

#! API erişimidir
#! Yürütülebilir versiyonlarda hazır girilidir
#! Eğer kendiniz derliyorsanız, googleGenai API anahtarınızı buraya girin
client = genai.Client(api_key="AIzaSyDVN386y_WYLyzuV3iygXVdaUJJvRHZs4Y")

def suggestNew(text,word):
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=f'''SANA AZ SONRA VERECEĞİM CÜMLEYİ, ANALİZ ET,
      VE VERDİĞİM KELİME YERİNE CÜMLE İÇİN DAHA İYİ ALTERNATİF SUN,
      YENİ KELİME ÖNERİSİNİ DOĞRUDAN CEVAP OLARAK DÖNDÜR, YANİ YENİ KELİME DIŞINDA BİR CEVAP DÖNDÜRME, TEK CEVAP OLSUN
      EĞER KELİMEYİ CÜMLEDEN SİLMEK DAHA UYGUN İSE '#' CEVAP OLARAK GÖNDER
      cümlenin tamamı : {text}
      alternatif sunman gereken kelime : {word}
      ''',
  )

# optimizator fonksiyonu
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
    
    #return radar(response.text) ##! BURAYLA DAHA SONRA İLGİLEN
    return response.text


def highlight_changes(original, optimized):
    original_words = original.split()
    optimized_words = optimized.split()

    highlighted_text = ""
    for o_word, opt_word in zip(original_words, optimized_words):
        if o_word != opt_word:
            highlighted_text += f'<span style="background-color: #2196F3; color: white;">{opt_word}</span> '
        else:
            highlighted_text += opt_word + ' '

    for opt_word in optimized_words[len(original_words):]:
        highlighted_text += f'<span style="background-color: #2196F3; color: white;">{opt_word}</span> '

    return highlighted_text


class LoadingCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setStyleSheet("background-color: orange; border-radius: 20px;")
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
        self.setWindowOpacity(0.85)

        screen_geometry = QApplication.desktop().availableGeometry()
        self.resize(400, 100)
        self.move(screen_geometry.width() - 420, screen_geometry.height() - 120)

        self.optimized_plain = ""

        layout = QVBoxLayout()

        self.circle = LoadingCircle()
        layout.addWidget(self.circle, alignment=Qt.AlignCenter)

        self.text_display = QTextEdit()
        self.text_display.setText("Metin optimize ediliyor...")
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet(
            "background-color: #121212; color: white; border-radius: 12px; padding: 10px;"
        )
        self.text_display.setFont(QFont("Segoe UI", 13))
        layout.addWidget(self.text_display)

        self.copy_button = QPushButton("Kopyala")
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.copy_button.clicked.connect(self.copy_optimized_text)
        self.copy_button.setVisible(False)
        layout.addWidget(self.copy_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.show()

        self.animation = QPropertyAnimation(self.circle, b"rotation")
        self.animation.setDuration(2000)
        self.animation.setLoopCount(-1)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.start()

        QTimer.singleShot(100, lambda: self.optimize_and_update(original_text))

    def optimize_and_update(self, text):
        try:
            optimized = optimizeThis(text)
            self.optimized_plain = optimized
            highlighted_optimized = highlight_changes(text, optimized)
            self.text_display.setHtml(highlighted_optimized)

            doc_height = self.text_display.document().size().height()
            content_height = int(doc_height * 1.6) + 100 

            screen_height = QApplication.desktop().availableGeometry().height()
            max_height = screen_height // 2
            final_height = min(max_height, max(150, content_height))

            self.setFixedHeight(final_height)

            self.copy_button.setVisible(True)

        except Exception as e:
            self.text_display.setText(f"[HATA] optimize edilemedi:\n{e}")

        self.animation.stop()
        QTimer.singleShot(5000, self.close)

    def copy_optimized_text(self):
        QApplication.clipboard().setText(self.optimized_plain)


class ClipboardListenerApp(QApplication):
    global IS_CAPTURED
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
        global IS_CAPTURED
        if IS_CAPTURED:
            text = self.clipboard().text()
            if text.strip():
                self.show_floating_popup(text)
                IS_CAPTURED = False

    def show_floating_popup(self, text):
        self.popup = FloatingWindow(text)
        self.popup.show()


if __name__ == '__main__':
    app = ClipboardListenerApp(sys.argv)
    sys.exit(app.exec_())
