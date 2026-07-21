def control(sensor_data, mission, config):

    target_speed = config["vehicle"]["target_speed"]
    max_steer = config["vehicle"]["max_steer"]

    steer = 0.15

    throttle = target_speed / 25

    brake = 0.0

    return steer, throttle, brake