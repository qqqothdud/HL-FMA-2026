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

for i in range(100):

    # 매 반복마다 센서 읽기
    sensor_data = get_sensor_data()

    distance = calculate_distance(sensor_data, waypoint)

    print("[Waypoint]")
    print(f"x : {waypoint['x']}")
    print(f"y : {waypoint['y']}")
    print(f"distance : {distance:.2f} m")

    mission = mission_planning(sensor_data)

    command = control(sensor_data, mission, config)
    send_command(command)

    save_log(
        i,
        sensor_data,
        command,
        mission
    )

    print("\n" + "=" * 40)
    print(f"Loop : {i+1}/100")

    print("[Sensor]")
    print(f"x      : {sensor_data['x']:.2f}")
    print(f"y      : {sensor_data['y']:.2f}")
    print(f"yaw    : {sensor_data['yaw']:.2f}")
    print(f"speed  : {sensor_data['speed']:.2f}")

    print("[Mission]")
    print(mission)

    print("[Command]")
    

    print("\n" + "=" * 40)