# HL-FMA-2026

## 프로젝트 소개

자율주행 소프트웨어 구조를 학습하기 위한 프로젝트

현재 구현된 기능은 더미(Dummy) 데이터 기반의 Main Loop이며,
Sensor → Mission → Controller → Command → Logger의 흐름을 구현함.

---

## 프로젝트 구조

```
HL-FMA-2026
│
├── config/
├── controller/
├── data/
├── docs/
├── logger/
├── mission/
├── perception/
├── planning/
├── simulator/
└── test/
```

---

## 실행 환경

- Python 3.10 이상
- VS Code
- WSL Ubuntu

---

## 실행 방법
| Member | Role |
|-------|-------|
| 배소영 | Simulator / Integration |
| 주연아 | Control |
| 이건 | Perception / Mission |

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

Mission

↓

Controller

↓

Command

↓

Logger
```

반복 실행 예시

```
Loop 1

Sensor
Mission
Command
Logger

Loop 2

...
```

---

## 현재 구현 기능

- Dummy Sensor Data
- Mission Module
- Controller Module
- Command 생성
- CSV Logger
- Main Loop

---

## 향후 구현 예정

- Perception
- PID Controller
- Pure Pursuit
- VTD Simulator Interface
