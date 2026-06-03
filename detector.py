import cv2
import requests
from ultralytics import YOLO

# 1. Carrega o modelo com o caminho corrigido
model = YOLO(r"C:\Users\crisa\Documents\SAFEWORK_TCC\runs\detect\train-4\weights\best.pt")

# 2. Inicializa a Webcam
cap = cv2.VideoCapture(0)

print("Sistema SafeWork em execução. Pressione 'q' para sair.")

import time
ultima_infracao = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Processa a detecção
    results = model(frame, conf=0.5)

    # 4. Desenha na tela (para visualização no TCC)
    annotated_frame = results[0].plot()
    cv2.imshow("SafeWork TCC - Monitoramento", annotated_frame)

    # 5. Lógica de detecção e envio para a API
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            
           
            if label == "NO-Hardhat":
                tempo_atual = time.time()
                if tempo_atual - ultima_infracao > INTERVALO_MINIMO:
                    try:
                        print("Tentando registrar infração na API...")
                        response = requests.post(
                            "http://127.0.0.1:8000/detector/registrar-infracao", 
                            params={"tipo": label, "confianca": 0.9, "setor": "Linha_A"}
                        )
                    
                        print(f"Status da API: {response.status_code}") 
                        
                        if response.status_code == 200:
                            print("✅ Sucesso: Infração salva no banco!")
                            ultima_infracao = tempo_atual
                        else:
                            print(f"API retornou erro: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        print("❌ ERRO: Não consegui conectar na API. O FastAPI está rodando?")
                    except Exception as e:
                        print(f"❌ ERRO DESCONHECIDO: {e}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()