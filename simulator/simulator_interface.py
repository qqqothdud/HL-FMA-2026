current_x = 12.3
current_y = 4.8
current_yaw = 1.57
current_speed = 8.5

def get_sensor_data():

    global current_x
    global current_y
    global current_yaw
    global current_speed

    current_x += 0.5
    current_y += 0.2

    sensor_data = {

        "x": current_x,
        "y": current_y,
        "yaw": current_yaw,
        "speed": current_speed

    }

    return sensor_data

def send_command(command):

    print()

    print("===== Vehicle Command =====")

    print(command)