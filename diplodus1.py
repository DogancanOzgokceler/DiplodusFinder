# 𓇋𓇍𓂻 𓅓 𓊵𓏏𓊪     
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
from ultralytics import YOLO
import os

class DiplodusFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diplodus Finder")
        self.root.geometry("400x380")
        self.root.configure(bg="#cceeff")
        self.root.resizable(False, False)

        self.image_path = None
        self.selected_model = None

        # Başlık
        tk.Label(root, text="Diplodus Finder'a Hoşgeldiniz", font=("Helvetica", 14, "bold"),
                 bg="#cceeff", fg="black").pack(pady=10)

        # Fotoğraf seçme alanı
        self.image_label = tk.Label(root, text="Fotoğraf yüklemek için tıklayın",
                                    bg="white", width=45, height=8, font=("Helvetica", 10, "bold"))
        self.image_label.pack(pady=10)
        self.image_label.bind("<Button-1>", self.select_image)

        # Model seçimi
                # Model seçimi
        tk.Label(root, text="Model Seçin:", font=("Helvetica", 10, "bold"), bg="#cceeff").pack(pady=5)

        # Buton çerçevesini ortalamak için anchor kullanılmadı, sadece pady ve padx ile hizalama yapıldı
        btn_frame = tk.Frame(root, bg="#cceeff")
        btn_frame.pack(pady=5)

        self.btn_v8 = tk.Button(btn_frame, text="YOLOv8", command=self.select_yolov8_model,
                                bg="black", fg="white", font=("Helvetica", 10, "bold"), width=10)
        self.btn_v8.grid(row=0, column=0, padx=10)
        self.btn_v8.bind("<Enter>", self.on_hover)
        self.btn_v8.bind("<Leave>", self.on_leave)

        self.btn_v11 = tk.Button(btn_frame, text="YOLOv11", command=self.select_yolov11_model,
                                 bg="black", fg="white", font=("Helvetica", 10, "bold"), width=10)
        self.btn_v11.grid(row=0, column=1, padx=10)
        self.btn_v11.bind("<Enter>", self.on_hover)
        self.btn_v11.bind("<Leave>", self.on_leave)


        # Model etiketi
        self.model_label = tk.Label(root, text="Seçili model: Yok", fg="blue",
                                    bg="#cceeff", font=("Helvetica", 10, "bold"))
        self.model_label.pack(pady=5)

        # Alt kısım için ayrı bir çerçeve
        bottom_frame = tk.Frame(root, bg="#cceeff")
        bottom_frame.pack(side="bottom", fill="x", pady=(5, 10))

        # İmza etiketi en altta
        self.signature_label = tk.Label(bottom_frame, text="Doğancan ÖZGÖKÇELER - 2025",
                                        font=("Helvetica", 10, "italic"),
                                        bg="#cceeff", fg="black")
        self.signature_label.pack(side="bottom", pady=(0, 3))

        # "Türü Tespit Et" butonu onun üstünde
        self.detect_button = tk.Button(bottom_frame, text="Türü Tespit Et", command=self.run_detection,
                                    bg="black", fg="white", font=("Helvetica", 13, "bold"), width=20, height=1)
        self.detect_button.pack(side="bottom", pady=(0, 5))
        self.detect_button.bind("<Enter>", self.on_hover)
        self.detect_button.bind("<Leave>", self.on_leave)

    def show_coming_soon(self):
        messagebox.showinfo("Bilgi", "Bu model yakında eklenecek.")

    def select_image(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Görseller", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image_path = file_path
            file_name = os.path.basename(file_path)
            self.image_label.config(text=f"Seçili Foto: {file_name}")

    def set_model(self, model_path, label=None):
        self.selected_model = model_path
        shown_name = label if label else model_path
        self.model_label.config(text=f"Seçili model: {shown_name}")

    def select_yolov8_model(self):
        models = {
            "En İyi Model": "DiplodusV8_Best.pt",
            "Genel Model": "DiplodusV8_last.pt"
        }

        popup = tk.Toplevel(self.root)
        popup.title("YOLOv8 Model Seçimi")
        popup.geometry("300x150")
        popup.configure(bg="#e6f2ff")

        tk.Label(popup, text="Model Seçin:", font=("Helvetica", 11, "bold"), bg="#e6f2ff").pack(pady=10)

        var = tk.StringVar(popup)
        var.set(list(models.keys())[0])

        dropdown = tk.OptionMenu(popup, var, *models.keys())
        dropdown.config(font=("Helvetica", 10))
        dropdown.pack(pady=5)

        def on_select():
            label = var.get()
            path = models[label]
            self.set_model(path, label=f"YOLOv8 - {label}")
            popup.destroy()

        tk.Button(popup, text="Seç", command=on_select,
                  bg="black", fg="white", font=("Helvetica", 10, "bold")).pack(pady=10)

    def select_yolov11_model(self):
        models = {
            "En İyi Model": "DiplodusV11_Best.pt",
            "Genel Model": "DiplodusV11_Last.pt"
        }

        popup = tk.Toplevel(self.root)
        popup.title("YOLOv11 Model Seçimi")
        popup.geometry("300x150")
        popup.configure(bg="#e6f2ff")

        tk.Label(popup, text="Model Seçin:", font=("Helvetica", 11, "bold"), bg="#e6f2ff").pack(pady=10)

        var = tk.StringVar(popup)
        var.set(list(models.keys())[0])

        dropdown = tk.OptionMenu(popup, var, *models.keys())
        dropdown.config(font=("Helvetica", 10))
        dropdown.pack(pady=5)

        def on_select():
            label = var.get()
            path = models[label]
            self.set_model(path, label=f"YOLOv11 - {label}")
            popup.destroy()

        tk.Button(popup, text="Seç", command=on_select,
                  bg="black", fg="white", font=("Helvetica", 10, "bold")).pack(pady=10)


    def run_detection(self):
        if not self.image_path:
            messagebox.showerror("Hata", "Lütfen bir fotoğraf seçin.")
            return
        if not self.selected_model:
            messagebox.showerror("Hata", "Lütfen bir model seçin.")
            return

        model = YOLO(self.selected_model)
        results = model(self.image_path, verbose=True)

        detected_classes = []
        confidences = []

        img_cv = cv2.imread(self.image_path)

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            name = model.names[cls_id]
            detected_classes.append(name)
            confidences.append(conf)

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{name} {conf*100:.1f}%"
            cv2.putText(img_cv, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if not detected_classes:
            messagebox.showinfo("Sonuç", "Hiç balık bulunamadı.")
            return

        max_index = confidences.index(max(confidences))
        best_confidence = confidences[max_index]
        if best_confidence < 0.70:
            messagebox.showwarning("Uyarı", "Yeterli güven oranı sağlanmadığından tür belirlenemedi !")
            return

        best_type = detected_classes[max_index]
        best_conf = best_confidence * 100
        count_by_type = {t: detected_classes.count(t) for t in set(detected_classes)}

        result_window = tk.Toplevel(self.root)
        result_window.title("Tanıma Sonucu")
        result_window.geometry("360x180")
        result_window.configure(bg="#f2f2f2")

        tk.Label(result_window, text=f"📌 Fotoğraftaki balık sayısı: {len(detected_classes)}",
                 font=("Helvetica", 11, "bold"), bg="#f2f2f2", justify="center").pack(pady=(20, 10))

        tk.Label(result_window, text="🐟 Tespit edilen balık türleri:",
                 font=("Helvetica", 10, "bold"), bg="#f2f2f2", justify="center").pack()

        for t, count in count_by_type.items():
            tk.Label(result_window, text=f"• {t}: {count} adet",
                     font=("Helvetica", 10, "bold"), bg="#f2f2f2", justify="center").pack()

        tk.Label(result_window, text="\n🎯 En yüksek doğruluk oranına sahip balık türü:",
                 font=("Helvetica", 10, "bold"), bg="#f2f2f2", justify="center").pack()
        tk.Label(result_window, text=f"{best_type} ({best_conf:.1f}%)",
                 font=("Helvetica", 10, "bold"), bg="#f2f2f2", justify="center").pack(pady=(0, 15))

        resized_img = cv2.resize(img_cv, (640, 640))
        cv2.imshow("Tespit Sonucu (YOLO)", resized_img)

        key = cv2.waitKey(0)
        if key != -1:
            cv2.destroyAllWindows()

    def on_hover(self, event):
        event.widget.config(bg="#444444")

    def on_leave(self, event):
        event.widget.config(bg="black")

# Başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = DiplodusFinderApp(root)
    root.mainloop()
