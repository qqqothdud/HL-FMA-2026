from enum import Enum

# 1. FSM 상태 정의 (Enum 활용) - 요청하신 내용 그대로 반영
class MissionState(Enum):
    LANE_FOLLOWING = "LANE_FOLLOWING"       # 기본 차선 주행
    APPROACHING_STOP = "APPROACHING_STOP"   # 정지선/교차로 접근 중 (감속)
    STOPPED = "STOPPED"                     # 완전 정차
    OBSTACLE_AVOIDING = "OBSTACLE_AVOIDING" # 장애물 회피 중
    LANE_RETURNING = "LANE_RETURNING"       # 회피 후 원래 차선 복귀 중
    EMERGENCY_STOP = "EMERGENCY_STOP"       # 돌발 상황 긴급 제동

class MissionManager:
    def __init__(self):
        # 초기 상태를 기본 차선 주행으로 설정
        self.current_state = MissionState.LANE_FOLLOWING

    def update_state(self, sensor_data):
        # 현재 상태를 기준으로 다음 상태와 목표 속도 반환
        if self.current_state == MissionState.LANE_FOLLOWING:
            if sensor_data.get("stop_line_detected", False):
                # 정지선 인식 시 감속 상태로 전환
                self.current_state = MissionState.APPROACHING_STOP
                target_speed = 10.0
            else:
                target_speed = 20.0

        elif self.current_state == MissionState.APPROACHING_STOP:
            if sensor_data.get("speed", 0.0) <= 0.1:
                # 속도가 0에 수렴하면 완전 정차 상태로 전환
                self.current_state = MissionState.STOPPED
                target_speed = 0.0
            else:
                target_speed = 0.0

        elif self.current_state == MissionState.STOPPED:
            target_speed = 0.0
            
        elif self.current_state == MissionState.OBSTACLE_AVOIDING:
            target_speed = 10.0
            
        elif self.current_state == MissionState.LANE_RETURNING:
            target_speed = 15.0
            
        elif self.current_state == MissionState.EMERGENCY_STOP:
            target_speed = 0.0
            
        else:
            target_speed = 0.0

        return self.current_state, target_speed