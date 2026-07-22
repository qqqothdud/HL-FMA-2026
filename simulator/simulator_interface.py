current_x = 12.3
current_y = 4.8
current_yaw = 1.57
current_speed = 8.5


def get_sensor_data():

    global current_x
    global current_y
    global current_yaw
    global current_speed

    # 차량이 조금씩 앞으로 이동
    current_x += 0.5
    current_y += 0.2

    sensor_data = {

        # GPS
        "x": current_x,
        "y": current_y,

        # 차량 방향
        "yaw": current_yaw,

        # 차량 속도
        "speed": current_speed,

        # Front Camera
        "camera": "camera/road.jpg"

    }

    return sensor_data

def send_command(command):

    print("\n===== Vehicle Command =====")

    print(f"Steer        : {command['steer']:.3f}")
    print(f"Accel        : {command['accel']:.3f}")
    print(f"Brake        : {command['brake']:.3f}")
    print(f"Target Speed : {command['target_speed']:.1f}")