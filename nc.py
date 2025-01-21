import tkinter as tk
from tkinter import messagebox
import socket
import threading
import re

class PortListenerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Dinleyici")
        self.root.geometry("400x300")
        
        # Ana frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Port giriş alanı
        self.port_label = tk.Label(self.main_frame, text="Port Numarası (1024-9999):")
        self.port_label.pack(pady=5)
        
        self.port_entry = tk.Entry(self.main_frame)
        self.port_entry.pack(pady=5)
        
        # Dinleme butonu
        self.listen_button = tk.Button(self.main_frame, text="Dinlemeye Başla", command=self.start_listening)
        self.listen_button.pack(pady=10)
        
        # Durum mesajları için text alanı
        self.status_text = tk.Text(self.main_frame, height=10, width=40)
        self.status_text.pack(pady=10)
        
        self.listening = False
        self.server_socket = None
        
    def validate_port(self, port_str):
        try:
            port = int(port_str)
            if 1024 <= port <= 9999:
                return True
            return False
        except ValueError:
            return False
    
    def append_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
    
    def listen_for_connections(self, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(5)
            
            self.append_status(f"[{port}] Dinleniyor...")
            
            while self.listening:
                try:
                    client_socket, address = self.server_socket.accept()
                    self.append_status(f"[+] Bağlantı: {address[0]}")
                    client_socket.close()
                except:
                    break
                    
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Hata", f"Bağlantı hatası: {str(e)}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def start_listening(self):
        if self.listening:
            self.listening = False
            if self.server_socket:
                self.server_socket.close()
            self.listen_button.config(text="Dinlemeye Başla")
            self.append_status("Dinleme durduruldu.")
            return
        
        port_str = self.port_entry.get().strip()
        
        if not self.validate_port(port_str):
            messagebox.showerror("Hata", "Lütfen 1024-9999 arasında geçerli bir port numarası girin.")
            return
        
        port = int(port_str)
        self.listening = True
        self.listen_button.config(text="Durdur")
        
        # Dinleme işlemini ayrı bir thread'de başlat
        threading.Thread(target=self.listen_for_connections, args=(port,), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PortListenerGUI(root)
    root.mainloop()
