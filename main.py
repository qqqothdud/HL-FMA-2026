import time
from mission.mission import mission_planning
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.geometry import calculate_distance
from planning.mission_manager import MissionManager
from enum import Enum

class MissionState(Enum):
    START = "START"
    LANE_FOLLOW = "LANE_FOLLOW"
    STOP_DETECTED = "STOP_DETECTED"
    OBSTACLE_AVOID = "OBSTACLE_AVOID"
    FINISH = "FINISH"

def main():
    print("=== 자율주행 파이프라인 시작 ===")
    
    config = load_config()
    mission_manager = MissionManager()
    
    sensor_data = {
        "x": 12.3,
        "y": 4.8,
        "yaw": 1.57,
        "speed": 8.5,
        "camera": None,
        "obstacles": []
    }
    
    waypoint = {
        "x": 20,
        "y": 10
    }

    # 메인 루프 실행 (기존 밖에서 돌던 코드와 아래 있던 코드를 통합)
    for i in range(1, 101):
        # 1. 센서 더미 데이터 업데이트
        sensor_data["x"] += 0.5
        sensor_data["y"] += 0.2
        sensor_data["speed"] += 0.1
        sensor_data["stop_line_detected"] = (i >= 50)
        
        distance = calculate_distance(sensor_data, waypoint)
        
        # 2. 미션 상태 판단 연결 (반환되는 current_state가 바로 Enum 객체임)
        current_state, target_speed = mission_manager.update_state(sensor_data)
        
        # 3. 제어 명령 계산
        steer, throttle, brake = control(sensor_data, current_state, config)
        
        command = {
            "steer": steer,
            "throttle": throttle,
            "brake": brake
        }
        
        # 4. [핵심] mission_state를 로그에 저장하도록 save_log 호출
        save_log(
            i,
            sensor_data,
            steer,
            current_state  # 현재 Enum 상태값을 바로 던져줌
        )
        
        # 확인용 출력
        print("=" * 40)
        print(f"Loop : {i}")
        print(f"목표 Waypoint까지 남은 거리: {distance:.2f}")
        
        print("[Sensor]")
        print(f"x      : {sensor_data['x']:.2f}")
        print(f"y      : {sensor_data['y']:.2f}")
        print(f"yaw    : {sensor_data['yaw']:.2f}")
        print(f"speed  : {sensor_data['speed']:.2f}")
        
        print("[Mission]")
        print(f"상태: {current_state.value:<16} | 목표 속도: {target_speed}")
        
        print("[Command]")
        print(command)
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()