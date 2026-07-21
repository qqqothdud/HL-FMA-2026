import csv
import os


def save_log(
    time,
    sensor_data,
    steer,
    mission
):

    file_exists = os.path.exists("log.csv")

    with open("log.csv", "a", newline="") as file:

        writer = csv.writer(file)

        # 파일이 처음 생성될 때만 헤더 작성
        if not file_exists:
            writer.writerow([
                "time",
                "x",
                "y",
                "yaw",
                "speed",
                "steer",
                "mission"
            ])

        # 실제 데이터 저장
        writer.writerow([
            time,
            sensor_data["x"],
            sensor_data["y"],
            sensor_data["yaw"],
            sensor_data["speed"],
            steer,
            mission
        ])


    print(f"[Loop {time + 1}] 로그 저장 완료!")