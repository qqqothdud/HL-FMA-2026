def control(sensor_data, mission_state, lane_center, config):

    target_speed = config["vehicle"]["target_speed"]

    image_center = 320
    error = lane_center - image_center
    steer = error * 0.002

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