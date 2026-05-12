from ultralytics import YOLO

# 1. Carrega o modelo que você acabou de treinar
model = YOLO(r"C:\Users\crisa\Documents\SAFEWORK_TCC\runs\detect\models\safework_v1-3\weights\best.pt")

# 2. Faz a detecção em uma imagem (escolha uma que você não usou no treino)
results = model.predict(source="dataset/val/images", save=True, conf=0.25)

print("Detecção concluída! Veja os resultados na pasta 'runs/detect/predict'")