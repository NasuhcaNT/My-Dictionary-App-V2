import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QInputDialog,QMessageBox, QDialog, QVBoxLayout, QTextBrowser

import os

filename= 'myworldlist.txt'

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Widget'ları oluştur
        self.label = QLabel('Word:', self)
        self.input_box = QLineEdit(self)
        self.button1 = QPushButton('Search', self)
        self.button2 = QPushButton('To Add', self)
        self.button3 = QPushButton('Print All', self)
        self.button4 = QPushButton('Delete All', self)

        # Widget'ların pozisyonlarını ve boyutlarını belirle
        self.label.move(45, 10)
        self.input_box.setGeometry(10, 30, 160, 30)  # (x, y, genişlik, yükseklik)
        self.button1.setGeometry(10, 70, 80, 30)
        self.button2.setGeometry(90, 70, 80, 30)
        self.button3.setGeometry(10, 110, 80, 30)
        self.button4.setGeometry(90, 110, 80, 30)

        # Giriş kutusunun değişiklik sinyalini bağla
        self.input_box.textChanged.connect(self.giris_kutusu_degisti)

        # Butonlara tıklama işlevlerini bağla
        self.button1.clicked.connect(self.buton1_tiklandi)
        self.button2.clicked.connect(self.buton2_tiklandi)
        self.button3.clicked.connect(self.buton3_tiklandi)
        self.button4.clicked.connect(self.buton4_tiklandi)
        
        # Kelime sayısını gösteren etiketi ve değeri ekleyin
        self.kelime_sayisi_label = QLabel('Kelime sayısı: ', self)
        self.kelime_sayisi_label.move(200, 10)

        # Kelime sayısını güncelleyin
        self.guncelle_kelime_sayisi()

        # Pencere özelliklerini ayarla
        self.setWindowTitle('My Vocabulary')
        self.setGeometry(100, 100, 350, 190)  # Pencere boyutu ve konumu
        
        # Yeni bir QLabel ekleyin
        self.anlam_label = QLabel('', self)
        self.anlam_label.setGeometry(10, 150, 320, 30)
             

        # Pencereyi göster
        self.show()

    # Buton tıklama işlevleri
    def buton1_tiklandi(self):
        print('Buton 1 tıklandı')
        girilen_metin = self.input_box.text().strip()  # Giriş kutusundaki metni al ve baştaki ve sondaki boşlukları temizle
        if not girilen_metin:
            QMessageBox.warning(self, 'Uyarı', 'Boş kelime girişi yapamazsınız.')
            return
        sonuc = kelime_ara(girilen_metin)

        # # Sonuç penceresini oluştur ve göster
        # pencere = SonucPenceresi(sonuc)
        # pencere.exec_()
        if sonuc.startswith("Bulunamadı"):
           # Kelime bulunamadıysa, SonucPenceresi'ni güncelleyerek ekleme seçeneğini ekleyin
           sonuc_penceresi = SonucPenceresi("Bulunamadı")
           if sonuc_penceresi.exec_() == QDialog.Accepted:
               kelime_ekle(girilen_metin)
        else:
           # Kelime bulunduysa, sadece SonucPenceresi'ni göster
           sonuc_penceresi = SonucPenceresi(sonuc)
           sonuc_penceresi.exec_()


    def buton2_tiklandi(self):
        girilen_metin = self.input_box.text().strip()  # Giriş kutusundaki metni al ve baştaki ve sondaki boşlukları temizle
        if not girilen_metin:
            QMessageBox.warning(self, 'Uyarı', 'Boş kelime girişi yapamazsınız.')
            return
        print('Buton 2 tıklandı')

        kelime_ekle(girilen_metin)
    

    def buton3_tiklandi(self):
        print('Buton 3 tıklandı')
        kelimeler = butun_kelimeleri_yazdir()
        pencere = KelimelerPenceresi(kelimeler)
        pencere.exec_()
        

        
    def buton4_tiklandi(self):
        print('Buton 4 tıklandı')

        soru = "Bütün kelimeleri silmek istediğinizden emin misiniz?"
        cevap = QMessageBox.question(self, 'Uyarı', soru, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if cevap == QMessageBox.Yes:
            self.kelime_sil()
            QMessageBox.information(self, 'Bilgi', 'Kayıtlar silindi.')
        else:
            QMessageBox.information(self, 'Bilgi', 'Kayıtlar silinmedi.')

    def kelime_sil(self):
        with open(filename, 'w', encoding='utf-8') as dosya:
            dosya.write('')

    # Giriş kutusu değişiklik işlevi
    def giris_kutusu_degisti(self, text):
        print(f'Giriş kutusu değişti. Yeni metin: {text}')
    
    def guncelle_kelime_sayisi(self):
     # Kelime sayısını hesapla ve etiketi güncelle
     sayi = kelime_sayisi()
     self.kelime_sayisi_label.setText(f'Kelime sayısı: {sayi}')
        
class CustomDialog(QDialog):
    def __init__(self, title, message, buttons):
        super().__init__()

        self.setWindowTitle(title)
        layout = QVBoxLayout()

        self.label = QLabel(message, self)
        layout.addWidget(self.label)

        for button_text in buttons:
            button = QPushButton(button_text, self)
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.setLayout(layout)

        self.selected_button = None

    def button_clicked(self):
        sender_button = self.sender()
        self.selected_button = sender_button.text()
        self.accept()

class CustomSearchDialog(QDialog):
    def __init__(self, title, message, buttons):
        super().__init__()

        self.setWindowTitle(title)
        self.label = QLabel(message, self)
        self.buttons = {button: self.addButton(button) for button in buttons}

    def addButton(self, text):
        button = QPushButton(text, self)
        button.clicked.connect(lambda: self.acceptButton(text))
        return button

    def acceptButton(self, button_text):
        self.selected_button = button_text
        self.accept()

class KelimelerPenceresi(QDialog):
    def __init__(self, kelimeler):
        super().__init__()

        self.setWindowTitle('Tüm Kelimeler')
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        label = QLabel('Tüm Kelimeler:', self)
        layout.addWidget(label)

        self.kelimeler_text_browser = QTextBrowser(self)
        self.kelimeler_text_browser.setPlainText(kelimeler)
        layout.addWidget(self.kelimeler_text_browser)

        self.ok_button = QPushButton('Tamam', self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

class SonucPenceresi(QDialog):
    def __init__(self, sonuc):
        super().__init__()

        self.setWindowTitle('Arama Sonuçları')
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        label = QLabel('Arama Sonuçları:', self)
        layout.addWidget(label)

        sonuc_label = QLabel(sonuc, self)
        layout.addWidget(sonuc_label)

        self.ok_button = QPushButton('Tamam', self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

def kelime_ekle(kelime):
    kelime = kelime.lower()
    with open(filename, 'r', encoding='utf-8') as dosya:
        kelimeler = dosya.readlines()

    with open(filename, 'w', encoding='utf-8') as dosya:
        kelime_mevcut = False
        print_control = 0
        for satir in kelimeler:
            mevcut_kelime, mevcut_anlam = satir.strip().split(':')
            if mevcut_kelime == kelime:
                kelime_mevcut = True

                buttons = ['Evet', 'Hayır', 'Anlamı Değiştir', 'Kelimeyi Sil']
                dialog = CustomDialog('Kelime Zaten Var', f"{kelime} kelimesi zaten sözlükte bulunuyor. Bir anlam daha eklemek ister misiniz?", buttons)
                if dialog.exec_() == QDialog.Accepted:
                    cevap = dialog.selected_button.lower()
                    print("cevap:",cevap)
                    if cevap == 'evet':
                        anlam, ok_pressed = QInputDialog.getText(None, 'Anlam Ekle', f"{kelime} kelimesinin anlamını girin:")
                        if ok_pressed and anlam:
                            if anlam not in mevcut_anlam:
                                mevcut_anlam = f"{mevcut_anlam}, {anlam}"
                            else:
                                print_control = 1
                                QMessageBox.information(None, 'Bilgi', f"{kelime} kelimesinin anlamı zaten mevcut: {mevcut_anlam}")

                    elif cevap == 'kelimeyi sil':
                        print_control = 1
                        continue

                    elif cevap == 'anlamı değiştir':
                        yeni_anlam, ok_pressed = QInputDialog.getText(None, 'Anlamı Sil', f"Yeni anlamı girin:")
                        if ok_pressed and yeni_anlam:
                            mevcut_anlam = yeni_anlam
                            QMessageBox.information(None, 'Bilgi', f"{kelime} kelimesinin anlamı güncellendi.")

            dosya.write(f"{mevcut_kelime}:{mevcut_anlam}\n")

        if not kelime_mevcut:
            anlam, ok_pressed = QInputDialog.getText(None, 'Yeni Kelime', f"{kelime} kelimesinin anlamını girin:")
            if ok_pressed and anlam:
                dosya.write(f"{kelime}:{anlam}\n")


# def kelime_ara(kelime):
#     kelime = kelime.lower()  # Kelimeyi küçük harflere dönüştür
#     with open(filename, 'r', encoding='utf-8') as dosya:
#         for satir in dosya:
#             veri = satir.strip().split(':')
#             if veri[0] == kelime:
#                 print(f"{kelime} kelimesinin anlamı: {veri[1]}")
#                 return
#             if kelime in veri[1].lower():  # Anlamlar içinde kelime ara (küçük harfe duyarlı değil)
#                 print(f"{kelime} kelimesi, '{veri[0]}' kelimesinin anlamında bulundu")
#                 return
#         print(f"{kelime} kelimesi sözlükte bulunamadı.")
#         ekleme = input (f"Bu '{kelime}' kelimeyi eklemek ister misiniz? (y/n): ")
#         if ekleme == "y":
#             kelime_ekle(kelime)
# def kelime_ara(kelime):
#     kelime = kelime.lower()  # Kelimeyi küçük harflere dönüştür
#     with open(filename, 'r', encoding='utf-8') as dosya:
#         for satir in dosya:
#             veri = satir.strip().split(':')
#             if veri[0] == kelime:
#                 print(f"{kelime} kelimesinin anlamı: {veri[1]}")
#                 return
#             if kelime in veri[1].lower():  # Anlamlar içinde kelime ara (küçük harfe duyarlı değil)
#                 print(f"{kelime} kelimesi, '{veri[0]}' kelimesinin anlamında bulundu")
#                 return
#         print(f"{kelime} kelimesi sözlükte bulunamadı.")
        
#         buttons = ['Evet', 'Hayır']
#         dialog = CustomDialog('Kelime Bulunamadı', f"Bu '{kelime}' kelimeyi eklemek ister misiniz?", buttons)
#         if dialog.exec_() == QDialog.Accepted:
#             ekleme_cevap = dialog.selected_button.lower()
#             if ekleme_cevap == "evet":
#                 kelime_ekle(kelime)   

def kelime_ara(kelime):
    kelime = kelime.lower()  # Kelimeyi küçük harflere dönüştür
    with open(filename, 'r', encoding='utf-8') as dosya:
        for satir in dosya:
            veri = satir.strip().split(':')
            if veri[0] == kelime:
                print(f"{kelime} kelimesinin anlamı: {veri[1]}")
                return f"{kelime} kelimesinin anlamı: {veri[1]}"
            if kelime in veri[1].lower():  # Anlamlar içinde kelime ara (küçük harfe duyarlı değil)
                print(f"{kelime} kelimesi, '{veri[0]}' kelimesinin anlamında bulundu")
                return f"{kelime} kelimesi, '{veri[0]}' kelimesinin anlamında bulundu"
        print(f"{kelime} kelimesi sözlükte bulunamadı.")
    return f"Bulunamadı: '{kelime}' kelimesini eklemek ister misiniz?"

        # Kelime bulunamazsa, kullanıcıya ekleme seçeneği sun

        # ekleme = input (f"Bu '{kelime}' kelimeyi eklemek ister misiniz? (y/n): ")
        # if ekleme == "y":
        #     kelime_ekle(kelime)
        






        
def kelime_sayisi():
    with open(filename, 'r', encoding='utf-8') as dosya:
        kelimeler = dosya.readlines()
        return len(kelimeler)
        #print(f"Sözlükte {kelime_sayisi()} kelime bulunuyor.")

def butun_kelimeleri_yazdir():
    with open(filename, 'r', encoding='utf-8') as dosya:
        kelimeler = dosya.readlines()
        return ''.join(kelimeler)
#         # for satir in kelimeler:
#         #     kelime, anlam = satir.strip().split(':')
#         #     print(f"{kelime}: {anlam}")
            
def kelime_sil():
    onay = input("Tüm kayıtları silmek istediğinizden emin misiniz? (evet/hayır): ").lower()
    if onay == 'evet':
        with open(filename, 'w', encoding='utf-8') as dosya:
            dosya.write('')
        print("Tüm kayıtlar silindi.")
    else:
        print("Kayıtlar silinmedi.") 

def klasor_ve_txt_olustur(klasor_adi):
    try:
        # Klasörü oluştur
        os.makedirs(klasor_adi)

        # Dosya yolu oluştur
        dosya_yolu = os.path.join(klasor_adi, 'myworldlist.txt')

        # Dosyayı oluştur ve içine bir şeyler yaz
        with open(dosya_yolu, 'w') as dosya:
            dosya.write("")

        print(f'{klasor_adi} adlı klasör ve içinde "myworldlist.txt" adlı dosya oluşturuldu.')

    except OSError as hata:
        print(f'Hata oluştu: {hata}')

# bir klasör oluştur
klasor_ve_txt_olustur('myworldlist')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    sys.exit(app.exec_())
