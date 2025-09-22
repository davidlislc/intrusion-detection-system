import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict, deque

class IntrusionDetector:
    def __init__(self, config):
        self.config = config
        self.model = YOLO(config['detection']['model_path'])
        self.track_history = defaultdict(lambda: deque(maxlen=config['detection']['track_history']))
        self.intrusion_zone = np.array(config['zones']['intrusion_zone']['points'], np.int32)
        self.zone_color = config['zones']['intrusion_zone']['color']
        self.zone_thickness = config['zones']['intrusion_zone']['thickness']
        
    def process_frame(self, frame, frame_count):
        # Run YOLO tracking
        results = self.model.track(
            frame, 
            persist=True, 
            conf=self.config['detection']['confidence_threshold'],
            classes=[0]  # Only detect persons (class 0)
        )
        
        detections = []
        annotated_frame = frame.copy()
        
        # Draw intrusion zone
        cv2.polylines(annotated_frame, [self.intrusion_zone], True, self.zone_color, self.zone_thickness)
        cv2.fillPoly(annotated_frame, [self.intrusion_zone], (*self.zone_color[:3], 30))  # Semi-transparent fill
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confidences = results[0].boxes.conf.float().cpu().tolist()
            
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                x, y, w, h = box
                center_point = (int(x), int(y))
                
                # Store track history
                self.track_history[track_id].append(center_point)
                
                # Check if person is in intrusion zone
                is_in_zone = cv2.pointPolygonTest(self.intrusion_zone, center_point, False) >= 0
                
                if is_in_zone:
                    detections.append({
                        'track_id': track_id,
                        'center': center_point,
                        'bbox': (int(x - w/2), int(y - h/2), int(w), int(h)),
                        'confidence': conf,
                        'frame_count': frame_count,
                        'in_zone': True
                    })
                    
                    # Draw red bounding box for intrusion
                    bbox_color = (0, 0, 255)  # Red
                    label = f"INTRUSION! ID:{track_id} {conf:.2f}"
                else:
                    # Draw green bounding box for normal detection
                    bbox_color = (0, 255, 0)  # Green
                    label = f"Person ID:{track_id} {conf:.2f}"
                
                # Draw bounding box
                x1, y1 = int(x - w/2), int(y - h/2)
                x2, y2 = int(x + w/2), int(y + h/2)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), bbox_color, 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color, 2)
                
                # Draw track history
                points = list(self.track_history[track_id])
                if len(points) > 1:
                    for i in range(1, len(points)):
                        thickness = int(np.sqrt(64 / float(i + 1)) * 2)
                        cv2.line(annotated_frame, points[i-1], points[i], bbox_color, thickness)
                
                # Draw center point
                cv2.circle(annotated_frame, center_point, 5, bbox_color, -1)
        
        return detections, annotated_frame