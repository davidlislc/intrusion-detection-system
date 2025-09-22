# Intrusion Detection System with Tracking Capabilities

This project implements an Intrusion Detection System (IDS) using the Ultralytics YOLO model for object detection and tracking. The system processes video feeds to identify and track potential intrusions in real-time.

## Project Structure

```
intrusion-detection-system
├── src
│   ├── main.py                # Entry point of the application
│   ├── detection              # Contains detection-related functionalities
│   │   ├── __init__.py
│   │   ├── detector.py        # Object detection using YOLO
│   │   └── tracker.py         # Object tracking across frames
│   ├── models                 # Contains model-related functionalities
│   │   ├── __init__.py
│   │   └── yolo_model.py      # YOLO model loading and prediction
│   ├── utils                  # Utility functions
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration loading
│   │   └── video_utils.py     # Video input/output operations
│   └── alerts                 # Alerting functionalities
│       ├── __init__.py
│       └── notification.py     # Sending alerts based on detections
├── config
│   └── settings.yaml          # Configuration settings for the application
├── data
│   └── videos                 # Directory for storing video files
├── models
│   └── weights                # Directory for storing YOLO model weights
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your video files in the `data/videos` directory.
2. Configure the settings in `config/settings.yaml` as needed.
3. Run the application:

```bash
python src/main.py
```

The system will start processing the video feeds and will send alerts for any detected intrusions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

##Usage
Install dependencies:

pip install -r requirements.txt
Configure your intrusion zone in settings.yaml by adjusting the polygon points

Run the system:


python src/main.py
The system will:

Use your live camera feed
Track persons using YOLO
Detect when someone enters the defined intrusion zone
Send visual and voice alerts
Display tracking trails and zone boundaries