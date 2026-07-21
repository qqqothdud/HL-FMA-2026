from enum import Enum

# 1. FSM 상태 정의 (Enum 활용)
class MissionState(Enum):
    LANE_FOLLOWING = "LANE_FOLLOWING"       # 기본 차선 주행
    APPROACHING_STOP = "APPROACHING_STOP"   # 정지선/교차로 접근 중 (감속)
    STOPPED = "STOPPED"                     # 완전 정차
    OBSTACLE_AVOIDING = "OBSTACLE_AVOIDING" # 장애물 회피 중
    LANE_RETURNING = "LANE_RETURNING"       # 회피 후 원래 차선 복귀 중
    EMERGENCY_STOP = "EMERGENCY_STOP"       # 돌발 상황 긴급 제동

# 2. 미션 관리자 클래스
class MissionManager:
    def __init__(self):
        # 시스템 시작 시 초기 상태는 차선 주행으로 설정
        self.current_state = MissionState.LANE_FOLLOWING
        
        # 상태별 목표 속도 매핑 (예시 단위: km/h) -> 이후 제어 파트로 전달됨
        self.target_speed_map = {
            MissionState.LANE_FOLLOWING: 30.0,
            MissionState.APPROACHING_STOP: 10.0,
            MissionState.STOPPED: 0.0,
            MissionState.OBSTACLE_AVOIDING: 15.0,
            MissionState.LANE_RETURNING: 15.0,
            MissionState.EMERGENCY_STOP: 0.0
        }

    # 3. 상태 전환 로직 (매 프레임마다 main.py에서 호출됨)
    def update_state(self, perception_data):
        """
        인지(Perception) 파트에서 넘겨준 데이터를 바탕으로 현재 상태를 업데이트합니다.
        perception_data 예시: {'stop_line_detected': True, 'obstacle_detected': False, ...}
        """
        
        # 더미 데이터 추출 (실제 perception_data 구조에 맞게 수정 필요)
        stop_line = perception_data.get('stop_line_detected', False)
        obstacle = perception_data.get('obstacle_detected', False)
        emergency = perception_data.get('emergency', False)

        # [예외] 최우선 순위: 긴급 상황 발생 시 바로 긴급 정지
        if emergency:
            self.current_state = MissionState.EMERGENCY_STOP
            return self.current_state, self.target_speed_map[self.current_state]

        # [상태 전환 흐름도 반영]
        if self.current_state == MissionState.LANE_FOLLOWING:
            if stop_line:
                self.current_state = MissionState.APPROACHING_STOP
            elif obstacle:
                self.current_state = MissionState.OBSTACLE_AVOIDING
                
        elif self.current_state == MissionState.APPROACHING_STOP:
            # 예시: 정지선 감지 후 특정 조건(거리 도달 등) 만족 시 완전 정차
            # 현재는 더미 로직으로 바로 STOPPED로 넘어간다고 가정
            self.current_state = MissionState.STOPPED
            
        elif self.current_state == MissionState.STOPPED:
            # 신호등 녹색 전환 등의 조건이 만족되면 다시 주행 상태로 복귀 (현재는 대기)
            pass 
            
        elif self.current_state == MissionState.OBSTACLE_AVOIDING:
            # 회피 경로를 다 통과했다고 가정 (더미 조건)
            # self.current_state = MissionState.LANE_RETURNING
            pass

        elif self.current_state == MissionState.LANE_RETURNING:
            # 복귀 완료 후 차선 주행으로 변경
            # self.current_state = MissionState.LANE_FOLLOWING
            pass

        return self.current_state, self.target_speed_map[self.current_state]

    def get_current_state(self):
        return self.current_state

# 파일 단독 실행 테스트용 코드
if __name__ == "__main__":
    manager = MissionManager()
    print(f"초기 상태: {manager.get_current_state().value}")
    
    # 1. 정지선 인지 더미 데이터 전달
    dummy_data = {'stop_line_detected': True, 'obstacle_detected': False}
    new_state, target_speed = manager.update_state(dummy_data)
    
    print(f"업데이트 후 상태: {new_state.value}, 목표 속도: {target_speed}")