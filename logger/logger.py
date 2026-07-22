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

        # 파일이 처음 생성될 때만 헤더 작성 (mission -> mission_state로 수정)
        if not file_exists:
            writer.writerow([
                "time",
                "x",
                "y",
                "yaw",
                "speed",
                "steer",
                "mission_state"
            ])

        # [수정] mission이 Enum 객체일 경우 문자열 값(.value)만 추출, 아니면 그냥 문자열 처리
        mission_str = mission.value if hasattr(mission, 'value') else str(mission)

        # 실제 데이터 저장 (혹시 모를 KeyError 방지를 위해 .get() 사용)
        writer.writerow([
            time,
            sensor_data.get("x", 0.0),
            sensor_data.get("y", 0.0),
            sensor_data.get("yaw", 0.0),
            sensor_data.get("speed", 0.0),
            steer,
            mission_str
        ])

    print(f"[Loop {time}] 로그 저장 완료!")