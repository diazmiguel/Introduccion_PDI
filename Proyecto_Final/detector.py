import cv2
import numpy as np
import time
import pandas as pd
from ultralytics import YOLO
from utils import get_bboxes, get_center, valid_detection, time_detection
import tkinter as tk
from PIL import Image, ImageTk

class Detector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')

    def run(self, cap, coords_area1, coords_area2, canvas, update_param):
        #print(f"Coordenadas", coords_area1, coords_area2)
        count = 0 
        detection_timers = {} # Diccionario para rastrear tiempo de detección de personas

        # Tiempo mínimo para calcular promedio (en segundos)
        MIN_TIME_AREA1 = 3  # 3 segundos     
        MIN_TIME_AREA2 = 5
        TOLERANCE = 50
        time_spent_by_person = {} # La clave es una combinación de las coordenadas del centro (xc, yc) para identificar a cada persona

        # Inicializamos un DataFrame vacío
        data = pd.DataFrame(columns=["timestamp", "person_id", "entry_time", "exit_time", "duration"])

        #Recorre los fotogramas del vídeo
        while cap.isOpened():
            # Leer fotograma del video
            success, frame = cap.read()
            if not success:
                break
            #Ayuda a saltar frames, para mas velocidad
            count += 1
            if count % 3 != 0:
                continue
            #Reconfigura a una resolucion fija
            frame = cv2.resize(frame, (1020, 500))

            # Realizar inferencia con YOLOv8
            results = self.model(frame)
            person_boxes = get_bboxes(results)
            # Variables para contar personas en el área
            current_time = time.time()

            updated_timers = {}# Actualizar el tiempo de detección para las personas dentro del área
            detections_area2 = 0 #Para contar por cada frame las personas en la region 2
            # Si se encontraron cajas de personas, dibujar sobre la imagen
            for box in person_boxes:
                xc, yc = get_center(box)#Obtenermos el centro

                # Verificaciones de detección y dibujo
                if valid_detection(xc, yc, coords_area1):
                    center_key = (xc, yc)#Crea una clave única basada en las coordenadas del centro  
                    #
                    for key in time_spent_by_person.keys():
                        if abs(key[0] - xc) <= TOLERANCE and abs(key[1] - yc) <= TOLERANCE:        
                            center_key=key                    
                    
                    # Calcula el tiempo transcurrido desde la primera detección
                    elapsed_time = time_detection(center_key, xc, yc, current_time, detection_timers, updated_timers)
                    if elapsed_time >= MIN_TIME_AREA1:
                        time_spent_by_person[center_key] = elapsed_time

                    # Dibuja el tiempo transcurrido sobre cada persona
                    cv2.putText(
                        frame,
                        text=f"Tiempo: {elapsed_time} s",
                        org=(box[0], box[1]-10),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=1.5,
                        color=(0, 255, 255),
                        thickness=2
                    )
                    
                # Verificar si está en el área 2
                if valid_detection(xc, yc, coords_area2):
                    center_key = (xc, yc)
                    elapsed_time = time_detection(center_key, xc, yc, current_time, detection_timers, updated_timers)
                    
                    cv2.putText(
                        frame,
                        text=f"Tiempo: {elapsed_time} s",
                        org=(box[0], box[1]-10),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=1.5,
                        color=(0, 255, 255),
                        thickness=2
                    )
                    #Si estuvo el suficiente tiempo se la cuenta en el area
                    if elapsed_time >= MIN_TIME_AREA2:
                        detections_area2 += 1

                # Dibujar punto central y rectángulo de detección
                cv2.circle(frame, center=(xc, yc), radius=5, color=(0, 255,0), thickness=1)
                xmin, ymin, xmax, ymax = box
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255,0), 2)
            #
            valid_times = [time for time in time_spent_by_person.values() if time > 0]

            # Calcular el tiempo promedio solo si hay tiempos válidos
            if valid_times:
                avg_time = sum(valid_times) / len(valid_times) 
                #print(f"Promedio en ese momemto -------------------------Promedio: {avg_time:.2f} segundos")
            else:
                avg_time = 0
            #Actualizamos los parametros para la interfaz
            update_param(avg_time, detections_area2)
            
            detection_timers = updated_timers

            # Asegúrarse de que coords sea un array numpy de tipo int32
            coords_array_area1 = np.array(coords_area1, dtype=np.int32)
            coords_array_area2 = np.array(coords_area2, dtype=np.int32)
            # Dibujar el polígono en la imagen 
            cv2.polylines(frame, [coords_array_area1], isClosed=True, color=(0, 0, 255), thickness=4)
            cv2.polylines(frame, [coords_array_area2], isClosed=True, color=(255, 0, 0), thickness=4)

            # Convertir y mostrar frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (1280, 600))
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)
            # Mostrar en el canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk
            # Actualizar la ventana
            canvas.update()
            
