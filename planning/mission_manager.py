from enum import Enum

class MissionState(Enum):
    LANE_FOLLOWING = "LANE_FOLLOWING"       
    APPROACHING_STOP = "APPROACHING_STOP"   
    STOPPED = "STOPPED"                     
    OBSTACLE_AVOIDING = "OBSTACLE_AVOIDING" 
    LANE_RETURNING = "LANE_RETURNING"       
    EMERGENCY_STOP = "EMERGENCY_STOP"       

class MissionManager:
    """
    [자율주행 FSM 상태 관리자]
    설정 파일(config.yaml)의 파라미터를 기반으로 차량의 다음 미션과 목표 속도를 결정합니다.
    """
    def __init__(self, config_data):
        self.current_state = MissionState.LANE_FOLLOWING
        
        # yaml에서 미션 관련 파라미터 로드
        mission_cfg = config_data.get('mission', {})
        self.thresholds = mission_cfg.get('thresholds', {'stop_distance': 1.0, 'approach_distance': 5.0})
        self.speeds = mission_cfg.get('speeds', {'lane_following': 20.0, 'approaching_stop': 10.0, 'stopped': 0.0})

    def update_state(self, sensor_data):
        """
        [참고] 필요 입력(sensor_data dict):
          - "distance_to_waypoint" (float): 목표 지점까지 거리
          - "stop_line_detected" (bool): 정지선 발견 여부
          - "speed" (float): 현재 차량 속도
          - current_state (MissionState): PID 제어 기준 상태
          - target_speed (float): 추종해야 할 목표 속도
        """
        dist = sensor_data.get("distance_to_waypoint", 999.0)

        if self.current_state == MissionState.LANE_FOLLOWING:
            if dist <= self.thresholds['stop_distance']:
                self.current_state = MissionState.STOPPED
                target_speed = self.speeds['stopped']
            elif dist <= self.thresholds['approach_distance']:
                self.current_state = MissionState.APPROACHING_STOP
                target_speed = self.speeds['approaching_stop']
            elif sensor_data.get("stop_line_detected", False):
                self.current_state = MissionState.APPROACHING_STOP
                target_speed = self.speeds['approaching_stop']
            else:
                target_speed = self.speeds['lane_following']

        elif self.current_state == MissionState.APPROACHING_STOP:
            if dist <= self.thresholds['stop_distance'] or sensor_data.get("speed", 0.0) <= 0.1:
                self.current_state = MissionState.STOPPED
                target_speed = self.speeds['stopped']
            else:
                target_speed = self.speeds['stopped']

        elif self.current_state == MissionState.STOPPED:
            target_speed = self.speeds['stopped']
            
        elif self.current_state == MissionState.OBSTACLE_AVOIDING:
            target_speed = self.speeds.get('obstacle_avoiding', 10.0)
            
        elif self.current_state == MissionState.LANE_RETURNING:
            target_speed = self.speeds.get('lane_returning', 15.0)
            
        else:
            target_speed = self.speeds['stopped']

        return self.current_state, target_speed