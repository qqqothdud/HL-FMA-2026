import cv2
import numpy as np
import os
import glob

class LaneDetector:
    def __init__(self):
        # 노란색 차선 (Yellow) HSV 범위 (실제 VTD 시뮬레이터의 카메라에서 받는 데이터로 HSV값 수정 필요)
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([40, 255, 255])
        
        # 흰색 차선 (White) HSV 범위 (실제 VTD 시뮬레이터의 카메라에서 받는 데이터로 HSV값 수정 필요)
        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 50, 255])

    def process_image(self, image_path):
        """단일 이미지를 불러와 차선 마스킹 작업을 수행합니다."""
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"[오류] 이미지를 읽을 수 없습니다: {image_path}")
            return None, None, None

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 색상 마스크 추출
        yellow_mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        white_mask = cv2.inRange(hsv, self.lower_white, self.upper_white)

        # 두 마스크를 합쳐 전체 차선 영역 추출
        combined_mask = cv2.bitwise_or(yellow_mask, white_mask)
        
        # 원본 이미지에 마스크 적용
        result = cv2.bitwise_and(img, img, mask=combined_mask)

        return img, combined_mask, result

# 7월 9일 실습용: 폴더 내 모든 PNG 파일 일괄 처리 및 저장
if __name__ == "__main__":
    # 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, "data", "image")
    output_dir = os.path.join(base_dir, "data", "image_result") # 결과물을 저장할 폴더
    
    # 출력 폴더가 없다면 자동 생성
    os.makedirs(output_dir, exist_ok=True)

    # input_dir 내의 모든 .png 파일 경로 가져오기
    png_files = glob.glob(os.path.join(input_dir, "*.png"))

    if not png_files:
        print(f"[알림] {input_dir} 폴더에 PNG 파일이 존재하지 않습니다.")
    else:
        print(f"총 {len(png_files)}개의 PNG 파일을 발견했습니다. 처리를 시작합니다...\n")
        detector = LaneDetector()
        
        for img_path in png_files:
            filename = os.path.basename(img_path)
            print(f"[{filename}] 처리 중...")
            
            original_img, mask_img, result_img = detector.process_image(img_path)
            
            if original_img is not None:
                # 저장할 파일 이름 설정 (원본이름_mask.png, 원본이름_result.png)
                name, ext = os.path.splitext(filename)
                mask_save_path = os.path.join(output_dir, f"{name}_mask{ext}")
                result_save_path = os.path.join(output_dir, f"{name}_result{ext}")
                
                # cv2.imwrite()를 사용해 결과물 파일로 저장
                cv2.imwrite(mask_save_path, mask_img)
                cv2.imwrite(result_save_path, result_img)
                
                print(f"  -> 저장 완료: {result_save_path}")
                
                # 시각화 창 띄우기
                cv2.imshow("1. Original Image", original_img)
                cv2.imshow("2. Combined Mask", mask_img)
                cv2.imshow("3. Final Result", result_img)
                
                print("  => 다음 이미지를 보려면 아무 키나 누르세요 (종료하려면 ESC 키).")
                key = cv2.waitKey(0)
                if key == 27: # 27은 ESC 키의 아스키코드
                    print("\n[알림] 사용자가 처리를 중단했습니다.")
                    break
                
        cv2.destroyAllWindows()
        print("\n모든 이미지 처리 및 저장이 완료되었습니다!")
