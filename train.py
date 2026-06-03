from ultralytics import YOLO

def main():
    # Carrega os pesos limpos do YOLOv11 nano
    model = YOLO("yolo11n.pt")

    # Dispara o treinamento alterado para rodar no processador (CPU)
    model.train(
        data="safework_data.yaml", 
        epochs=100,        # Quantidade ideal de épocas
        imgsz=640,         # Resolução padrão
        device="cpu",      # Mudamos aqui! Agora o Python aceitará o comando sem reclamar de placa de vídeo
        workers=2          # Ajustado para ficar leve e estável na CPU
    )

if __name__ == "__main__":
    main()