import sys
import serial
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QSlider, QHBoxLayout, QTextEdit)
from PyQt5.QtCore import Qt, QTimer

class RobotController(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 시퀀스 저장을 위한 리스트 초기화
        self.sequence = [] 
        self.is_running = False
        
        # 시퀀스 실행을 위한 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_next_step)
        self.current_step = 0
        
        self.initUI()
        self.initSerial()

    def initSerial(self):
        try:
            self.ser = serial.Serial('COM6', 115200, timeout=1) # 포트 확인 필수
            time.sleep(2)
        except:
            self.ser = None
            print("시리얼 연결 실패")

    def initUI(self):
        self.setWindowTitle('4축 로봇암 티칭 시스템')
        self.setGeometry(100, 100, 500, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # ===== 상단: 시퀀스 표시 텍스트 윈도우 추가 =====
        layout.addWidget(QLabel("=== Recorded Sequence ==="))
        
        # QTextEdit: 여러 줄 텍스트를 표시할 수 있는 위젯 (읽기 전용)
        self.txt_sequence = QTextEdit()
        self.txt_sequence.setReadOnly(True)  # 사용자가 직접 수정 불가
        self.txt_sequence.setMaximumHeight(150)  # 높이 제한
        self.txt_sequence.setPlaceholderText("레코딩된 시퀀스가 여기에 표시됩니다...")
        layout.addWidget(self.txt_sequence)
        
        layout.addWidget(QLabel("--- Robot Control ---"))

        # 슬라이더 & 라벨 (이전과 동일)
        self.sliders = []
        self.labels = []
        # 아두이노 프로토콜 순서에 맞춘 명명
        names = ["Base (회전)", "Shoulder (어깨)", "UpperArm (팔꿈치)", "ForeArm (손목)"]
        
        for i, name in enumerate(names):
            lbl = QLabel(f"{name}: 90")
            self.labels.append(lbl)
            layout.addWidget(lbl)
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 180)
            slider.setValue(90)
            slider.valueChanged.connect(lambda val, idx=i: self.update_label(idx, val))
            self.sliders.append(slider)
            layout.addWidget(slider)

        # 기본 제어 버튼
        btn_layout = QHBoxLayout()
        self.btn_move = QPushButton('Robot Run')
        #self.btn_move.clicked.connect(self.move_robot)
        self.btn_move.clicked.connect(lambda: self.move_robot())
        btn_layout.addWidget(self.btn_move)

        self.btn_home = QPushButton('Home')
        self.btn_home.clicked.connect(self.go_home)
        btn_layout.addWidget(self.btn_home)
        layout.addLayout(btn_layout)

        # 구분선
        layout.addWidget(QLabel("--- Sequence Control ---"))

        # 시퀀스 제어 버튼 추가
        self.lbl_status = QLabel("저장된 동작: 0개")
        layout.addWidget(self.lbl_status)

        self.btn_record = QPushButton('Record Pose (기록)')
        self.btn_record.clicked.connect(self.record_pose)
        layout.addWidget(self.btn_record)

        seq_btn_layout = QHBoxLayout()
        self.btn_start_seq = QPushButton('Sequence Run Start')
        self.btn_start_seq.clicked.connect(self.start_sequence)
        seq_btn_layout.addWidget(self.btn_start_seq)

        self.btn_stop_seq = QPushButton('Sequence Run Stop')
        self.btn_stop_seq.clicked.connect(self.stop_sequence)
        seq_btn_layout.addWidget(self.btn_stop_seq)
        layout.addLayout(seq_btn_layout)

        # 시퀀스 초기화 버튼 추가
        self.btn_clear = QPushButton('Clear Sequence (초기화)')
        self.btn_clear.clicked.connect(self.clear_sequence)
        layout.addWidget(self.btn_clear)

    def update_label(self, index, value):
        names = ["Base (회전)", "Shoulder (어깨)", "UpperArm (팔꿈치)", "ForeArm (손목)"]
        self.labels[index].setText(f"{names[index]}: {value}")

    def update_sequence_display(self):
        """시퀀스 리스트를 텍스트 윈도우에 업데이트"""
        self.txt_sequence.clear()
        
        if not self.sequence:
            self.txt_sequence.setPlaceholderText("레코딩된 시퀀스가 없습니다.")
            return
        
        # 시퀀스를 한 줄씩 표시 (맨 처음 레코딩이 맨 위)
        for i, angles in enumerate(self.sequence, 1):
            # 포맷: Step 1: [Base:90, Shoulder:45, UpperArm:120, ForeArm:90]
            line = f"Step {i}: [B:{angles[0]:3d}, S:{angles[1]:3d}, U:{angles[2]:3d}, F:{angles[3]:3d}]\n"
            self.txt_sequence.append(line.strip())

    def move_robot(self, angles=None):
        if self.ser is None: return
        
        # 인자가 없으면 현재 슬라이더 값 사용
        if angles is None:
            angles = [s.value() for s in self.sliders]
            
        cmd = f"2a{angles[0]}b{angles[1]}c{angles[2]}d{angles[3]}e\n"
        self.ser.write(cmd.encode())
        print(f"Move: {cmd.strip()}")

    def go_home(self):
        if self.ser is None: return
        #self.stop_sequence()  # 무한 리컬션 에러 
        self.ser.write("3\n".encode())
        for s in self.sliders: s.setValue(90)
        print("Go Home")

    def record_pose(self):
        """현재 슬라이더 값들을 리스트로 저장"""
        current_angles = [s.value() for s in self.sliders]
        self.sequence.append(current_angles)
        
        # 상태 라벨 업데이트
        self.lbl_status.setText(f"저장된 동작: {len(self.sequence)}개")
        
        # 텍스트 윈도우 업데이트
        self.update_sequence_display()
        
        print(f"Recorded: {current_angles}")

    def clear_sequence(self):
        """저장된 시퀀스 모두 삭제"""
        self.sequence.clear()
        self.lbl_status.setText("저장된 동작: 0개")
        self.update_sequence_display()
        print("Sequence Cleared")

    def start_sequence(self):
        if not self.sequence:
            print("저장된 시퀀스가 없습니다.")
            return
        self.is_running = True
        self.current_step = 0
        self.timer.start(2000) # 2초마다 다음 동작 실행 (로봇 속도 고려)
        print("Sequence Started")
        
        # 첫 번째 동작 즉시 실행
        self.run_next_step()

    def run_next_step(self):
        if not self.is_running: return
        
        # 현재 스텝의 각도 가져오기
        angles = self.sequence[self.current_step]
        
        # UI 슬라이더 업데이트 (시각적 피드백)
        for i, val in enumerate(angles):
            self.sliders[i].setValue(val)
            
        # 로봇으로 명령 전송
        self.move_robot(angles)
        
        print(f"Executing Step {self.current_step + 1}/{len(self.sequence)}")
        
        # 다음 스텝 준비 (무한 반복)
        self.current_step += 1
        if self.current_step >= len(self.sequence):
            self.current_step = 0

    def stop_sequence(self):
        self.is_running = False
        self.timer.stop()
        print("Sequence Stopped")
        self.go_home() # 정지 후 원점 복귀

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotController()
    window.show()
    sys.exit(app.exec_())