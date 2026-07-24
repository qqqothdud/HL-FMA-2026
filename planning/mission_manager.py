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
        
        # ------------------------------------------------------------------
        # [7/25 목표] 미션 전환 Hold Time (Debouncing & 최소 유지 시간) 제어 변수
        # ------------------------------------------------------------------
        self.hold_counter = 0
        self.STOP_HOLD_FRAMES = 60       # STOPPED 상태에 진입하면 최소 60루프(약 3초)간 정지 유지
        self.STOPLINE_DEBOUNCE = 3       # 정지선이 3루프 연속으로 감지되어야 진짜 정지선으로 인정
        self.stopline_count = 0

    def update_state(self, sensor_data):
        """
        [7/26 리팩토링] 메인 판단 루틴: 각 상태별 전용 핸들러 함수로 분기 처리
        """
        # 정지선 노이즈 필터링 (Debounce 처리)
        if sensor_data.get("stop_line_detected", False):
            self.stopline_count += 1
        else:
            self.stopline_count = max(0, self.stopline_count - 1)
            
        is_stop_line_confirmed = (self.stopline_count >= self.STOPLINE_DEBOUNCE)
        dist = sensor_data.get("distance_to_waypoint", 999.0)

        # 상태별 전용 처리 함수 호출 (Refactoring)
        if self.current_state == MissionState.LANE_FOLLOWING:
            return self._handle_lane_following(dist, is_stop_line_confirmed)
            
        elif self.current_state == MissionState.APPROACHING_STOP:
            return self._handle_approaching_stop(dist, sensor_data)
            
        elif self.current_state == MissionState.STOPPED:
            return self._handle_stopped()
            
        elif self.current_state == MissionState.OBSTACLE_AVOIDING:
            return self._handle_obstacle_avoiding()
            
        elif self.current_state == MissionState.LANE_RETURNING:
            return self._handle_lane_returning()
            
        else:
            return self.current_state, self.speeds['stopped']

    # ------------------------------------------------------------------
    # [7/26 리팩토링] 상태별 세부 핸들러 메서드 분리
    # ------------------------------------------------------------------
    def _handle_lane_following(self, dist, is_stop_line):
        if is_stop_line or dist <= self.thresholds['approach_distance']:
            self._transition_to(MissionState.APPROACHING_STOP)
            return self.current_state, self.speeds['approaching_stop']
            
        return self.current_state, self.speeds['lane_following']

    def _handle_approaching_stop(self, dist, sensor_data):
        current_speed = sensor_data.get("speed", 0.0)
        
        # 목표 지점 도달 또는 속도가 거의 0이 되면 완전 정지 상태로 전환
        if dist <= self.thresholds['stop_distance'] or current_speed <= 0.1:
            self._transition_to(MissionState.STOPPED)
            self.hold_counter = self.STOP_HOLD_FRAMES  # [7/25] 정지 유지 카운터 시작!
            return self.current_state, self.speeds['stopped']
            
        return self.current_state, self.speeds['approaching_stop']

    def _handle_stopped(self):
        # [7/25 목표] Hold Time 작동: 카운터가 0이 될 때까지 무조건 STOPPED 상태 유지
        if self.hold_counter > 0:
            self.hold_counter -= 1
            return self.current_state, self.speeds['stopped']
            
        # Hold Time 종료 후 다음 액션(예: 다시 출발 또는 차선 복귀)으로 전환
        self._transition_to(MissionState.LANE_FOLLOWING)
        return self.current_state, self.speeds['lane_following']

    def _handle_obstacle_avoiding(self):
        return self.current_state, self.speeds.get('obstacle_avoiding', 10.0)

    def _handle_lane_returning(self):
        return self.current_state, self.speeds.get('lane_returning', 15.0)

    def _transition_to(self, new_state):
        """상태 전환 시 공통으로 실행할 로직"""
        if self.current_state != new_state:
            self.current_state = new_state