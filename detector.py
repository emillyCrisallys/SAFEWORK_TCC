import cv2
import requests
import time
import threading
import os
import unicodedata
from ultralytics import YOLO
from src.recognition import ReconhecedorFacial

MODEL_PATH = r"C:\users\gusta\onedrive\documentos\safework_tcc-main\safework_tcc-main\runs\detect\train-4\weights\best.pt"
API_URL = "http://127.0.0.1:8000/detector/registrar-infracao"
INTERVALO_MINIMO = 10 
ultima_infracao = 0

# Dicionário de tradução corrigido para coincidir com o 'if'
TRADUCOES = {
    "NO-Hardhat": "Sem Capacete",
    "Safety Cone": "Cone de Segurança",
    "Hardhat": "Capacete",
    "Mask": "Mascara",
    "Safety Vest": "Colete"
}

def limpar_texto(texto):
    nfkd = unicodedata.normalize('NFKD', str(texto))
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# Inicialização
model = YOLO(MODEL_PATH)
reconhecedor = ReconhecedorFacial(db_path="dataset/faces")
os.makedirs("storage/ocorrencias", exist_ok=True)

def enviar_alerta_assincrono(dados):
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        requests.post(API_URL, json=dados, headers=headers, timeout=5)
    except Exception as e:
        print(f"Erro na conexão com API: {e}")

print("SafeWork TCC em execução 24h. Pressione 'q' para sair.")

while True:
    try:
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Câmera desconectada. Tentando reconectar...")
                break

            results = model(frame, conf=0.5, verbose=False)
            annotated_frame = frame.copy()
            
            for result in results:
                for box in result.boxes:
                    # Tradução com fallback e limpeza
                    label_original = model.names[int(box.cls[0])]
                    label = TRADUCOES.get(label_original, label_original)
                    label_para_tela = limpar_texto(label) # Remove acentos para o OpenCV
                    
                    # Desenha retângulo e texto
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, label_para_tela, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Lógica de Infração (coincidindo com o dicionário)
                    if label in ["Sem Capacete", "Cone de Segurança"]: 
                        if time.time() - ultima_infracao > INTERVALO_MINIMO:
                            
                            nome_raw = reconhecedor.identificar_pessoa(frame)
                            nome_seguro = "".join(c for c in limpar_texto(nome_raw) if c.isalnum() or c in [' ', '_'])
                            
                            caminho_foto = f"storage/ocorrencias/infracao_{int(time.time())}.jpg"
                            cv2.imwrite(caminho_foto, frame)
                            
                            dados = {
                                "tipo": str(label), 
                                "confianca": float(box.conf[0]), 
                                "setor": "Linha_A",
                                "funcionario": nome_seguro,
                                "foto_path": caminho_foto
                            }
                            
                            threading.Thread(target=enviar_alerta_assincrono, args=(dados,), daemon=True).start()
                            ultima_infracao = time.time()

            cv2.imshow("SafeWork TCC - Monitoramento", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()
        
        cap.release()
        time.sleep(2)

    except Exception as e:
        print(f"Erro crítico no loop: {e}")
        time.sleep(5)