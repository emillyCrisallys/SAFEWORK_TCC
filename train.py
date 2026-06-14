from ultralytics import YOLO

def main():
    # Carrega os pesos limpos do YOLOv11 nano
    model = YOLO(r"runs\detect\train-4\weights\best.pt")

    # Dispara o treinamento alterado para rodar no processador (CPU)
    model.train(
        data="safework_data.yaml",
        epochs=30,         
        imgsz=640,
        device="cpu",
        workers=2,
        batch=8,            
        name="safework_treino_atualizado"
    )

if __name__ == "__main__":
    main()