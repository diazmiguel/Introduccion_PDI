import cv2

class Coordinates:
    def __init__(self, video_path: str):
         # Inicializa el objeto de captura de video
        self.cap = cv2.VideoCapture(video_path)
        self.coordinates = []  # Atributo para almacenar las coordenadas

        # Verifica si el video se ha abierto correctamente
        if not self.cap.isOpened():
            print("Error al abrir el video")
            return
        # Crea una ventana para mostrar el video
        cv2.namedWindow("Selecciona Area de interes")
        # Configura un callback para manejar eventos del ratón
        cv2.setMouseCallback("Selecciona Area de interes", self.print_coordinates)

        # Llama a la función video() para empezar a mostrar el video
        self.video()

    # Función para manejar los eventos del ratón
    def print_coordinates(self, event, x, y, flags, params):
        # Si se hace click izquierdo en la imagen, muestra las coordenadas (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            #print(f"[{x}, {y}],")
            self.coordinates.append([x, y])  # Guardar las coordenadas en la lista

    # Función principal para reproducir el video
    def video(self):
        while True:
            status, frame = self.cap.read()
            
            if not status:
                break

            frame=cv2.resize(frame,(1020,500)) #Solo cambia el tamano de reproduccion
            
            for coord in self.coordinates:
                #print(len(self.coordinates))
                cv2.circle(frame, coord, 5, (0, 0, 255), -1)

            cv2.imshow("Selecciona Area de interes", frame)

            #cv2.imshow("Frame", frame)
            #El valor 10 en cv2.waitKey(10) significa que OpenCV espera 10 milisegundos entre cada fotograma.
            if cv2.waitKey(10) & 0xFF == ord('q'): break
        
        cv2.destroyAllWindows() #Elimina la ventana

    def get_coordinates(self):
        return self.coordinates
    
    # Función para liberar los recursos cuando el objeto se destruye
    #def __del__(self):
        # Libera la captura de video
        #self.cap.release()
        # Cierra todas las ventanas de OpenCV
        #cv2.destroyAllWindows()

if __name__ == '__main__':
    # Inicia el objeto de la clase Coordinates pasando la ruta del video
    c = Coordinates("./inference/cr.mp4")

