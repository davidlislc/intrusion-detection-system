class YoloModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        from ultralytics import YOLO
        self.model = YOLO(self.model_path)

    def predict(self, frame):
        if self.model is None:
            raise ValueError("Model is not loaded. Please call load_model() first.")
        results = self.model(frame)
        return results