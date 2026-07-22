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

    # [추가 1] 이전 상태를 기억할 변수 초기화 (루프 밖에서 선언)
    previous_state = MissionState.LANE_FOLLOWING

    for i in range(1, 101):
        # 더미 데이터 업데이트
        sensor_data["x"] += 0.5
        sensor_data["y"] += 0.2
        sensor_data["stop_line_detected"] = (i >= 50)

        distance = calculate_distance(sensor_data, waypoint)

        # 미션 상태 판단 (변수명을 current_state 대신 new_state로 변경하여 명확히 비교)
        new_state, target_speed = mission_manager.update_state(sensor_data)
        
        # ---------------------------------------------------------
        # [핵심 로직] 상태 전환 감지 및 터미널 알림 출력
        # ---------------------------------------------------------
        if previous_state != new_state:
            print("\n" + "="*55)
            print(f"[🚨 FSM 상태 전환 감지 🚨] {previous_state.value} ---> {new_state.value}")
            print("="*55 + "\n")
            # 알림을 띄운 후, 다음 루프 비교를 위해 이전 상태를 현재 상태로 덮어씌움
            previous_state = new_state 
        
        # 간이 물리 엔진
        if sensor_data["speed"] < target_speed:
            sensor_data["speed"] += 0.5
        elif sensor_data["speed"] > target_speed:
            sensor_data["speed"] -= 1.5 
        sensor_data["speed"] = max(0.0, sensor_data["speed"]) 

        steer, throttle, brake = control(sensor_data, new_state, config)
        
        command = {
            "steer": steer,
            "throttle": throttle,
            "brake": brake
        }
        
        # CSV 파일 저장은 기존과 동일하게 매 틱마다 지속적으로 기록됨
        save_log(i, sensor_data, steer, new_state)
        
        # 실시간 모니터링을 위해 기본 출력문은 1줄로 간소화
        print(f"Loop: {i:03d} | 상태: {new_state.value:<18} | 속도: {sensor_data['speed']:05.2f} | 남은 거리: {distance:.2f}")
        
        time.sleep(0.05)

if __name__ == "__main__":
    main()