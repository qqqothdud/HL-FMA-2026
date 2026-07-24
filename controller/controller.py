def control(sensor_data, mission_state, lane_center, config):

    max_speed = config["vehicle"]["max_speed"]
    min_speed = config["vehicle"]["min_speed"]
    corner_gain = config["speed_control"]["corner_gain"]

    image_center = 320
    error = lane_center - image_center
    kp = config["control"]["kp"]

    steer = error * kp

    # Corner Speed Control
    steer_abs = abs(steer)
    target_speed = max(
        min_speed,
        max_speed - steer_abs * corner_gain
    )

    accel = 0.4
    brake = 0.0

    if mission_state == "STOP":
        accel = 0.0
        brake = 1.0
        target_speed = 0.0

    command = {
        "steer": steer,
        "target_speed": target_speed,
        "accel": accel,
        "brake": brake
    }

    return command