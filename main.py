import time
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.geometry import calculate_distance
from planning.mission_manager import MissionManager, MissionState

# [리팩토링] 팀원이 작성한 시뮬레이터 인터페이스 임포트
# (현재 파일 내용은 더미여도, 구조적 결합을 위해 여기서 불러와야 합니다)
from simulator.simulator_interface import get_sensor_data, send_command

def main():
    print("=== 자율주행 파이프라인 (Refactored) 시작 ===")
    
    # 설정 파일 로드 및 매니저 초기화
    config = load_config()
    mission_manager = MissionManager(config) 
    
    waypoint = {"x": 25.0, "y": 10.0}
    previous_state = MissionState.LANE_FOLLOWING

    for i in range(1, 101):
        # 1. [리팩토링] 더미 데이터 계산 로직을 삭제하고 인터페이스 함수로 교체
        # 배소영 님이 작성한 모듈에서 VTD 센서 데이터를 받아오는 형태로 통일
        sensor_data = get_sensor_data() 
        
        # 1-1. 인터페이스에서 아직 구현되지 않은 임시값 덮어쓰기 (테스트 유지용)
        sensor_data["distance_to_waypoint"] = calculate_distance(sensor_data, waypoint)
        sensor_data["stop_line_detected"] = (i >= 50)

        # 2. 미션 상태 판단
        current_state, target_speed = mission_manager.update_state(sensor_data)
        
        # 상태 전환 감지
        if previous_state != current_state:
            print("\n" + "="*55)
            print(f"[🚨 FSM 상태 전환 🚨] {previous_state.value} ---> {current_state.value}")
            print("="*55 + "\n")
            previous_state = current_state 

        # 3. 제어 명령 계산 (팀원이 추가한 여분의 반환값이 있다면 *extra_args가 흡수함)
        steer, throttle, brake, *extra_args = control(sensor_data, current_state, config)
        
        # 4. [리팩토링] 계산된 명령을 시뮬레이터로 전송하는 인터페이스 연결
        command = {"steer": steer, "throttle": throttle, "brake": brake}
        send_command(command)
        
        # 5. 로깅
        save_log(i, sensor_data, steer, current_state)
        
        print(f"Loop: {i:03d} | 상태: {current_state.value:<18} | 속도: {sensor_data.get('speed', 0.0):05.2f}")
        time.sleep(0.05)

if __name__ == "__main__":
    main()