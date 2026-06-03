from ultralytics import YOLO


model = YOLO(r"C:\Users\crisa\Documents\SAFEWORK_TCC\runs\detect\models\safework_v1-3\weights\best.pt")


results = model.predict(source="dataset/val/images", save=True, conf=0.25)

print("Detecção concluída! Veja os resultados na pasta 'runs/detect/predict'")