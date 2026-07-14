# Sensor 생성
def get_sensor_data():

    sensor = {
        "speed": 20,
        "yaw": 3.5,
        "lane_center": 318,
        "traffic_light": "green"
    }

    return sensor

# Mission 판단
def mission_planning(sensor):

    if sensor["traffic_light"] == "red":
        return "STOP"

    return "DRIVE"

# Command 생성
def controller(mission):

    if mission == "STOP":

        command = {
            "steer": 0,
            "speed": 0,
            "brake": 100
        }

    else:

        command = {
            "steer": 0,
            "speed": 20,
            "brake": 0
        }

    return command

# 변수 정의
sensor = get_sensor_data()

mission = mission_planning(sensor)

command = controller(mission)
sensor = get_sensor_data()

mission = mission_planning(sensor)

command = controller(mission)

# 출력
print("===== Sensor =====")
print(sensor)

print()

print("===== Mission =====")
print(mission)

print()

print("===== Command =====")
print(command)