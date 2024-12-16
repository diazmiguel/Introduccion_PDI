import matplotlib.path as mlpPath
import time
import pandas as pd
import cv2

#Leemos el modelo Yolov8
#def load_model():
 #   model = YOLO('yolov8n.pt')
  #  return model

#Para filtrar las clase persona y con un nivel de confianza 
def get_bboxes(results):
    # Filtrar las predicciones para obtener las cajas de 'person' con confianza > 0.35
    boxes = results[0].boxes
    # Extraer las coordenadas de las cajas y filtrar según la clase y la confianza
    person_boxes = [
        box.xyxy[0].cpu().numpy().astype(int)  # Coordenadas [xmin, ymin, xmax, ymax]
        for box in boxes
        if box.conf[0] >= 0.35 and box.cls[0] == 0  # Filtra clase 'person' (índice 0) y confianza
    ]

    return person_boxes

#Para obtener el punto centro
def get_center(bbox):
    # Coordenadas [xmin, ymin, xmax, ymax]
    #               0      1    2       3
    center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
    return center

#Detectar si el punto central entra al area de interes 
def valid_detection(xc, yc, coords):
    return mlpPath.Path(coords).contains_point((xc, yc))

""" def dataSet():
    if center_key not in updated_timers:
        person_id = active_people.pop(center_key, None)
        if person_id:
            exit_time = current_time
            entry_time = detection_timers[matched_key]
            duration = exit_time - entry_time

            # Guardar datos en el DataFrame
            data = pd.concat([data, pd.DataFrame({
                "timestamp": [current_time],
                "person_id": [person_id],
                "entry_time": [entry_time],
                "exit_time": [exit_time],
                "duration": [duration]
                })], ignore_index=True)
            
    # Mostrar estadísticas en pantalla (opcional)
            if len(data) > 0:
                    average_duration = data["duration"].mean()
                    total_people = len(data)
                    cv2.putText(
                        frame,
                        text=f"Promedio tiempo: {average_duration:.2f}s | Total personas: {total_people}",
                        org=(50, 100),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=1.5,
                        color=(255, 255, 0),
                        thickness=2
                    )

        # Exportar el dataset a CSV para análisis posterior
        data.to_csv("detections.csv", index=False)

        # Agrupar por intervalos de 5 minutos
        data["interval"] = (data["timestamp"] // 300).astype(int)  # Intervalos de 5 minutos (300s)
        # Agrupar por intervalos y calcular estadísticas
        stats = data.groupby("interval").agg(
            total_personas=("person_id", "count"),
            promedio_tiempo=("duration", "mean")
        )

        # Mostrar las estadísticas en consola
        print(f'Intervalos y Estadísticas',stats)
    return data """

#Para calcular el tiempo que pasa cada persona en el area 1
def time_detection(center_key, xc, yc, current_time, detection_timers, updated_timers):

    # Busca si hay alguna posición previa cercana, en el diccionario de tiempos
    matched_key = None 

    # Umbral de tolerancia para considerar la misma persona (en píxeles)
    TOLERANCE = 50

    for key in detection_timers.keys():
        if abs(key[0] - xc) <= TOLERANCE and abs(key[1] - yc) <= TOLERANCE: 
            matched_key = key
            break

    #Si encuentra una posición previa cercana, mantiene su tiempo inicial
    if matched_key:
        updated_timers[center_key] = detection_timers[matched_key]
        #Si es una nueva detección, registra el tiempo actual como inicio
    else:
        updated_timers[center_key] = current_time    

    # Calcula el tiempo transcurrido desde la primera detección
    elapsed_time = int(current_time - updated_timers[center_key])
    return elapsed_time