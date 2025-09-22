class Tracker:
    def __init__(self):
        self.tracked_objects = {}

    def track_objects(self, detections):
        for detection in detections:
            object_id = detection['id']
            if object_id not in self.tracked_objects:
                self.tracked_objects[object_id] = detection
            else:
                self.tracked_objects[object_id].update(detection)

    def get_tracked_objects(self):
        return self.tracked_objects