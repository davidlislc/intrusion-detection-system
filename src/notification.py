import time
import pyttsx3
from threading import Thread
from collections import defaultdict

class Notification:
    def __init__(self, alert_type, recipient):
        self.alert_type = alert_type
        self.recipient = recipient

    def send_alert(self, message):
        # Logic to send alert (e.g., email, SMS, etc.)
        print(f"Sending {self.alert_type} alert to {self.recipient}: {message}")

class AlertManager:
    def __init__(self, config):
        self.config = config
        self.last_alert_time = defaultdict(float)
        self.cooldown = config['alerts']['cooldown_seconds']
        
        if config['alerts']['voice_alerts']:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.8)
        else:
            self.engine = None
    
    def process_detections(self, detections, frame):
        current_time = time.time()
        
        for detection in detections:
            if detection['in_zone']:
                track_id = detection['track_id']
                
                # Check cooldown
                if current_time - self.last_alert_time[track_id] >= self.cooldown:
                    self.send_alert(detection)
                    self.last_alert_time[track_id] = current_time
    
    def send_alert(self, detection):
        alert_message = f"INTRUSION DETECTED! Person ID {detection['track_id']} in restricted zone"
        print(f"[ALERT] {alert_message}")
        
        if self.engine and self.config['alerts']['voice_alerts']:
            # Run TTS in separate thread to avoid blocking
            tts_thread = Thread(target=self._speak_alert, args=(detection,))
            tts_thread.daemon = True
            tts_thread.start()
    
    def _speak_alert(self, detection):
        message = f"Intrusion alert! Person detected in restricted zone"
        self.engine.say(message)
        self.engine.runAndWait()
    
    def cleanup(self):
        if self.engine:
            self.engine.stop()