import cv2 
import sys
import numpy as np
import people_motion
import time

## cnt_down, cnt_up 정보를 통해 객차내의 승객수 계산 및 스크린 도어에 전달할 light 결정
def getlight_information(cnt_person, light, Calculate_the_passengers):
    if Calculate_the_passengers < 0:
        Calculate_the_passengers = 0

    number_of_people = Calculate_the_passengers + cnt_person

    if number_of_people < 1 and number_of_people >= 0:
        light = 'Green'
    elif number_of_people >= 1 and number_of_people < 2:
        light = 'Yellow'
    elif number_of_people >= 2:
        light = 'Red'

    if cnt_person == -1:
        print('Calculate_the_passengers:{} = {} - 1'.format(number_of_people, Calculate_the_passengers))
    elif cnt_person == 1:
        print('Calculate_the_passengers:{} = {} + 1'.format(number_of_people, Calculate_the_passengers))

    Calculate_the_passengers = number_of_people
    
    return light, Calculate_the_passengers

## 입력 영상 불러오기
cap = cv2.VideoCapture('TestVideo.avi')

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()
    
## 출력 이미지의 size 와 up&down counting 초기화
w, h = 640, 480
cnt_up, cnt_down = 0, 0

## 테스트 영상 저장하기
# fps = cap.get(cv2.CAP_PROP_FPS)
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# delay = round(1000/fps)
# out = cv2.VideoWriter('TestVideo output.avi', fourcc, fps, (w, h))

## 변수 초기화 
people = []
max_p_age = 5
person_index = 1
light = 'Green'
Calculate_the_passengers = 0

## Enter / Exit Lines 들을 정의
line_up = int(2.0 * (h/5))
line_down = int(2.5 *(h/5))

up_limit =   int(0.5*(h/5)) 
down_limit = int(4.5*(h/5))  

print("Down line의 경계선 (y의 값):", line_down)
print("Up line의 경계선 (y의 값):", line_up)

line_down_color = (255,0,0)
line_up_color = (0,0,255)

# down line에 대한 정보
pt1 =  [0, line_down];
pt2 =  [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))

# up line에 대한 정보
pt3 =  [0, line_up];
pt4 =  [w, line_up];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

# up limit line에 대한 정보
pt5 =  [0, up_limit];
pt6 =  [w, up_limit];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))

# down limit line에 대한 정보
pt7 =  [0, down_limit];
pt8 =  [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

## MOG2 기술을 사용하여 객체을 검출
MOG2 = cv2.createBackgroundSubtractorMOG2(detectShadows=True) # 그림자도 검출

## morphogenic filters를 위한 kernel 초기화 (3개의 kernel중 택 1)
kernelOp = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)
kernelOp2 = np.ones((3, 3), np.uint8)

