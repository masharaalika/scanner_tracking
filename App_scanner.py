import customtkinter as ctk
import time
import os
from PIL import Image
from datetime import datetime
from database import simpan_data, get_connection
from history_window import HistoryWindow

# Deteksi folder untuk gambar 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

class AppScanner(ctk.CTk): 
    def __init__(self):
        super().__init__()
        self.title("Sistem Scanner Formulasi")
        self.geometry("1200x800")
        self.configure(fg_color="#0f172a")
        
        self.last_input_time = time.time()
        self.limit_sidebar = 30
        
        self.setup_ui()
        self.update_clock()
        self.load_sidebar_history() 
        self.loop_check()

    def setup_ui(self):
        # HEADER
        self.header = ctk.CTkFrame(self, height=110, corner_radius=0, fg_color="#1e3d59")
        self.header.pack(side="top", fill="x")

        # Logo Mayora
        try:
            logo_path = os.path.join(BASE_DIR, "logo2.png")
            img_logo = Image.open(logo_path)
            self.logo_img = ctk.CTkImage(img_logo, size=(70, 70))
            ctk.CTkLabel(self.header, text="", image=self.logo_img).place(x=25, y=20)
        except:
            ctk.CTkLabel(self.header, text="LOGO", fg_color="#e11d48", width=70, height=70).place(x=25, y=20)

        ctk.CTkLabel(self.header, text="SISTEM SCANNER FORMULASI", font=("Franklin Gothic Heavy", 28, "bold"), text_color="white").place(x=115, y=40)
        
        self.datetime_label = ctk.CTkLabel(self.header, text="", font=("Arial", 14, "bold"), text_color="#38bdf8")
        self.datetime_label.place(relx=0.97, rely=0.15, anchor="ne")
        
        # Tombol icon History di Header 
        try:
            icon_path = os.path.join(BASE_DIR, "icon_history2.png")
            img_hist = Image.open(icon_path)
            self.icon_header = ctk.CTkImage(img_hist, size=(20, 20))
        except:
            self.icon_header = None

        self.btn_full = ctk.CTkButton(self.header, text=" HISTORY", image=self.icon_header, compound="left", 
                                      fg_color="#0ea5e9", font=("Arial", 12, "bold"), command=self.buka_window_history)
        self.btn_full.place(relx=0.97, rely=0.6, anchor="ne")

        #  CONTENT AREA
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(expand=True, fill="both", padx=20, pady=20)

        # Sidebar Kiri
        self.sidebar = ctk.CTkFrame(self.content, width=300, corner_radius=20, fg_color="#1e293b")
        self.sidebar.pack(side="left", fill="y", padx=(0, 15))
        
        ctk.CTkLabel(self.sidebar, text="DATA MASUK", text_color="#38bdf8", font=("Arial", 16, "bold")).pack(pady=15)
        
        self.history_display = ctk.CTkTextbox(self.sidebar, fg_color="#0f172a", text_color="#fffbeb", font=("Consolas", 14), corner_radius=10)
        self.history_display.pack(expand=True, fill="both", padx=15, pady=(0, 10))

        # Tombol "Lihat data lainnya" di bawah sidebar
        self.btn_more = ctk.CTkButton(self.sidebar, text="Lihat data lainnya", fg_color="transparent", 
                                      text_color="#94a3b8", hover_color="#334155", command=self.buka_window_history)
        self.btn_more.pack(pady=10)

        # Area Utama (Tengah)
        self.main_area = ctk.CTkFrame(self.content, corner_radius=20, fg_color="#1e293b")
        self.main_area.pack(side="right", expand=True, fill="both")
        
        # Label Hasil Scan 
        ctk.CTkLabel(self.main_area, text="HASIL SCAN :", font=("Arial", 18, "bold"), text_color="#94a3b8").pack(pady=(150, 5))
        
        self.result_display = ctk.CTkLabel(self.main_area, text="---", font=("Arial", 50, "bold"), text_color="white")
        self.result_display.pack(pady=10)

        # Entry Barcode dengan Placeholder
        self.entry_barcode = ctk.CTkEntry(self.main_area, width=450, height=60, justify="center", 
                                          font=("Arial", 20), placeholder_text="Silahkan scan barcode...",
                                          fg_color="#0f172a", text_color="white", border_color="#38bdf8")
        self.entry_barcode.pack(pady=20)
        self.entry_barcode.focus_set()

    def buka_window_history(self):
        HistoryWindow(self)

    def update_clock(self):
        self.datetime_label.configure(text=datetime.now().strftime("%A, %d %B %Y\n%H:%M:%S"))
        self.after(1000, self.update_clock)

    def load_sidebar_history(self):
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute(f"SELECT kode_barcode FROM latihan.barcode ORDER BY id DESC LIMIT {self.limit_sidebar}")
            rows = cur.fetchall()
            self.history_display.configure(state="normal")
            self.history_display.delete("1.0", "end")
            for row in rows: self.history_display.insert("end", f" • {row[0]}\n")
            self.history_display.configure(state="disabled")
            cur.close(); conn.close()
        except: pass

    def loop_check(self):
        val = self.entry_barcode.get().strip()
        if val and time.time() - self.last_input_time > 0.6:
            if simpan_data(val):
                self.result_display.configure(text=val) # Update teks hasil scan
                self.load_sidebar_history()
                self.entry_barcode.delete(0, 'end')
                self.last_input_time = time.time()
        self.after(100, self.loop_check)

if __name__ == "__main__":
    app = AppScanner()
    app.mainloop() 