import time
from mission.mission import mission_planning
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.geometry import calculate_distance
from planning.mission_manager import MissionManager, MissionState

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

    for i in range(1, 101):
        # 더미 데이터 업데이트
        sensor_data["x"] += 0.5
        sensor_data["y"] += 0.2
        
        # 50루프 이후 정지선 검출 플래그 활성화
        sensor_data["stop_line_detected"] = (i >= 50)

        distance = calculate_distance(sensor_data, waypoint)

        # 미션 상태 판단
        current_state, target_speed = mission_manager.update_state(sensor_data)
        
        # 간이 물리 엔진: 목표 속도에 맞게 현재 속도 가감속
        if sensor_data["speed"] < target_speed:
            sensor_data["speed"] += 0.5
        elif sensor_data["speed"] > target_speed:
            sensor_data["speed"] -= 1.5 # 브레이크 시 급감속
        sensor_data["speed"] = max(0.0, sensor_data["speed"]) # 속도 음수 방지

        steer, throttle, brake = control(sensor_data, current_state, config)
        
        command = {
            "steer": steer,
            "throttle": throttle,
            "brake": brake
        }
        
        # 로그 저장
        save_log(i, sensor_data, steer, current_state)
        
        # 확인용 출력 (출력 포맷 여백 조정)
        print("=" * 45)
        print(f"Loop : {i} | 남은 거리: {distance:.2f}")
        print(f"[Sensor] speed: {sensor_data['speed']:.2f}")
        print(f"[Mission] 상태: {current_state.value:<18} | 목표 속도: {target_speed}")
        
        time.sleep(0.05)

if __name__ == "__main__":
    main()