from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from ultralytics import YOLO
import io

app = FastAPI()

# Carregue o modelo UMA VEZ ao iniciar o servidor (não a cada requisição!)
model = YOLO('yolov11n.pt')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Lê os bytes da imagem que o Backend enviou
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 2. Executa a detecção (a mesma lógica que você tinha)
    results = model(frame, verbose=False)
    
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    # 3. Retorna o JSON para o seu Backend
    return {"status": "sucesso", "detections": detections}