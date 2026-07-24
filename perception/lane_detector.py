import cv2
import numpy as np

class LaneDetector:
    def __init__(self, img_width=640, img_height=480):
        self.w = img_width
        self.h = img_height
        self.center_x = self.w // 2
        
        # [7/24 예외 처리] 이전 프레임의 차선 중심을 기억할 변수 초기화
        self.prev_lane_center = self.center_x
        self.fail_count = 0  # 연속 실패 횟수 카운트
        
        # HSV 색상 범위
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([40, 255, 255])
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 50, 255])

        # BEV 사다리꼴 좌표 설정
        self.src_pts = np.float32([
            [int(self.w * 0.35), int(self.h * 0.65)],
            [int(self.w * 0.65), int(self.h * 0.65)],
            [int(self.w * 0.95), self.h],
            [int(self.w * 0.05), self.h]
        ])
        self.dst_pts = np.float32([
            [int(self.w * 0.2), 0],
            [int(self.w * 0.8), 0],
            [int(self.w * 0.8), self.h],
            [int(self.w * 0.2), self.h]
        ])
        self.M_persp = cv2.getPerspectiveTransform(self.src_pts, self.dst_pts)

    def get_bird_eye_view(self, img):
        return cv2.warpPerspective(img, self.M_persp, (self.w, self.h))

    def get_color_mask(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        white_mask = cv2.inRange(hsv, self.lower_white, self.upper_white)
        return cv2.bitwise_or(yellow_mask, white_mask)

# 전역 감지기 인스턴스
_detector_instance = None

def _get_detector(image):
    global _detector_instance
    if _detector_instance is None and image is not None:
        h, w = image.shape[:2]
        _detector_instance = LaneDetector(img_width=w, img_height=h)
    return _detector_instance

def detect_lane(image):
    """
    [7/24 목표] 차선 인식 실패 시 이전 프레임의 차선 중심(prev_lane_center)을 유지하여 반환
    """
    if image is None:
        return 320

    detector = _get_detector(image)
    bev_img = detector.get_bird_eye_view(image)
    mask = detector.get_color_mask(bev_img)
    
    nonzero_y, nonzero_x = np.nonzero(mask)
    
    # ------------------------------------------------------------------
    # [7/24 핵심 구현] 유의미한 차선 픽셀이 검출되었는지 검사
    # ------------------------------------------------------------------
    if len(nonzero_x) > 50:
        lane_center = int(np.mean(nonzero_x))
        detector.prev_lane_center = lane_center  # 성공 시 최신 중심값 갱신!
        detector.fail_count = 0
    else:
        detector.fail_count += 1
        # 차선을 놓쳤을 때: 직전 프레임의 정상 위치를 그대로 반환 (Fallback)
        lane_center = detector.prev_lane_center
        
        # 만약 30프레임(약 1.5초) 이상 연속으로 실패하면 차선이 아예 없는 것으로 간주하고 중앙으로 복귀
        if detector.fail_count > 30:
            lane_center = detector.center_x
            
    return lane_center

def detect_stop_line(image):
    if image is None:
        return False
    detector = _get_detector(image)
    roi_top = int(detector.h * 0.7)
    roi_img = image[roi_top:, :]
    hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, detector.lower_white, detector.upper_white)
    contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / max(float(h), 1.0)
            if aspect_ratio > 3.0 and w > (detector.w * 0.4):
                return True
                
    return False