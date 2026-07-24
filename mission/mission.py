def mission_planning(
    sensor_data,
    stop_line_detected,
    mission_state
):

    if mission_state == "DRIVE":

        if stop_line_detected:
            mission_state = "STOP"

    elif mission_state == "STOP":

        if sensor_data["speed"] < 0.1:  
            # 실제 시뮬레이터에서는 속도가 정확히 0.0이 되는 경우가 드물기 때문에, 작은 오차를 허용해서 안정화를 한다. 
            mission_state = "DRIVE"

    return mission_state