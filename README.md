## Personal-Project_counting-people-who-enter-in-subway-by-using-opencv

### 1. 목적
- 카메라와 OpenCV를 통해 실시간으로 승객의 탑승 여부를 확인한 뒤, 이를 바탕으로 지하철의 혼잡도를 계산합니다.
  이렇게 계산된 혼잡도는 스크린 도어 상단에 설치된 RGB Diode를 통해 승객에게 전달되게 됩니다.
- 전달된 정보를 통해 승객들은 현재 대기하고 있는 칸에 대한 지하철 혼잡도를 확인할 수 있습니다.
  또한, 승객들은 해당 정보를 통해 지하철 혼잡도가 상대적으로 적은 칸으로 이동하여 지하철 혼잡도를 완화시킬 수 있습니다.

<br><br>

### 2. 프로젝트의 목표
- Python과 OpenCV를 통해 테스트 영상과 카메라를 통한 실시간 환경에서 객체를 인식할 수 있도록 구현
- 라즈베리파이4를 이용하여 계산된 혼잡도 정보를 RGB Diode를 통해 출력되도록 설계

<br><br>

### 3. System Diagram
<p align="center">
  <img src="./Images/시스템 구상도.jpg" style="width: 50%; height: auto;">
</p>

<br><br>

### 5. MIT App Inventor
<p>
  <img src="./Images/App Inventor Bluetooth Logic.jpg" style="width: 30%; height: auto;">
  <br>
  <img src="./Images/App Inventor Bluetooth Send Text.jpg" style="width: 30%; height: auto;">
</p>  

<br><br>

### 5. Implementation
<p>
  <img src="./Images/하드웨어 구현.jpg" style="width: 50%; height: auto;">
</p>
