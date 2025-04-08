import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QTextCursor, QColor, QClipboard, QFont
from google import genai

client = genai.Client(api_key="AIzaSyDVN386y_WYLyzuV3iygXVdaUJJvRHZs4Y")

def optimizeThis(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f'''SANA AZ SONRA VERECEĞİM CÜMLEYİ, OPTİMİZE ET,
        NOKTALAMA İŞARETLERİNİ VE YAZIM KURALLARINI DÜZELT,
        KENDİNCE YANLIŞ OLDUĞUNU DÜŞÜNDÜĞÜN KISIMLARI DÜZELT
        VE CÜMLENİN DÜZELTİLMİŞ HALİNİ DOĞRUDAN CEVAP OLARAK DÖNDÜR, YANİ O CÜMLENİN DÜZELTİLMİŞ HALİ DIŞINDA BİR CEVAP DÖNDÜRME, TEK CEVAP OLSUN

        ANCAK DİKKKAT ET : DÜZELTİLECEK VEYA OPTİMİZE EDİLECEK YAZI BİR KOD PARÇASIDA OLABİLİR, EĞER KOD PARÇASI İSE, DAHA KISA, ANLAŞILABİLİR, HIZLI ÇALIŞACAK ŞEKİLDE
        DÜZELTEBİLİRSİN.

        düzletilecek cümle : {text}
        ''',
    )

    return response.text

class TextOptimizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Metin Optimizasyonu')
        self.setGeometry(100, 100, 600, 400)  # Pencere boyutunu küçülttük

        # Koyu Tema Arka Planı
        self.setStyleSheet("background-color: #121212; color: white;")

        self.layout = QVBoxLayout()

        # Metin Alanı
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText('Metninizi kopyalayın...')
        self.text_edit.setStyleSheet("background-color: #2E2E2E; color: white;")
        font = QFont()
        font.setPointSize(14)  # Yazı boyutunu büyüttük
        self.text_edit.setFont(font)
        self.layout.addWidget(self.text_edit)

        # Optimizasyon Sonuç Alanı
        self.result_edit = QTextEdit(self)
        self.result_edit.setPlaceholderText('Optimizasyon sonucu burada görünecek...')
        self.result_edit.setReadOnly(True)
        self.result_edit.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.result_edit.setFont(font)  # Aynı yazı tipini burada da kullandık
        self.layout.addWidget(self.result_edit)

        # Layout'u ayarla
        self.setLayout(self.layout)

        # Clipboard (Panoya kopyalanan metin) izleme
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.handle_clipboard_change)

    def handle_clipboard_change(self):
        clipboard_text = self.clipboard.text()
        if clipboard_text:
            self.text_edit.setPlainText(clipboard_text)
            self.apply_optimization(clipboard_text)

    def apply_optimization(self, text):
        optimized_text = optimizeThis(text)
        self.display_optimized_text(optimized_text)

    def display_optimized_text(self, optimized_text):
        self.result_edit.clear()

        # Optimize edilmiş metni ekleyelim
        cursor = QTextCursor(self.result_edit.document())
        cursor.insertText(optimized_text)

        # Değişiklikleri altı çizili göstermek
        original_text = self.text_edit.toPlainText()
        for i, (orig_char, opt_char) in enumerate(zip(original_text, optimized_text)):
            if orig_char != opt_char:
                cursor.setPosition(i)
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, 1)
                cursor.setCharFormat(cursor.charFormat().setUnderline(True))

app = QApplication(sys.argv)
window = TextOptimizerApp()
window.show()
sys.exit(app.exec_())
