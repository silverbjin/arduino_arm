import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class RobotController(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 윈도우 기본 설정
        self.setWindowTitle('4축 로봇암 제어기')
        self.setGeometry(100, 100, 400, 300) # x, y, width, height

        # 메인 위젯 설정 (PyQt는 메인 윈도우 안에 위젯을 배치해야 함)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 레이아웃 설정 (수직으로 위젯을 쌓는 QVBoxLayout 사용)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 1. 로봇 동작 버튼 생성 및 추가
        self.btn_move = QPushButton('Robot Run (이동)')
        self.btn_move.clicked.connect(self.move_robot) # 버튼 클릭 시 move_robot 함수 실행
        layout.addWidget(self.btn_move)

        # 2. 원점 이동 버튼 생성 및 추가
        self.btn_home = QPushButton('Home (원점)')
        self.btn_home.clicked.connect(self.go_home) # 버튼 클릭 시 go_home 함수 실행
        layout.addWidget(self.btn_home)

    # 슬롯 함수: 버튼이 눌렸을 때 실행될 기능들
    def move_robot(self):
        print("로봇 동작 버튼이 눌렸습니다.")

    def go_home(self):
        print("원점 이동 버튼이 눌렸습니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotController()
    window.show()
    sys.exit(app.exec_())