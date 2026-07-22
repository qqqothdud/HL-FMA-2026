import time
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.mission_manager import MissionManager, MissionState
from simulator.simulator_interface import get_sensor_data, send_command

def main():
    print("=== 자율주행 파이프라인 (Architecture Final) 시작 ===")
    
    config = load_config()
    mission_manager = MissionManager(config) 
    previous_state = MissionState.LANE_FOLLOWING

    for i in range(1, 101):
        # 1. 시뮬레이터에서 최신 센서 데이터 수신 (현재는 더미, 추후 VTD 데이터로 자연스럽게 교체됨)
        sensor_data = get_sensor_data() 
        
        # (FSM 상태 전환 테스트를 위한 최소한의 강제 트리거 - 연동 시 삭제)
        sensor_data["stop_line_detected"] = (i >= 50)
        sensor_data["distance_to_waypoint"] = 0.5 if i >= 50 else 5.0
        
        # 2. 미션 상태 판단
        current_state, target_speed = mission_manager.update_state(sensor_data)
        
        if previous_state != current_state:
            print("\n" + "="*55)
            print(f"[🚨 FSM 상태 전환 🚨] {previous_state.value} ---> {current_state.value}")
            print("="*55 + "\n")
            previous_state = current_state 

        # 3. 제어 명령 계산
        command = control(sensor_data, current_state, config)
        
        # 4. 시뮬레이터로 제어 명령 전송
        send_command(command)
        
        # 5. 로깅
        current_steer = command.get("steer", 0.0)
        save_log(i, sensor_data, current_steer, current_state)
        
        print(f"Loop: {i:03d} | 상태: {current_state.value:<18} | 제어출력: {command}")
        time.sleep(0.05)

if __name__ == "__main__":
    main()