while True:
    retval, frame = cap.read()

    if not retval:
        break

    ## frame을 640, 480 사이즈로 변환
    frame = cv2.resize(frame, (640, 480))

    # Method1. grayscale로 변환 후 Gaussian bluring을 적용
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    filtered_frame_gray = cv2.GaussianBlur(frame_gray, (0, 0), 3)

    for person in people:
        person.age_one() #age every person one frame

    ## MOG 배경 모델 적용 (foreground mask 두개 중에 택 1)
    fgmask1 = MOG2.apply(filtered_frame_gray)

    ## 그림자 없애기
    try:
        # fgmask1과 fgmask2 이미지를 이진화시키기
        _, bin_fgmask1 = cv2.threshold(fgmask1, 240, 255, cv2.THRESH_BINARY)
       
        # open(모폴리지)를 적용, 노이즈 제거하기 위해서
        mask = cv2.morphologyEx(bin_fgmask1, cv2.MORPH_OPEN, kernelOp)

        # close(모폴리지)를 적용, open으로 줄어든 면적을 다시 두껍게 만들기 위해서
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)

    except:
        print('End of file')
        print('UP:',cnt_up)
        print ('DOWN:',cnt_down)
        break

    ## mask와 mask2의 외각선 검출하기
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 노이즈 제거
        retval = cv2.contourArea(contour)

        if retval < 800 or retval > 15000:
            continue

        # 객체의 무게 중심점 구하기
        M = cv2.moments(contour)
        center_x = int(M['m10']/M['m00'])
        center_y = int(M['m01']/M['m00'])


        # 객체를 감싸는 최소 크기 사각형(바운딩 박스) 반환
        x,y,w,h = cv2.boundingRect(contour)

        # 객체의 무게 중심점의 y좌표가 up.limit와 down.limit 사이에 존재한다면
        new = True # 새로운 객체 있가?
        if center_y in range(up_limit, down_limit):
            for person in people:
                # 이 객체는 이미 존재했던 것이다.
                if abs(x - person.getX()) <= w and abs(y - person.getY()) <= h:
                    new = False
                    person.updateCoords(center_x, center_y) # person의 track 리스트에 [center_x, center_y]를 append해준다.
                    
                    if person.going_UP(line_down, line_up) == True:         
                        cnt_up += 1;
                        one_who_camp_up = -1
                        print("ID:",person.getId(),'crossed going up at',time.strftime("%c"))
                        light, Calculate_the_passengers = getlight_information(one_who_camp_up, light, Calculate_the_passengers)
                        one_who_camp_up = 0
                    elif person.going_DOWN(line_down, line_up) == True:
                        cnt_down += 1;
                        one_who_camp_down = 1
                        print( "ID:",person.getId(),'crossed going down at',time.strftime("%c"))
                        light, Calculate_the_passengers = getlight_information(one_who_camp_down, light, Calculate_the_passengers)
                        one_who_camp_down = 0
                    break

                # 객체가 line_down과 line_up 사이 존재한다면
                if person.getState() == '1':
                    # 객체의 방향이 down인 동시에 객체의 y좌표가 down_limit보다 크다면 확실히 아래로 내려온 객체이다.
                    if person.getDir() == 'down' and person.getY() > down_limit:
                        person.setDone()
                    # 객체의 방향이 up인 동시에 객체의 y좌표가 up_limit보다 작으면 확실히 아래로 내려온 객체이다.
                    elif person.getDir() == 'up' and person.getY() < up_limit:
                        person.setDone()
                       
                # 세팅이 끝났으면
                if person.timedOut():
                    index = people.index(person)
                    people.pop(index) # people 리스트에서 person 정보만 끄집어 내기
                    del person    
            if new == True:
                # 객체의 정보들을 person_inf 변수에 대입 후, people 리스트에 append 시켜준다.
                person_inf = people_motion.person_information(person_index, center_x, center_y, max_p_age)
                people.append(person_inf)
                person_index += 1   

        cv2.circle(frame, (center_x,center_y), 5, (0,0,255), -1)
        # img = cv2.rectangle(frame,(x, y), (x+w, y+h), (0,255,0), 2)   
        # cv2.drawContours(frame, contour, -1, (0,255,0), 3)   
    
    # 객체에 정보 표시
    # for person in people:
    #     cv2.putText(frame, str(person.getId()), (person.getX(),person.getY()), cv2.FONT_HERSHEY_SIMPLEX,0.3, person.getRGB(), thickness=1, lineType=cv2.LINE_AA)

    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    light_information = 'Light: ' + str(light)

    # Lines들 화면 표시
    frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)

    # Limit Lines들 화면 표시
    # frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    # frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)

    cv2.putText(frame, str_up ,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_up ,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv2.LINE_AA)

    # 스크린 도어의 Light 정보를 화면에 표시
    cv2.putText(frame, light_information ,(530, 40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv2.LINE_AA)

    # out.write(frame) # 영상 데이터만 저장. 소리는 X
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)    

    if cv2.waitKey(30) == 27:
        break

    
cap.release()
cv2.destroyAllWindows()

## TestVideo.avi 일 경우
# 모폴리지 OPEN은 적용하지만, 모폴리지 CLOSE은 적용하지 않는다. Threshold = 900 ~ 1200

## TestVideo2.mp4 일 경우
# GuassianBlur 적용하고, 모폴리지 OPEN과 CLOSE 모두 적용하고 Threshold = 1990으로 적용

## TestVideo4.mp4 일 경우
# GuassianBlur 적용하고, 모폴리지 OPEN(kernelCl2, (21, 21))과 CLOSE(kernelCl3, (121, 121)) 모두 적용하고 Threshold = 9000으로 적용