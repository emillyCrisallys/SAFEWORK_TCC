import cv2
from ultralytics import YOLO

model = YOLO(r"C:\Users\crisa\Documents\SAFEWORK_TCC\runs\detect\train-4\weights\best.pt")


cap = cv2.VideoCapture(0)

print("Iniciando detecção... Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5) # conf=0.5 filtra detecções abaixo de 50% de certeza


    annotated_frame = results[0].plot()

  
    cv2.imshow("SafeWork - Detecção em Tempo Real", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()