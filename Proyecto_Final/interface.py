import cv2
from coordinates import Coordinates
from detector import Detector
import tkinter as tk
from tkinter import filedialog

class Interface:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Monitoreo de Personas - IPDI")
        self.ventana.geometry("1380x768")
        self.ventana.config(bg="#333333")

        # Canvas para mostrar el video
        self.canvas = tk.Canvas(self.ventana, width=1280, height=600, bg="gray")
        self.canvas.pack(pady=10)

        # Frame para botones
        self.frame_botones = tk.Frame(self.ventana, bg="#333333")
        self.frame_botones.pack(pady=10)

        # Botón de abrir video
        self.btn_abrir = tk.Button(self.frame_botones, text="Abrir Video", command=self.open_video, width=20, height=2)
        self.btn_abrir.pack(side=tk.LEFT, padx=10)

        # Botón de salir
        self.btn_salir = tk.Button(self.frame_botones, text="Salir", command=self.exit_video, width=20, height=2)
        self.btn_salir.pack(side=tk.LEFT, padx=10)
        
        self.tiempo_label = tk.Label(self.frame_botones, 
                               text="Tiempo Prom.(Area1): 0  ", 
                               bg="#333333", 
                               fg="white", 
                               font=("Helvetica", 20))
        self.tiempo_label.pack(side=tk.LEFT, padx=20)

        self.personas_label = tk.Label(self.frame_botones, 
                               text="Personas (Area2): 0  ", 
                               bg="#333333", 
                               fg="white", 
                               font=("Helvetica", 20))
        self.personas_label.pack(side=tk.LEFT, padx=20)

        # Variables para el video y detección
        self.video_path = None
        self.cap = None
        self.detector = None
        self.coords1 = None
        self.coords2 = None

    def update_param(self, avg_time, cant_person):
        self.tiempo_label.config(text=f"Tiempo Prom.(Area1): {avg_time:.2f}")
        self.personas_label.config(text=f"Cant. Personas (Area2): {cant_person}")


    def open_video(self):
        # Abrir diálogo para seleccionar video
        self.video_path = filedialog.askopenfilename( filetypes=[("Video Files", "*.mp4 ; *.avi ; *.mov")])
        
        if self.video_path:
            # Abrir el video
            self.cap = cv2.VideoCapture(self.video_path)
            
            # Obtener coordenadas
            coord1 = Coordinates(self.video_path)
            coord2 = Coordinates(self.video_path)
            
            # Obtener las coordenadas de las áreas
            self.coords1 = coord1.get_coordinates()
            self.coords2 = coord2.get_coordinates()
            
            # Inicializar detector
            self.detector = Detector()
            
            # Comenzar reproducción del video con detección
            self.play_video()

    def play_video(self):
        if self.cap is not None and self.detector is not None:
            # Ejecutar la detección de personas
            self.detector.run(self.cap, self.coords1, self.coords2, self.canvas, self.update_param)

    def exit_video(self):
        # Detener cualquier detección en curso
        self.is_detecting = False
        
        # Liberar recursos de OpenCV
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Cerrar la ventana de Tkinter
        self.ventana.quit()
        self.ventana.destroy()

    def run(self):
        # Iniciar el bucle de la interfaz
        self.ventana.mainloop()
