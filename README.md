#  Simulator Module

## 목적

Simulator 모듈은 차량과 시뮬레이터(VTD) 사이의 입출력을 담당

현재는 Dummy Sensor Data를 사용하며,
향후 VTD API와 연결될 예정

---

## 입력 데이터

현재 Sensor Data 형식

```python
sensor_data = {
    "x": 12.3,
    "y": 4.8,
    "yaw": 1.57,
    "speed": 8.5,
    "camera": None,
    "obstacles": []
}
```

---

## 출력 데이터

Controller에서 생성된 Command

```python
command = {
    "steer": 0.15,
    "throttle": 0.4,
    "brake": 0.0
}
```

---

## 현재 구현 상태

- Dummy Sensor Data 생성
- Main Loop 연동
- Logger 연동

---

## 향후 구현 예정

- VTD Sensor API 연결
- Camera Image 수신
- Obstacle 정보 수신
- Vehicle State 수신