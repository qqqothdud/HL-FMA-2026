from enum import Enum

class MissionState(Enum):
    LANE_FOLLOWING = "LANE_FOLLOWING"       
    APPROACHING_STOP = "APPROACHING_STOP"   
    STOPPED = "STOPPED"                     
    OBSTACLE_AVOIDING = "OBSTACLE_AVOIDING" 
    LANE_RETURNING = "LANE_RETURNING"       
    EMERGENCY_STOP = "EMERGENCY_STOP"       

class MissionManager:
    def __init__(self, config_data):
        self.current_state = MissionState.LANE_FOLLOWING
        
        mission_cfg = config_data.get('mission', {})
        self.thresholds = mission_cfg.get('thresholds', {'stop_distance': 1.0, 'approach_distance': 5.0})
        self.speeds = mission_cfg.get('speeds', {'lane_following': 20.0, 'approaching_stop': 10.0, 'stopped': 0.0})

    def update_state(self, sensor_data):
        dist = sensor_data.get("distance_to_waypoint", 999.0)
        
        # ------------------------------------------------------------------
        # [7/18 이식 포인트 3] main.py에서 이식해 준 정지선 감지 결과 읽기!
        # ------------------------------------------------------------------
        is_stop_line = sensor_data.get("stop_line_detected", False)

        if self.current_state == MissionState.LANE_FOLLOWING:
            # OpenCV 인지 모듈이 정지선을 발견했거나, 목표 지점이 가까워지면 감속 상태로 진입
            if is_stop_line or dist <= self.thresholds['approach_distance']:
                self.current_state = MissionState.APPROACHING_STOP
                target_speed = self.speeds['approaching_stop']
            else:
                target_speed = self.speeds['lane_following']

        elif self.current_state == MissionState.APPROACHING_STOP:
            # 정지선 앞에서 완전히 멈춰야 할 때
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