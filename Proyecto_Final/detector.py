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

        detection_timers = {} 

        # Tiempo mínimo para calcular promedio (en segundos)
        MIN_TIME_AREA1 = 3  # 3 segundos     

        MIN_TIME_AREA2 = 5
        TOLERANCE = 50
        time_spent_by_person = {} # La clave es una combinación de las coordenadas del centro (xc, yc) para identificar a cada persona

        # Inicializamos un DataFrame vacío
        #data = pd.DataFrame(columns=["timestamp", "person_id", "entry_time", "exit_time", "duration"])

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
            #Cambia el tamanio
            frame = cv2.resize(frame, (1020, 500))

            # Realizar inferencia con YOLOv8
            results = self.model(frame)
            person_boxes = get_bboxes(results)

            current_time = time.time()
            updated_timers = {}
            #Variables para contar por cada frame las personas en la region 2
            detections_area2 = 0

            for box in person_boxes:
                xc, yc = get_center(box)

                # Verificaciones de detección y dibujo
                if valid_detection(xc, yc, coords_area1):
                    center_key = (xc, yc)
                    #MODIFICACION NUEVA
                    for key in time_spent_by_person.keys():
                        if abs(key[0] - xc) <= TOLERANCE and abs(key[1] - yc) <= TOLERANCE:        
                            center_key=key                    
                            """print("Entra tolerancia-------------")
                            break
                        else:
                            print("Nuevo centro-------------")"""
                    #HASTA AQUI
                    
                    # Calcula el tiempo transcurrido desde la primera detección
                    elapsed_time = time_detection(center_key, xc, yc, current_time, detection_timers, updated_timers)
                    if elapsed_time >= MIN_TIME_AREA1:
                        #print(f"Tiempo--------------------: {int(elapsed_time)} segundos")
                        time_spent_by_person[center_key] = elapsed_time

                    """print("Contenido de time_spent_by_person:")
                    for key, value in time_spent_by_person.items():
                        print(f"Clave: {key}, Valor: {value}")"""

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

                    """if elapsed_time >= MIN_TIME_AREA1:
                        if center_key not in average_times:
                            average_times[center_key] = []
                        average_times[center_key].append(elapsed_time)
                        avg_time = sum(average_times[center_key]) / len(average_times[center_key])
                        
                        cv2.putText(
                            frame,
                            text=f"Tiempo Prom: {avg_time:.1f} s",
                            org=(box[0], box[1] - 30),
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=1.5,
                            color=(233, 196, 106),
                            thickness=2
                        )"""

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

                    if elapsed_time >= MIN_TIME_AREA2:
                        detections_area2 += 1

                    """cv2.putText(
                        frame,
                        text=f"Personas en area 2: {detections_area2}",
                        org=(50, 50),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=2,
                        color=(0, 255, 255),
                        thickness=2
                    )"""

                # Dibujar punto central y rectángulo de detección
                cv2.circle(frame, center=(xc, yc), radius=5, color=(0, 255,0), thickness=1)
                xmin, ymin, xmax, ymax = box
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255,0), 2)
            #ESTO TAMBIEN SE AGREGO
            valid_times = [time for time in time_spent_by_person.values() if time > 0]

            """for t in time_spent_by_person.keys():
                print(f"Key-Value: {t} {time_spent_by_person[t]}" )
            
            print(f"Values: {valid_times}" )"""

            # Calcular el tiempo promedio solo si hay tiempos válidos
            if valid_times:
                avg_time = sum(valid_times) / len(valid_times) 
                #print(f"Promedio en ese momemto -------------------------Promedio: {avg_time:.2f} segundos")
            else:
                avg_time = 0

            update_param(avg_time, detections_area2)
            
            #print(f"Cantidad de personas: {len(valid_times)}, Promedio: {avg_time:.2f} segundos")

            """# Dibujar el tiempo promedio en pantalla
            cv2.putText(
                frame,
                text=f"Tiempo promedio: {avg_time:.1f} s",  
                org=(50, 90), 
                fontFace=cv2.FONT_HERSHEY_PLAIN,
                fontScale=2,  
                color=(0, 255, 0),  
                thickness=2
            ) 
            #HASTA AQUI"""
            
            detection_timers = updated_timers

            # Dibujar áreas
            coords_array_area1 = np.array(coords_area1, dtype=np.int32)
            coords_array_area2 = np.array(coords_area2, dtype=np.int32)
            
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
            
