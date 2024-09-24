import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import csv

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotator")

        # Kullanıcıdan görüntü klasörünü seçmesini iste
        self.image_dir = filedialog.askdirectory(initialdir="C:/Users/user/Desktop", title="Görüntü Klasörünü Seç")
        if not self.image_dir:
            exit()

        # Seçilen klasördeki görüntü dosyalarını al
        self.image_files = [f for f in os.listdir(self.image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_image_index = 0

        # Kullanıcıdan CSV dosyasının kaydedileceği konumu ve adını iste
        self.csv_file = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                       filetypes=[("CSV Files", "*.csv")],
                                                       initialdir="C:/Users/user/Desktop", 
                                                       title="CSV Dosyasını Kaydet")
        if not self.csv_file:
            exit()

        # CSV dosyasını oluştur, eğer yoksa başlıkları ekle
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Image Name', 'Value'])  # Başlık satırı

        self.create_widgets()

        # İlk görüntüyü göster
        self.show_image()

    def create_widgets(self):
        # Görüntüyü gösterecek label
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Kullanıcının gireceği değer için giriş alanı
        self.value_entry = tk.Entry(self.root)
        self.value_entry.pack()
        self.value_entry.focus()  # Giriş alanına odaklan

        # Kaydet ve sonraki görüntüye geç butonu
        self.next_button = tk.Button(self.root, text="Kaydet ve Sonraki", command=self.save_and_next)
        self.next_button.pack()

    def show_image(self):
        # Geçerli görüntüyü göster
        if self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.image_dir, self.image_files[self.current_image_index])
            image = Image.open(image_path)
            image = image.resize((400, 400))  
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo  # Referansı tutuyoruz ki görüntü kaybolmasın
            self.value_entry.delete(0, tk.END)  # Giriş alanını temizle
            self.value_entry.focus()  # Giriş alanına odaklan
        else:
            # Tüm görüntüler işlendiğinde
            self.image_label.config(text="Tüm görüntüler işlendi.")
            self.value_entry.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)

    def save_and_next(self):
        # Kullanıcının girdiği değeri al ve kaydet
        value = self.value_entry.get()
        if value:
            try:
                # Değerin float olduğundan emin ol
                float_value = float(value)

                # Değerin 0-10 arasında olup olmadığını kontrol et
                if 0 <= float_value <= 10:
                    # Değeri CSV dosyasına yaz
                    with open(self.csv_file, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([self.image_files[self.current_image_index], float_value])

                    # Sonraki görüntüye geç
                    self.current_image_index += 1
                    self.show_image()
                else:
                    # Geçersiz aralıkta değer girildiğinde
                    print("Lütfen değeri 0 ile 10 arasında girin.")
                    self.value_entry.delete(0, tk.END)  # Giriş alanını temizle
                    self.value_entry.focus()  # Giriş alanına odaklan
            except ValueError:
                # Geçersiz değer girildiğinde
                self.value_entry.delete(0, tk.END)
                print("Lütfen geçerli bir float değeri girin.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()




