from perception.lane_detector import (
    detect_lane,
    detect_stop_line
)

def run_perception(sensor_data):

    image = sensor_data["camera"]["front"]

    # OpenCV 구현 전
    binary_image = None

    lane_center = detect_lane(binary_image)
    stop_line_detected = detect_stop_line(binary_image)

    return lane_center, stop_line_detected