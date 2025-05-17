import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont, QGuiApplication
from pynput import keyboard
from PyQt5.QtCore import QEasingCurve





class FloatingEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_visible = False
        self.dragPos = None
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def initUI(self):
        self.setWindowTitle("Asistan Not")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.screen_w = screen.width()
        self.screen_h = screen.height()

        self.w = int(self.screen_w * 0.5)
        self.line_height = 35
        self.max_lines = int((self.screen_h * 0.6) / self.line_height)
        self.line_count = 3  # Minimum satır

        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(QFont("Segoe UI", 11))
        self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #f8f8f2;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.textChanged.connect(self.check_for_newline)

        self.copyButton = QPushButton("Kopyala", self)
        self.copyButton.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:pressed {
                background-color: #005cbf;
            }
        """)
        self.copyButton.clicked.connect(self.copy_text)

        self.update_layout()

    def resize_and_reposition(self):
        height = self.line_height * self.line_count + 70
        height = min(height, int(self.screen_h * 0.6))
        x = (self.screen_w - self.w) // 2
        y = (self.screen_h - height) // 2
        self.setGeometry(x, y, self.w, height)

    def update_layout(self):
        text_height = self.line_height * self.line_count
        self.textEdit.setGeometry(10, 10, self.w - 20, text_height)
        self.copyButton.setGeometry(self.w - 120, text_height + 20, 100, 35)
        self.resize_and_reposition()

    def check_for_newline(self):
        text = self.textEdit.toPlainText()
        lines = text.count('\n') + 1
        lines = max(lines, 3)
        if lines != self.line_count and lines <= self.max_lines:
            self.line_count = lines
            self.update_layout()

    def copy_text(self):
        text = self.textEdit.toPlainText()
        QGuiApplication.clipboard().setText(text)
        self.copyButton.setText("Kopyalandı!")
        QTimer.singleShot(2000, lambda: self.copyButton.setText("Kopyala"))

    def toggle_window(self):
        if self.isVisible():
            self.hide()
            self.is_visible = False
        else:
            self.show()
            self.activateWindow()
            self.raise_()
            self.is_visible = True

    # 🧲 Sürükleme & animasyon
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos:
            target_pos = event.globalPos() - self.dragPos
            self.anim.stop()
            self.anim.setStartValue(self.pos())
            self.anim.setEndValue(target_pos)
            self.anim.start()
            event.accept()

def start_listener(window_instance):
    def on_press(key):
        try:
            if key == keyboard.Key.ctrl_l:
                pressed_keys.add("ctrl")
            elif hasattr(key, "vk") and key.vk == 53:  # 5 numaralı tuşun virtual key kodu
                if "ctrl" in pressed_keys:
                    window_instance.toggle_window()
        except:
            pass

    def on_release(key):
        if key == keyboard.Key.ctrl_l and "ctrl" in pressed_keys:
            pressed_keys.remove("ctrl")

    pressed_keys = set()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def run():
    app = QApplication(sys.argv)
    window = FloatingEditor()
    window.hide()

    listener_thread = threading.Thread(target=start_listener, args=(window,), daemon=True)
    listener_thread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    run()