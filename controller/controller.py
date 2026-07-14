def calculate_control (lane_deviation, current_speed):
   
    steer_angle = -0.5 * lane_deviation
    
    if abs(steer_angle) > 15:
        target_speed = 20.0
    else:
        target_speed = 50.0
    
    return steer_angle, target_speed

if __name__ == "__main__":
    steer,speed = calculate_control(10.0, 40.0)
    print(f"Steer: {steer}도, Speed: {speed}km/h")