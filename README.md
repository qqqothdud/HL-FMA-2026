# HL-FMA-2026

## 프로젝트 소개

HL-FMA-2026은 Python 기반의 자율주행 학습 프로젝트이다.

실제 VTD(Virtual Test Drive) 시뮬레이터를 사용하기 전에 자율주행 시스템의 기본 구조를 직접 구현하며 학습하는 것을 목표로 한다.

현재는 Dummy Simulator를 이용하여 차량의 센서 데이터 생성, 미션 판단, 제어 명령 생성, 로그 저장까지의 전체 파이프라인을 구현하였다.

향후 OpenCV, Pure Pursuit, PID Controller, FSM, ROS2 및 VTD 환경으로 확장할 예정이다.

---

# 프로젝트 구조

```
HL-FMA-2026
│
├── config/
│   ├── config.yaml
│   └── config_loader.py
│
├── simulator/
│   └── simulator_interface.py
│
├── planning/
│   └── geometry.py
│
├── mission/
│   └── mission.py
│
├── controller/
│   └── controller.py
│
├── logger/
│   └── logger.py
│
├── logs/
│   └── driving_log.csv
│
├── main.py
│
└── README.md
```

---

## 실행 환경

- Python 3.10 이상
- VS Code
- WSL Ubuntu

---

## 실행 방법

프로젝트 루트에서 실행

```bash
python3 main.py
```

---

## 실행 결과

프로그램은 아래 순서로 반복 실행됨.

```
Sensor

↓

Mission Planner

        ↓

Controller

        ↓

Vehicle Command

        ↓

Logger
```

---

# 구현 완료 기능

## 1. Config

- YAML 설정 파일 작성
- Config Loader 구현
- 프로젝트 설정값 관리

---

## 2. Dummy Simulator

구현 함수

- get_sensor_data()
- send_command()

현재 생성하는 센서 데이터

```python
sensor_data = {
    "x": current_x,
    "y": current_y,
    "yaw": current_yaw,
    "speed": current_speed,

    "camera": {
        "front": "camera/road.jpg",
        "width": 1280,
        "height": 720,
        "fps": 30
    }
}
```

---

## 3. Geometry

구현 함수

```
calculate_distance()
```

현재 위치와 Waypoint 사이의 거리를 계산한다.

---

## 4. Mission Planner

구현 함수

```
mission_planning()
```

현재 차량 상태를 기반으로 수행할 미션을 결정한다.

현재는 Dummy Mission으로 `LANE` 상태를 반환한다.

---

## 5. Controller

구현 함수

```
control()
```

현재 Mission에 따라 차량 제어 명령을 생성한다.

반환 데이터

```python
command = {
    "steer": steer,
    "accel": accel,
    "brake": brake,
    "target_speed": target_speed
}
```

---

## 6. Logger

CSV 로그 저장 기능 구현

현재 저장되는 열(Column)

| Column | 설명 |
|---------|------|
| time | Loop 번호 |
| x | 차량 X 좌표 |
| y | 차량 Y 좌표 |
| yaw | 차량 방향 |
| speed | 차량 속도 |
| steer | 조향 명령 |
| accel | 가속 명령 |
| brake | 브레이크 명령 |
| target_speed | 목표 속도 |
| mission | 현재 미션 |

CSV Header

```text
time,x,y,yaw,speed,steer,accel,brake,target_speed,mission
```

---

# Main Loop

현재 Main Loop는 100회 반복하도록 구현하였다.

실행 순서

```
for 100 Loop

↓

get_sensor_data()

↓

calculate_distance()

↓

mission_planning()

↓

control()

↓

send_command()

↓

save_log()
```

---

# 현재 출력 정보

매 Loop마다 다음 정보를 출력한다.

```
Loop 1/100

[Sensor]
x
y
yaw
speed

[Waypoint]
x
y
distance

[Mission]

[Command]
steer
accel
brake
target_speed
```

---

# 현재 구현된 Waypoint

```python
waypoint = {
    "x": 20,
    "y": 10
}
```

Dummy Vehicle은 해당 Waypoint를 향해 주행하는 형태로 시뮬레이션된다.

---

# 현재 학습 완료 내용

- Python 프로젝트 구조
- Git / GitHub 협업
- YAML Config 관리
- Dummy Simulator 구현
- Sensor Data 생성
- Geometry(거리 계산)
- Mission Planner
- Controller
- Vehicle Command 생성
- Logger 구현
- CSV 로그 저장
- Main Loop 100회 반복
- Dummy Waypoint 주행 시뮬레이션

---

# 향후 구현 예정

## Perception

- OpenCV
- HSV
- Mask
- Contour
- Perspective Transform
- Lane Detection

---

## Planning

- Multiple Waypoints
- Waypoint Index 관리
- Waypoint 도착 판정
- Path Planning

---

## Control

- Pure Pursuit
- VTD Simulator Interface