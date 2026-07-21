from mission.mission import mission_planning
from controller.controller import control
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

    mission = mission_planning(sensor_data)
    steer, throttle, brake = control(sensor_data, mission)

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
    print(sensor_data)

    print("[Mission]")
    print(mission)

    print("[Command]")
    print(command)

    print("=" * 40)