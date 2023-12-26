import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk

import sqlite3
from reportlab.pdfgen import canvas

class DenemePyProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("DenemePy Program")
        self.root.geometry("1080x720")
        
        # Pencere ikonunu ayarla
        image = Image.open("logo.ico")
        self.icon_image = ImageTk.PhotoImage(image)
        self.root.iconphoto(False, self.icon_image)
        

        # SQLite veritabanı bağlantısı
        self.conn = sqlite3.connect("deneme.db")
        self.create_table()

        # Ana frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # İlk yavru frame
        frame1 = tk.Frame(self.main_frame, bg="turquoise", width=360, height=360)  # Arka plan rengini turkuaz olarak değiştirdim
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Veri girişi için alanlar
        label1 = tk.Label(frame1, text="Veri 1:")
        label1.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry1 = tk.Entry(frame1)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        label2 = tk.Label(frame1, text="Veri 2:")
        label2.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry2 = tk.Entry(frame1)
        self.entry2.grid(row=1, column=1, padx=10, pady=10)

        # Butonlar
        save_button = tk.Button(frame1, text="Kaydet", command=self.on_save_button_click, bg="green", fg="white", relief=tk.RAISED)
        save_button.grid(row=2, column=0, pady=10, columnspan=2, sticky="ew")

        delete_button = tk.Button(frame1, text="Sil", command=self.on_delete_button_click, bg="red", fg="white", relief=tk.RAISED)
        delete_button.grid(row=3, column=0, pady=10, columnspan=2, sticky="ew")

        search_button = tk.Button(frame1, text="Ara", command=self.on_search_button_click, bg="blue", fg="white", relief=tk.RAISED)
        search_button.grid(row=4, column=0, pady=10, columnspan=2, sticky="ew")

        
        


        # İkinci yavru frame (frame2)
        frame2 = tk.Frame(self.main_frame, bg="turquoise", width=360, height=360)  # Arka plan rengini turkuaz olarak değiştirdim
        frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        

        # Tablo oluştur
        self.table_frame = tk.Frame(frame2, bg="turquoise", width=360, height=180)
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(self.table_frame, columns=("ID", "Veri 1", "Veri 2"), show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Veri 1", text="Veri 1")
        self.table.heading("Veri 2", text="Veri 2")
        self.table.pack(fill=tk.BOTH, expand=True)

        # Arama sonuçları için frame
        self.search_results_frame = tk.Frame(frame2, bg="turquoise", width=360, height=180)
        self.search_results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.search_results_label = tk.Label(self.search_results_frame, text="Arama Sonuçları:")
        self.search_results_label.pack(pady=5)

        # export_button'ı sağa (RIGHT) yerleştir
        export_button = tk.Button(frame2, text="PDF'ye Aktar", command=self.export_to_pdf)
        export_button.pack(side=tk.RIGHT, pady=5)

        


        self.search_results_table = ttk.Treeview(self.search_results_frame, columns=("ID", "Veri 1", "Veri 2"), show="headings")
        self.search_results_table.heading("ID", text="ID")
        self.search_results_table.heading("Veri 1", text="Veri 1")
        self.search_results_table.heading("Veri 2", text="Veri 2")
        self.search_results_table.pack(fill=tk.BOTH, expand=True)

        # Veri tablosu
        self.load_data_to_table()

        # Tabloya tıklama olayını bağla
        self.table.bind("<ButtonRelease-1>", self.on_table_click)
        
    def export_to_pdf(self):
        # PDF dosyasını kaydetmek için dosya iletişim kutusunu aç
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            # PDF dosyasına verileri yazdır
            self.write_table_data_to_pdf(file_path)
            tk.messagebox.showinfo("Başarılı", "Veriler PDF'ye başarıyla aktarıldı!")

    def write_table_data_to_pdf(self, file_path):
        pdf = canvas.Canvas(file_path)
        pdf.setPageSize((600, 600))

        # Tablo başlıklarını ekle
        headers = ["ID", "Veri 1", "Veri 2"]
        col_widths = [50, 200, 200]

        for i, header in enumerate(headers):
            pdf.drawString(sum(col_widths[:i]) + 5, 580, header)

        # Verileri ekleyin
        for row in self.search_results_table.get_children():
            values = self.search_results_table.item(row)["values"]
            for i, value in enumerate(values):
                pdf.drawString(sum(col_widths[:i]) + 5, 580 - 20 * (self.search_results_table.index(row) + 1), str(value))

        pdf.save()
    

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS veriler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                veri1 TEXT,
                veri2 TEXT
            )
        """)
        self.conn.commit()

    def load_data_to_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM veriler")
        rows = cursor.fetchall()
        for row in rows:
            self.table.insert("", "end", values=row)

    def on_save_button_click(self):
        # "Kaydet" butonuna tıklandığında yapılacak işlemler
        data1 = self.entry1.get()
        data2 = self.entry2.get()

        # Eksik giriş kontrolü
        if not data1 or not data2:
            tk.messagebox.showwarning("Uyarı", "Veri 1 ve Veri 2 alanları boş bırakılamaz!")
            return

        print("Veri 1:", data1)
        print("Veri 2:", data2)

        # Tabloya verileri ekle
        self.table.insert("", "end", values=(None, data1, data2))
        # Veri tablosunu güncelle
        self.insert_data_to_db(data1, data2)

    def on_search_button_click(self):
        # "Ara" butonuna tıklandığında yapılacak işlemler
        search_data1 = self.entry1.get()
        search_data2 = self.entry2.get()

        # Tabloyu temizle
        self.table.delete(*self.table.get_children())
        self.search_results_table.delete(*self.search_results_table.get_children())

        # Arama koşullarına göre veriyi getir
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM veriler")
        rows = cursor.fetchall()

        for row in rows:
            if search_data1.lower() in row[1].lower() or search_data2.lower() in row[2].lower():
                self.search_results_table.insert("", "end", values=row)
            else:
                self.table.insert("", "end", values=row)

    def on_delete_button_click(self):
        # "Sil" butonuna tıklandığında yapılacak işlemler
        selected_item = self.table.selection()
        if selected_item:
            item_id = self.table.item(selected_item)["values"][0]
            self.delete_data_from_db(item_id)
            self.table.delete(selected_item)

    def on_table_click(self, event):
        # Tabloda bir satıra tıklandığında yapılacak işlemler
        selected_item = self.table.selection()
        if selected_item:
            data1 = self.table.item(selected_item)["values"][1]
            data2 = self.table.item(selected_item)["values"][2]
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry1.insert(0, data1)
            self.entry2.insert(0, data2)

    def insert_data_to_db(self, data1, data2):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO veriler (veri1, veri2) VALUES (?, ?)", (data1, data2))
        self.conn.commit()

    def delete_data_from_db(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM veriler WHERE id=?", (item_id,))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    program = DenemePyProgram(root)
    root.mainloop()
