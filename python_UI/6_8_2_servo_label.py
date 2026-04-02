import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout

class RobotController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('4축 로봇암 제어기 - 6-8-2')
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout() # 메인 레이아웃
        central_widget.setLayout(self.layout)

        # --- 라벨 추가 영역 ---
        # 4개의 라벨을 저장할 리스트
        self.labels = [] 
        label_names = ["Base (축 1)", "Shoulder (축 2)", "UpperArm (축 3)", "ForeArm (축 4)"]

        for name in label_names:
            # 각 축의 이름과 현재 각도를 표시할 라벨 생성
            # 초기값은 90도로 설정
            lbl = QLabel(f"{name}: 90")
            self.layout.addWidget(lbl)
            self.labels.append(lbl) # 나중에 값을 바꾸기 위해 리스트에 저장
        
        # 기존 버튼 추가 (레이아웃 하단에 추가됨)
        self.btn_move = QPushButton('Robot Run')
        self.layout.addWidget(self.btn_move)

        self.btn_home = QPushButton('Home')
        self.layout.addWidget(self.btn_home)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotController()
    window.show()
    sys.exit(app.exec_())