import sys
import serial
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QSlider)
from PyQt5.QtCore import Qt

class RobotController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSerial()

    def initSerial(self):
        # 시리얼 포트 설정 (사용자의 환경에 맞게 COM 포트 변경 필요)
        # 윈도우: 'COM3', 'COM4' 등 / 맥,리눅스: '/dev/ttyUSB0' 등
        try:
            self.ser = serial.Serial('COM6', 115200, timeout=1)
            print("시리얼 포트 연결 성공")
            time.sleep(2) # 아두이노 리셋 대기
        except:
            print("시리얼 포트 연결 실패. 포트 번호를 확인하세요.")
            self.ser = None

    def initUI(self):
        # ... (6-8-3의 UI 설정 코드와 동일, 생략) ...
        self.setWindowTitle('4축 로봇암 제어기 - 6-8-4')
        self.setGeometry(100, 100, 400, 500)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.sliders = []
        self.labels = []
        # 아두이노 프로토콜 순서에 맞춰 수정:
        # a=Base(회전), b=Shoulder(어깨), c=UpperArm(팔꿈치), d=ForeArm(손목/그리퍼)
        names = ["Base (회전)", "Shoulder (어깨)", "UpperArm (팔꿈치)", "ForeArm (손목)"]

        for i, name in enumerate(names):
            lbl = QLabel(f"{name}: 90")
            self.labels.append(lbl)
            main_layout.addWidget(lbl)
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 180)
            slider.setValue(90)
            slider.valueChanged.connect(lambda val, idx=i: self.update_label(idx, val))
            self.sliders.append(slider)
            main_layout.addWidget(slider)

        self.btn_move = QPushButton('Robot Run')
        self.btn_move.clicked.connect(self.move_robot) # 함수 연결
        main_layout.addWidget(self.btn_move)

        self.btn_home = QPushButton('Home')
        self.btn_home.clicked.connect(self.go_home) # 함수 연결
        main_layout.addWidget(self.btn_home)

    def update_label(self, index, value):
        names = ["Base (회전)", "Shoulder (어깨)", "UpperArm (팔꿈치)", "ForeArm (손목)"]
        self.labels[index].setText(f"{names[index]}: {value}")

    def move_robot(self):
        if self.ser is None: return
        
        # 슬라이더의 현재 값들을 읽어옵니다.
        angles = [s.value() for s in self.sliders]
        
        # 프로토콜 포맷 생성: 2 + a + 각도1 + b + 각도2 ...
        command = f"2a{angles[0]}b{angles[1]}c{angles[2]}d{angles[3]}e\n"
        print(f"Sending: {command.strip()}")
        
        # 아두이노로 전송 (바이트 단위로 인코딩 필요)
        self.ser.write(command.encode())

    def go_home(self):
        if self.ser is None: return
        
        # 슬라이더 UI도 90도로 복귀
        for slider in self.sliders:
            slider.setValue(90)
            
        # 원점 복귀 명령 '3' 전송
        command = "3\n"
        self.ser.write(command.encode())
        print("Homing...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotController()
    window.show()
    sys.exit(app.exec_())