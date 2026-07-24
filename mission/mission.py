def mission_planning(sensor_data, stop_line_detected):

    if stop_line_detected:
        return "STOP"

    return "DRIVE"