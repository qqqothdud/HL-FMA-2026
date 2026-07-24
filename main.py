from mission.mission import mission_planning
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.geometry import calculate_distance
from simulator.simulator_interface import (
    get_sensor_data,
    send_command
)
config = load_config()

waypoint = {
    "x": 20,
    "y": 10
}

mission_state = "DRIVE"

for i in range(100):

    # 센서 데이터 읽기
    sensor_data = get_sensor_data()

    # Camera Frame 경로
    image = sensor_data["camera"]["front"]

    # Waypoint까지 거리 계산
    distance = calculate_distance(sensor_data, waypoint)

    # 정지선 호출
    binary_image = ...
    lane_center = detect_lane(binary_image)
    stop_line_detected = False

    # 현재 미션 결정
    mission_state = mission_planning(
        sensor_data,
        stop_line_detected,
        mission_state
    )

    # 제어 명령 생성
    command = control(
        sensor_data,
        mission_state,
        lane_center,
        config
    )

    # 차량 제어 명령 전송
    send_command(command)

    # 로그 저장
    save_log(
        i,
        sensor_data,
        command,
        mission_state,
        stop_line_detected
    )

    # 화면 출력
    print("\n" + "=" * 40)
    print(f"Loop {i + 1}/100")

    print("\n[Sensor]")
    print(f"x      : {sensor_data['x']:.2f}")
    print(f"y      : {sensor_data['y']:.2f}")
    print(f"yaw    : {sensor_data['yaw']:.2f}")
    print(f"speed  : {sensor_data['speed']:.2f}")

    print("\n[Waypoint]")
    print(f"x        : {waypoint['x']}")
    print(f"y        : {waypoint['y']}")
    print(f"distance : {distance:.2f} m")

    print("\n[Mission]")
    print(mission_state)

    print("\n[Command]")
    print(f"steer        : {command['steer']:.3f}")
    print(f"accel        : {command['accel']:.3f}")
    print(f"brake        : {command['brake']:.3f}")
    print(f"target_speed : {command['target_speed']:.2f}")

    print("=" * 40)