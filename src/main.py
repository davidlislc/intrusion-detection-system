import cv2
import yaml
from pathlib import Path
from detector import IntrusionDetector
from config import load_config
from notification import AlertManager

def main():
    # Load configuration
    config = load_config()
    # Initialize detector and alert manager
    detector = IntrusionDetector(config)
    alert_manager = AlertManager(config)
    
    # Initialize camera
    camera_source = config['camera']['source']
    cap = cv2.VideoCapture(camera_source)
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['camera']['resolution']['width'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['camera']['resolution']['height'])
    cap.set(cv2.CAP_PROP_FPS, config['camera']['fps'])
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_source}")
        return
    
    print("Starting intrusion detection system...")
    print("Press 'q' to quit, 's' to save current frame")
    
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from camera")
                break
            
            frame_count += 1
            
            # Process frame for intrusion detection
            detections, annotated_frame = detector.process_frame(frame, frame_count)
            
            # Check for intrusions and send alerts
            if detections:
                alert_manager.process_detections(detections, frame)
            
            # Display the frame
            cv2.imshow('Intrusion Detection System', annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                cv2.imwrite(f'intrusion_frame_{frame_count}.jpg', annotated_frame)
                print(f"Frame saved as intrusion_frame_{frame_count}.jpg")
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        alert_manager.cleanup()

if __name__ == "__main__":
    main()