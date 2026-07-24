import cv2
import numpy as np

class LaneDetector:
    """
    3주차 인지 모듈: HSV 필터링, Bird-Eye View 변환, 차선 중심 및 정지선 검출 클래스
    """
    def __init__(self, img_width=640, img_height=480):
        self.w = img_width
        self.h = img_height
        self.center_x = self.w // 2
        
        # 1. HSV 색상 범위 (config.yaml과 일치시킴)
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([40, 255, 255])
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 50, 255])

        # 2. [7/15 목표] Bird-Eye View (Perspective Transform) 좌표 설정
        # VTD 앞카메라 ROI 사다리꼴 좌표 (실제 주행 화면에 맞춰 튜닝 필요)
        self.src_pts = np.float32([
            [int(self.w * 0.2), int(self.h * 0.7)],  # 좌상
            [int(self.w * 0.8), int(self.h * 0.7)],  # 우상
            [int(self.w * 0.95), self.h],            # 우하
            [int(self.w * 0.05), self.h]             # 좌하
        ])
        self.dst_pts = np.float32([
            [int(self.w * 0.2), 0],
            [int(self.w * 0.8), 0],
            [int(self.w * 0.8), self.h],
            [int(self.w * 0.2), self.h]
        ])
        self.M_persp = cv2.getPerspectiveTransform(self.src_pts, self.dst_pts)

    def get_bird_eye_view(self, img):
        """카메라 이미지를 하늘에서 본 탑뷰로 변환"""
        return cv2.warpPerspective(img, self.M_persp, (self.w, self.h))

    def get_color_mask(self, img):
        """HSV 기반 흰색 + 노란색 차선 이진화 마스크 추출"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        white_mask = cv2.inRange(hsv, self.lower_white, self.upper_white)
        return cv2.bitwise_or(yellow_mask, white_mask)

# --- 팀원의 perception/perception.py에서 호출할 마스터 함수들 ---

# 전역 감지기 인스턴스 (매번 생성하지 않고 재사용)
_detector_instance = None

def _get_detector(image):
    global _detector_instance
    if _detector_instance is None and image is not None:
        h, w = image.shape[:2]
        _detector_instance = LaneDetector(img_width=w, img_height=h)
    return _detector_instance

def detect_lane(image):
    """
    [7/13~15 목표] 차선 중심 x좌표 반환 (팀원 호환용 API)
    """
    if image is None:
        return 320  # 이미지가 없을 경우 화면 중앙 기본값 반환

    detector = _get_detector(image)
    
    # 1. Bird-Eye View로 펴기
    bev_img = detector.get_bird_eye_view(image)
    
    # 2. 색상 마스크 추출
    mask = detector.get_color_mask(bev_img)
    
    # 3. 차선 픽셀들의 x좌표 평균으로 차선 중심(lane_center) 연산
    nonzero_y, nonzero_x = np.nonzero(mask)
    
    if len(nonzero_x) > 50:  # 차선 픽셀이 유의미하게 많을 때만 계산
        lane_center = int(np.mean(nonzero_x))
    else:
        lane_center = detector.center_x  # 차선을 놓치면 중앙 유지
        
    return lane_center

def detect_stop_line(image):
    """
    [7/16 목표] 정지선 검출 플래그 반환 (팀원 호환용 API)
    """
    if image is None:
        return False

    detector = _get_detector(image)
    
    # 1. 화면 하단 30% 영역(ROI)만 잘라내서 정지선 탐색
    roi_top = int(detector.h * 0.7)
    roi_img = image[roi_top:, :]
    
    # 2. 흰색 영역 마스크 추출
    hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, detector.lower_white, detector.upper_white)
    
    # 3. 마스크 내부의 윤곽선(Contours) 검출
    contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # 노이즈를 제외한 큰 덩어리만 확인
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / max(float(h), 1.0)
            
            # 정지선 특성: 가로로 아주 길고(너비 > 높이*3) 면적이 큼
            if aspect_ratio > 3.0 and w > (detector.w * 0.4):
                return True
                
    return False