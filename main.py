import cv2
from ultralytics import YOLO
from src.database import salvar_deteccao
import time

# 1. Carrega o modelo padrão (YOLOv11 nano é leve para testes)
# Na primeira vez, ele vai baixar o arquivo yolov11n.pt automaticamente
model = YOLO('yolov11n.pt') 

def iniciar_monitoramento():
    # 0 é a webcam padrão. Para o TCC, depois usaremos a url_rtsp do banco
    cap = cv2.VideoCapture(0) 

    print("Monitoramento SafeWork iniciado...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        start_time = time.time()

        # 2. Executa a detecção no frame
        results = model(frame, verbose=False)
        
        processing_time = int((time.time() - start_time) * 1000)

        for result in results:
            for box in result.boxes:
                # Classe 0 no YOLO padrão é 'person'
                # Vamos fingir que detectar uma pessoa sem filtro é uma "falta de EPI" para testar
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if cls == 0 and conf > 0.5:
                    print(f"Detectado! Confiança: {conf:.2f}")

                    # 3. Monta o objeto para o banco conforme sua tabela 'deteccoes'
                    # Referência: SafeWork.sql
                    deteccao_data = {
                        'id_camera': 1,  # ID fictício para teste
                        'id_funcionario': None, # Ficará para a parte de Face ID
                        'tipo_falta_epi': 'Teste de Sistema',
                        'path_original': 'storage/test_orig.jpg',
                        'path_blur': 'storage/test_blur.jpg',
                        'confianca': conf,
                        'tempo_ms': processing_time
                    }

                    # 4. Salva no Postgres
                    salvar_deteccao(deteccao_data)
                    
                    # Desenha na tela para você ver acontecer
                    cv2.rectangle(frame, (int(box.xyxy[0][0]), int(box.xyxy[0][1])), 
                                 (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (0, 255, 0), 2)

        cv2.imshow("SafeWork - Monitoramento IA", frame)

        # Aperte 'q' para fechar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_monitoramento()