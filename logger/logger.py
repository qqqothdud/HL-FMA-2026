import csv
import os

def save_log(
    frame,
    sensor_data,
    command,
    mission_state,
    lane_center,
    stop_line_detected
):

    file_exists = os.path.exists("log.csv")

    with open("log.csv", "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "time",
                "x",
                "y",
                "yaw",
                "speed",
                "steer",
                "accel",
                "brake",
                "target_speed",
                "mission_state",
                "stop_line_detected"
            ])

        writer.writerow([
            time,
            sensor_data["x"],
            sensor_data["y"],
            sensor_data["yaw"],
            sensor_data["speed"],
            command["steer"],
            command["accel"],
            command["brake"],
            command["target_speed"],
            mission_state,
            stop_line_detected
        ])

    print(f"[Loop {time + 1}] 로그 저장 완료!")