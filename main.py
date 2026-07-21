from mission.mission import mission_planning
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.geometry import calculate_distance

config = load_config()

sensor_data = {
    "x": 12.3,
    "y": 4.8,
    "yaw": 1.57,
    "speed": 8.5,
    "camera": None,
    "obstacles": []
}

waypoint = {
    "x": 20,
    "y": 10
}

for i in range(10):

    sensor_data["x"] += 0.5
    sensor_data["y"] += 0.2
    sensor_data["speed"] += 0.1

    distance = calculate_distance(
    sensor_data,
    waypoint
    )    

    print(distance)

    mission = mission_planning(sensor_data)
    steer, throttle, brake = control(sensor_data, mission, config)

    command = {
    "steer": steer,
    "throttle": throttle,
    "brake": brake
    }

    save_log(
    i,
    sensor_data,
    steer,
    mission
    )

    print("=" * 40)
    print(f"Loop : {i+1}")

    print("[Sensor]")
    print(f"x      : {sensor_data['x']:.2f}")
    print(f"y      : {sensor_data['y']:.2f}")
    print(f"yaw    : {sensor_data['yaw']:.2f}")
    print(f"speed  : {sensor_data['speed']:.2f}")

    print("[Mission]")
    print(mission)

    print("[Command]")
    print(command)

    print("=" * 40)

    print(config)