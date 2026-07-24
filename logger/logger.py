import csv
import os


def save_log(
    time,
    sensor_data,
    command,
    mission,
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
                "mission",
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
            mission,
            stop_line_detected
        ])

    print(f"[Loop {time + 1}] 로그 저장 완료!")