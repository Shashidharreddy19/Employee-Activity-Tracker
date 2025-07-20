import cv2
import time
import mediapipe as mp
import csv

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Track multiple employees’ activity times
employees = {}

# Connect to webcam (0 for default cam, use 1/2 for external cam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)

    current_ids = []

    if results and results.detections:
        for i, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            current_ids.append(i)

            if i not in employees:
                employees[i] = {
                    'status': 'Rest',
                    'work_time': 0,
                    'rest_time': 0,
                    'start_time': time.time()
                }

            # Face direction logic
            face_center_x = x + w_box // 2
            screen_center_x = frame.shape[1] // 2
            face_direction_threshold = 100
            current_status = "Work" if abs(face_center_x - screen_center_x) < face_direction_threshold and detection.score[0] > 0.5 else "Rest"

            color = (0, 255, 0) if current_status == "Work" else (0, 0, 255)
            elapsed_time = time.time() - employees[i]['start_time']

            if current_status == employees[i]['status']:
                if current_status == "Work":
                    employees[i]['work_time'] += elapsed_time
                else:
                    employees[i]['rest_time'] += elapsed_time

            employees[i]['status'] = current_status
            employees[i]['start_time'] = time.time()

            # Draw bounding box and status info
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
            status_text = f"Employee {i+1}: {current_status}"
            time_text = f"Work: {int(employees[i]['work_time'])}s | Rest: {int(employees[i]['rest_time'])}s"
            cv2.putText(frame, status_text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, time_text, (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Score: {detection.score[0]:.2f}", (x, y + h_box + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    else:
        print("No faces detected")

    # Handle disappeared employees
    for emp_id in list(employees.keys()):
        if emp_id not in current_ids:
            employees[emp_id]['status'] = "Rest"

    # Show the frame
    cv2.imshow('Employee Activity Tracker', frame)

    # Exit on pressing ‘q’
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

# Final Report to console
print("\n--- Final Report ---")
for emp_id, data in employees.items():
    print(f"Employee {emp_id+1} – Total Work Time: {int(data['work_time'])}s, Total Rest Time: {int(data['rest_time'])}s")

# Save final report to a TXT file
with open("employee_activity_report.txt", "w") as file:
    file.write("--- Final Report ---\n")
    for emp_id, data in employees.items():
        file.write(
            f"Employee {emp_id+1} – Total Work Time: {int(data['work_time'])}s, "
            f"Total Rest Time: {int(data['rest_time'])}s\n"
        )

# Save final report to a CSV file
with open("employee_activity_report.csv", "w", newline='') as csvfile:
    fieldnames = ['Employee ID', 'Total Work Time (s)', 'Total Rest Time (s)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for emp_id, data in employees.items():
        writer.writerow({
            'Employee ID': emp_id + 1,
            'Total Work Time (s)': int(data['work_time']),
            'Total Rest Time (s)': int(data['rest_time']),
        })

print("Reports saved to 'employee_activity_report.txt' and 'employee_activity_report.csv'")
