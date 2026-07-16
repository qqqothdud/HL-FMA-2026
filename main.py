from logger.logger import save_log

sensor_data = {
    "x": 12.3,
    "y": 4.8,
    "yaw": 1.57,
    "speed": 8.5,
    "camera": None,
    "obstacles": []
}

for i in range(10):

    sensor_data["x"] += 0.5
    sensor_data["y"] += 0.2
    sensor_data["speed"] += 0.1

    save_log(
        i,
        sensor_data,
        0.15,
        "DRIVE"
    )

print("로그 저장 완료!")