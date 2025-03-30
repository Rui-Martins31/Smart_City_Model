import cv2
import tkinter as tk
import time
from PIL import Image, ImageTk
from ultralytics import YOLO
import paho.mqtt.client as mqtt  # MQTT library

# Set callback API version to 2
mqtt.Client.callback_api_version = 2

# --- MQTT Configuration ---
broker_address = "127.0.0.1"  # Change this to your MQTT broker address
broker_port = 1883  # Default MQTT port
mqtt_topic = "detection/events"  # MQTT topic to publish detection messages

# Create and connect MQTT client
mqtt_client = mqtt.Client("RaspberryPiClient")
mqtt_client.connect(broker_address, broker_port, keepalive=60)
mqtt_client.loop_start()  # Start MQTT network loop in a background thread

# --- YOLO Setup ---
weights = "ESISTmodelo.pt"
model = YOLO(weights)

# Open two cameras
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

# Check if cameras opened successfully
if not cap1.isOpened():
    print("Warning: Camera 1 not accessible!")
if not cap2.isOpened():
    print("Warning: Camera 2 not accessible!")

# Set camera resolution for both
frame_width, frame_height = 640, 480
for cap in (cap1, cap2):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Define 4 fixed detection zones
box_size = (100, 100)  # Width, Height
random_boxes = [
    (50, 50, 50 + box_size[0], 50 + box_size[1]),  # Top-left
    (frame_width - 50 - box_size[0], 50, frame_width - 50, 50 + box_size[1]),  # Top-right
    (100, frame_height - 100 - box_size[1], 100 + box_size[0], frame_height - 100),  # Bottom-left
    (frame_width - 100 - box_size[0], frame_height - 100 - box_size[1], frame_width - 100, frame_height - 100)  # Bottom-right
]
box_labels = ["Zone A", "Zone B", "Zone C", "Zone D"]

# Create Tkinter window
window = tk.Tk()
window.title("YOLOv8 Live Detection - Dual Cameras")

# Create Canvas for Camera 1
canvas1 = tk.Canvas(window, width=frame_width, height=frame_height)
canvas1.grid(row=0, column=0)
fps_label1 = tk.Label(window, text="FPS1: --", font=("Arial", 12))
fps_label1.grid(row=1, column=0)
msg_label1 = tk.Label(window, text="", font=("Arial", 12), fg="red")
msg_label1.grid(row=2, column=0)

# Create Canvas for Camera 2
canvas2 = tk.Canvas(window, width=frame_width, height=frame_height)
canvas2.grid(row=0, column=1)
fps_label2 = tk.Label(window, text="FPS2: --", font=("Arial", 12))
fps_label2.grid(row=1, column=1)
msg_label2 = tk.Label(window, text="", font=("Arial", 12), fg="red")
msg_label2.grid(row=2, column=1)

prev_time1, prev_time2 = time.time(), time.time()

def is_inside_roi(x1, y1, x2, y2):
    """Check if the bounding box is inside any of the 4 ROIs."""
    for idx, (bx1, by1, bx2, by2) in enumerate(random_boxes):
        if bx1 < x1 < bx2 and by1 < y1 < by2:
            return True, box_labels[idx]
    return False, None

def process_frame(frame, canvas, msg_label, fps_label, prev_time):
    """Process frame for YOLO detection, update canvas, and publish MQTT message on detection."""
    detected = False
    detected_label = ""
    results = model(frame)
    annotated_frame = frame.copy()

    # Draw fixed detection zones
    for i, (bx1, by1, bx2, by2) in enumerate(random_boxes):
        cv2.rectangle(annotated_frame, (bx1, by1), (bx2, by2), (255, 0, 0), 2)
        cv2.putText(annotated_frame, box_labels[i], (bx1, by1 - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Process detections
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            inside, box_label = is_inside_roi(x1, y1, x2, y2)
            if inside:
                detected = True
                detected_label = box_label
                conf = box.conf[0].item()
                class_id = int(box.cls[0])
                object_label = f"{model.names[class_id]}: {conf:.2f}"
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, object_label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Detected in: {box_label}", (x1, y1 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
                # Publish detection event to MQTT broker
                mqtt_msg = f"{model.names[class_id]} detected in {box_label} with confidence {conf:.2f}"
                mqtt_client.publish(mqtt_topic, mqtt_msg)

    # Update Tkinter canvas with annotated frame
    img_pil = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)))
    canvas.create_image(0, 0, anchor=tk.NW, image=img_pil)
    canvas.imgtk = img_pil
    msg_label.config(text=f"Object in {detected_label}" if detected else "")
    
    # Calculate and update FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
    fps_label.config(text=f"FPS: {fps:.2f}")
    return curr_time

def update_frames():
    global prev_time1, prev_time2
    if cap1.isOpened():
        ret1, frame1 = cap1.read()
        if ret1:
            prev_time1 = process_frame(frame1, canvas1, msg_label1, fps_label1, prev_time1)
    if cap2.isOpened():
        ret2, frame2 = cap2.read()
        if ret2:
            prev_time2 = process_frame(frame2, canvas2, msg_label2, fps_label2, prev_time2)
    window.after(10, update_frames)

def on_closing():
    cap1.release()
    cap2.release()
    mqtt_client.loop_stop()  # Stop MQTT network loop
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
update_frames()
window.mainloop()
