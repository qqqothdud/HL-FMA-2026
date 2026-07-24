import time
from controller.controller import control
from logger.logger import save_log
from config.config_loader import load_config
from planning.mission_manager import MissionManager, MissionState
from simulator.simulator_interface import get_sensor_data, send_command

# [7/18 이식 포인트 1] 우리가 만든 인지 모듈(또는 팀원의 마스터 모듈) 임포트
from perception.lane_detector import detect_lane, detect_stop_line

def main():
    print("=== 자율주행 파이프라인 (7/18 인지-미션-제어 최종 통합) 시작 ===")
    
    config = load_config()
    mission_manager = MissionManager(config) 
    previous_state = MissionState.LANE_FOLLOWING

    for i in range(1, 101):
        # 1. 시뮬레이터에서 최신 센서 데이터(카메라 영상 포함) 수신
        sensor_data = get_sensor_data() 
        
        # ------------------------------------------------------------------
        # [7/18 이식 포인트 2] 카메라 이미지를 빼와서 OpenCV 인지 알고리즘 실행!
        # ------------------------------------------------------------------
        camera_img = sensor_data.get("camera", {}).get("front", None)
        
        # 인지 모듈 실행 후 결과값을 sensor_data 바구니에 '이식(추가)'
        sensor_data["lane_center"] = detect_lane(camera_img)
        sensor_data["stop_line_detected"] = detect_stop_line(camera_img)
        
        # (테스트용: 아직 시뮬레이터 영상이 없어서 None이면 가상 정지선 신호 주입)
        if camera_img is None and i >= 50:
            sensor_data["stop_line_detected"] = True
        # ------------------------------------------------------------------

        # 2. 미션 상태 판단 (이식된 stop_line_detected 값을 읽어 상태를 결정함)
        current_state, target_speed = mission_manager.update_state(sensor_data)
        
        if previous_state != current_state:
            print("\n" + "="*55)
            print(f"[🚨 FSM 상태 전환 🚨] {previous_state.value} ---> {current_state.value}")
            print("="*55 + "\n")
            previous_state = current_state 

        # 3. 제어 명령 계산 (이식된 lane_center와 current_state를 보고 조향/가속 결정)
        command = control(sensor_data, current_state, config)
        
        # 4. 시뮬레이터로 제어 명령 전송
        send_command(command)
        
        # 5. 로깅
        current_steer = command.get("steer", 0.0)
        save_log(i, sensor_data, current_steer, current_state)
        
        print(f"Loop: {i:03d} | 상태: {current_state.value:<16} | 차선중심: {sensor_data['lane_center']} | 정지선: {sensor_data['stop_line_detected']}")
        time.sleep(0.05)

if __name__ == "__main__":
    main()