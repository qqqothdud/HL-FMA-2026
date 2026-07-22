from enum import Enum

class MissionState(Enum):
    LANE_FOLLOWING = "LANE_FOLLOWING"
    APPROACHING_STOP = "APPROACHING_STOP"
    STOPPED = "STOPPED"
    OBSTACLE_AVOIDING = "OBSTACLE_AVOIDING"
    LANE_RETURNING = "LANE_RETURNING"
    EMERGENCY_STOP = "EMERGENCY_STOP"

class MissionManager:
    def __init__(self):
        self.current_state = MissionState.LANE_FOLLOWING

    def update_state(self, sensor_data):
        # 1. 센서 데이터에서 Waypoint까지의 거리 값을 가져옴 (없으면 안전을 위해 아주 큰 값인 999.0으로 처리)
        dist = sensor_data.get("distance_to_waypoint", 999.0)

        if self.current_state == MissionState.LANE_FOLLOWING:
            # [7/11 목표 적용] 거리가 5미터 이내면 감속 시작, 1미터 이내면 완전 정지 트리거
            if dist <= 1.0:
                self.current_state = MissionState.STOPPED
                target_speed = 0.0
            elif dist <= 5.0:
                self.current_state = MissionState.APPROACHING_STOP
                target_speed = 5.0
            elif sensor_data.get("stop_line_detected", False):
                self.current_state = MissionState.APPROACHING_STOP
                target_speed = 10.0
            else:
                target_speed = 20.0

        elif self.current_state == MissionState.APPROACHING_STOP:
            # 감속 중 목표 좌표 1미터 이내 도달 시 완전 정지
            if dist <= 1.0 or sensor_data.get("speed", 0.0) <= 0.1:
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