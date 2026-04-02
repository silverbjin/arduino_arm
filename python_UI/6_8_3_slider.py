import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QSlider, QHBoxLayout)
from PyQt5.QtCore import Qt

class RobotController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('4축 로봇암 제어기 - 6-8-3')
        self.setGeometry(100, 100, 400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.sliders = [] # 슬라이더 객체 저장
        self.labels = []  # 라벨 객체 저장
        names = ["Base", "Shoulder", "UpperArm", "ForeArm"]

        for i, name in enumerate(names):
            # 수평 레이아웃: [라벨] - [슬라이더] 형태로 배치하기 위함
            h_layout = QVBoxLayout() 
            
            # 라벨 생성
            lbl = QLabel(f"{name}: 90")
            self.labels.append(lbl)
            h_layout.addWidget(lbl)

            # 슬라이더 생성
            slider = QSlider(Qt.Horizontal) # 가로 방향 슬라이더
            slider.setRange(0, 180)         # 서보모터 범위 0~180도
            slider.setValue(90)             # 초기값 90도 (중간)
            
            # 슬라이더 값 변경 시 update_label 함수 호출 (lambda를 사용하여 인덱스 전달)
            # 주의: 루프 안에서 lambda 사용 시 i값 고정을 위해 i=i 구문 필요
            slider.valueChanged.connect(lambda val, idx=i: self.update_label(idx, val))
            
            self.sliders.append(slider)
            h_layout.addWidget(slider)
            
            main_layout.addLayout(h_layout)

        # 제어 버튼들
        self.btn_move = QPushButton('Robot Run')
        main_layout.addWidget(self.btn_move)

        self.btn_home = QPushButton('Home')
        main_layout.addWidget(self.btn_home)

    def update_label(self, index, value):
        # 슬라이더가 움직일 때 해당 라벨의 텍스트 업데이트
        names = ["Base", "Shoulder", "UpperArm", "ForeArm"]
        self.labels[index].setText(f"{names[index]}: {value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotController()
    window.show()
    sys.exit(app.exec_())