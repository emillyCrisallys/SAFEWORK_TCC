from ultralytics import YOLO

def treinar_modelo():
    # 1. Carregar o modelo base do YOLOv11
    model = YOLO("yolo11n.pt")

    # 2. Iniciar o treinamento
    model.train(
        data="dataset/safework_data.yaml", 
        epochs=50,       # Comece com 50 para testar a velocidade
        imgsz=640,       # Tamanho padrão do YOLO
        batch=16,        # Quantidade de imagens processadas por vez
        project="models", # Onde salvar o resultado
        name="safework_v1"
    )

if __name__ == "__main__":
    treinar_modelo()