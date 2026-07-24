import cv2
import numpy as np
import os
import glob

class LaneDetector:
    def __init__(self, img_width=640, img_height=480):
        self.w = img_width
        self.h = img_height
        
        # 1. 노란색/흰색 차선 HSV 범위
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([40, 255, 255])
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 50, 255])

        # 2. [BEV 추가] Bird-Eye View (Perspective Transform) 사다리꼴 좌표 설정
        # ※ 실제 VTD 카메라 화면의 도로 소실점에 맞춰 숫자를 약간씩 튜닝해야 합니다.
        self.src_pts = np.float32([
            [int(self.w * 0.35), int(self.h * 0.65)],  # 좌상
            [int(self.w * 0.65), int(h * 0.65)],  # 우상
            [int(self.w * 0.95), self.h],            # 우하
            [int(self.w * 0.05), self.h]             # 좌하
        ])
        self.dst_pts = np.float32([
            [int(self.w * 0.2), 0],                  # 변환 후 좌상
            [int(self.w * 0.8), 0],                  # 변환 후 우상
            [int(self.w * 0.8), self.h],             # 변환 후 우하
            [int(self.w * 0.2), self.h]              # 변환 후 좌하
        ])
        self.M_persp = cv2.getPerspectiveTransform(self.src_pts, self.dst_pts)

    def process_image(self, image_path):
        """이미지를 불러와 ROI 시각화 및 Bird-Eye View 변환을 수행합니다."""
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"[오류] 이미지를 읽을 수 없습니다: {image_path}")
            return None, None, None

        # 이미지 해상도에 맞춰 BEV 좌표계 동적 갱신
        h, w = img.shape[:2]
        if w != self.w or h != self.h:
            self.w, self.h = w, h
            self.__init__(img_width=w, img_height=h)

        # 1. 원본 이미지에 사다리꼴 ROI 영역 그리기 (붉은색 선)
        img_with_roi = img.copy()
        cv2.polylines(img_with_roi, [np.int32(self.src_pts)], isClosed=True, color=(0, 0, 255), thickness=2)

        # 2. Bird-Eye View로 하늘에서 내려다본 탑뷰 변환
        bev_img = cv2.warpPerspective(img, self.M_persp, (self.w, self.h))

        # 3. BEV 화면에서 HSV 차선 마스크 추출
        hsv = cv2.cvtColor(bev_img, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        white_mask = cv2.inRange(hsv, self.lower_white, self.upper_white)
        combined_mask = cv2.bitwise_or(yellow_mask, white_mask)
        
        # BEV 차선 컬러 결과물
        bev_result = cv2.bitwise_and(bev_img, bev_img, mask=combined_mask)

        return img_with_roi, bev_img, bev_result

# 7월 15일 실습용: 경로 에러 없는 BEV 자동 검증
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # [경로 탐색 개선] 가능한 모든 폴더 위치를 후보군으로 등록
    candidate_dirs = [
        os.path.join(current_dir, "data", "image"),
        os.path.join(os.path.dirname(current_dir), "data", "image"),
        os.path.join(current_dir, "data"),
        os.path.join(os.path.dirname(current_dir), "data"),
        current_dir,
        os.path.dirname(current_dir)
    ]

    image_files = []
    found_dir = ""

    # 여러 확장자(.png, .PNG, .jpg 등) 및 후보 폴더에서 파일 탐색
    for d in candidate_dirs:
        if os.path.exists(d):
            for ext in ("*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg"):
                files = glob.glob(os.path.join(d, ext))
                if files:
                    image_files.extend(files)
                    found_dir = d
            if image_files:
                break

    if not image_files:
        print("[오류] 다음 경로들에서 이미지 파일을 찾지 못했습니다:")
        for d in candidate_dirs:
            print(f"  - {os.path.abspath(d)}")
        print("\n[팁] 실행하는 파이썬 스크립트와 같은 폴더나 data/image/ 폴더에 이미지를 넣어주세요.")
    else:
        # 중복 제거 및 정렬
        image_files = sorted(list(set(image_files)))
        output_dir = os.path.join(found_dir, "bev_result")
        os.makedirs(output_dir, exist_ok=True)

        print(f"[성공] '{found_dir}'에서 총 {len(image_files)}개의 이미지를 발견했습니다!")
        print(f"결과 저장 폴더: {output_dir}\n")
        
        detector = LaneDetector()
        
        for img_path in image_files:
            filename = os.path.basename(img_path)
            print(f"[{filename}] BEV 변환 중...")
            
            roi_img, bev_img, bev_result = detector.process_image(img_path)
            
            if roi_img is not None:
                name, ext = os.path.splitext(filename)
                cv2.imwrite(os.path.join(output_dir, f"{name}_bev_top{ext}"), bev_img)
                cv2.imwrite(os.path.join(output_dir, f"{name}_bev_lane{ext}"), bev_result)
                
                # 원본(ROI 표시)과 BEV 탑뷰를 가로로 나란히 붙여서 비교 시각화
                combined_view = np.hstack((roi_img, bev_img))
                cv2.imshow("Bird-Eye View Verification: [Left] Original ROI | [Right] BEV Top-down", combined_view)
                cv2.imshow("BEV Lane Mask Result", bev_result)
                
                print("  => 다음 이미지: 아무 키 | 종료: ESC 키")
                key = cv2.waitKey(0)
                if key == 27:
                    print("\n[알림] 검증을 중단합니다.")
                    break
                
        cv2.destroyAllWindows()
        print("\n모든 BEV 변환 및 저장이 완료되었습니다!")