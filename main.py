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
    
    # 초기 시작 위치
    sensor_data = {
        "x": 0.0,
        "y": 0.0,
        "yaw": 1.57,
        "speed": 8.5,
        "camera": None,
        "obstacles": []
    }
    
    # 테스트를 위해 50루프째에 도달할 수 있는 정확한 좌표로 Waypoint 설정
    waypoint = {
        "x": 25.0,
        "y": 10.0
    }

    previous_state = MissionState.LANE_FOLLOWING

    for i in range(1, 101):
        # 차량이 Waypoint를 향해 이동 (매 루프마다 x는 +0.5, y는 +0.2)
        sensor_data["x"] += 0.5
        sensor_data["y"] += 0.2
        
        # 1. 거리 계산
        distance = calculate_distance(sensor_data, waypoint)
        
        # 2. [핵심] FSM이 거리를 알 수 있도록 sensor_data에 값을 주입
        sensor_data["distance_to_waypoint"] = distance

        # 3. 미션 상태 판단 (이제 i >= 50 플래그가 아닌 실제 거리를 기반으로 판단됨)
        new_state, target_speed = mission_manager.update_state(sensor_data)
        
        # 상태 전환 감지 및 터미널 알림
        if previous_state != new_state:
            print("\n" + "="*55)
            print(f"[🚨 FSM 상태 전환 감지 🚨] {previous_state.value} ---> {new_state.value}")
            print("="*55 + "\n")
            previous_state = new_state 
        
        # 간이 물리 엔진
        if sensor_data["speed"] < target_speed:
            sensor_data["speed"] += 0.5
        elif sensor_data["speed"] > target_speed:
            sensor_data["speed"] -= 1.5 
        sensor_data["speed"] = max(0.0, sensor_data["speed"]) 

        steer, throttle, brake = control(sensor_data, new_state, config)
        
        # CSV 로깅
        save_log(i, sensor_data, steer, new_state)
        
        # 실시간 모니터링 출력
        print(f"Loop: {i:03d} | 위치: ({sensor_data['x']:04.1f}, {sensor_data['y']:04.1f}) | 거리: {distance:05.2f}m | 상태: {new_state.value:<16} | 속도: {sensor_data['speed']:05.2f}")
        
        time.sleep(0.05)

if __name__ == "__main__":
    main()