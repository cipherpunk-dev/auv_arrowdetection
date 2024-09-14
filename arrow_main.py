import sys
import cv2
import numpy as np
import math as m
def line_solver(m1,m3,point1,point2):
    x1,y1=point1
    x3,y3=point2
    x=(m3*x3-m1*x1+y1-y3)/(m3-m1)
    y=(m3*y1-m1*y3+m1*m3*(x3-x1))/(m3-m1)
    return x,y
def those_point(diag,sorted_details):
    for file in diag:
        slope=file[0]
        for i in range(1,3):
            x1,y1=file[i]
            count = 0
            for j in range(0,4):
                for k in range(1,3):
                    x,y=sorted_details[j][k]
                    val=slope*(y)+x-slope*(y1)-x1
                    if val>0 :
                        count=count+1
                    elif val<0 :
                        count=count-1
                    else :
                        count=count
            if count == 8 or count == -8:
                return [(x1,y1),file]
def arrow_sep_bycolor(source):
    hsv=cv2.cvtColor(source,cv2.COLOR_BGR2HSV)
    lower_hsv=np.array([0,0,160])
    upper_hsv=np.array([40,255,255])
    mask=cv2.inRange(hsv,lower_hsv,upper_hsv)
    # 1 and 1 then only 1 ho , so that's why "and" is used here 1, 0 means pixels here
    result=cv2.bitwise_and(hsv,hsv,mask=mask)
    re = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    return re
def angle_finder(dictator):
    for i in range(1,3):
        if dictator[1][i] != dictator[0]:
            tail=dictator[1][i]
            head=dictator[0]
    x_tail, y_tail = tail
    x_head, y_head = head
    dx = x_head - x_tail
    dy = -y_head + y_tail
    if dy == 0:
        angle_radians = 0
    else:
        angle_radians = m.atan2(dx, dy)  # atan2(dx, dy) gives angle with the vertical
    angle_degrees = m.degrees(angle_radians)
    print(angle_degrees)
    if dx >= 0 and dy >= 0:
        print("First quadrant")
    elif dx < 0 <= dy:
        print("Second quadrant")
    elif dx < 0 and dy < 0:
        print("Third quadrant")
    elif dx >= 0 > dy:
        print("Fourth quadrant")
    return angle_degrees
def compressor(source):
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)
    return edges
def line_detect(source):
    lines = cv2.HoughLinesP(source, 1, np.pi / 180, 40,minLineLength=50,maxLineGap=10)
    details = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            p1=(x1,y1)
            p2=(x2,y2)
            if x2-x1 == 0:
                slope = sys.maxsize
            else:
                slope=(y2-y1)/(x2-x1)
            details.append([slope,p1,p2])
            sorted_details = sorted(details, key=lambda x: x[0])
        return sorted_details
def polygon_create(array):
    m1,m2,m3,m4=array[0][0],array[1][0],array[2][0],array[3][0]
    p11,p12,p13,p14=array[0][1],array[1][1],array[2][1],array[3][1]
    poly_1=line_solver(m1,m3,p11,p13)
    poly_2=line_solver(m2,m3,p12,p13)
    poly_3=line_solver(m2,m4,p12,p14)
    poly_4=line_solver(m1,m4,p11,p14)
    mapp=[poly_1,poly_2,poly_3,poly_4]
    return mapp
def diagonals_locater(rectangle):
    pt1=rectangle[0]
    pt2=rectangle[1]
    pt3=rectangle[2]
    pt4=rectangle[3]
    if pt3[0]-pt1[0] == 0 :
        slope1=sys.maxsize
    elif pt2[0]-pt4[0] == 0 :
        slope2=sys.maxsize
    else:
        slope1=(pt3[1]-pt1[1])/(pt3[0]-pt1[0])
        slope2=(pt4[1]-pt2[1])/(pt4[0]-pt2[0])
    loc1=[slope1,pt1,pt3]
    loc2=[slope2,pt2,pt4]
    return loc1,loc2
img=cv2.imread("resources/arrow_new.jpg")
img_up=cv2.imread("resources/arrow_new_up.jpg")
img_dwn=cv2.imread("resources/arrow_new_down.jpg")
img_ri=cv2.imread("resources/arrow_new_ri.jpg")
kernel = np.ones((5, 5), np.uint8)
def menu(source):
    ans='y'
    while ans=='y':
            print("press 1 to get angle")
            print()
            print("Angle in 1st , 4th quad measured from vertical are positive")
            print("Angle in 2nd , 3rd quad measured from vertical are negative")
            ch=int(input("Enter\t"))
            if ch == 1:
                process1 = arrow_sep_bycolor(source)
                process2 = compressor(process1)
                arr = line_detect(process2)
                rho = polygon_create(arr)
                diag = diagonals_locater(rho)
                fin = those_point(diag, arr)
                x1, y1 = fin[1][1]
                x2, y2 = fin[1][2]
                n1, n2 = int(x1), int(y1)   #may not show that exact line coz rounded off
                m1, m2 = int(x2), int(y2)   #but angle would be correct
                point1 = (n1, n2)
                point2 = (m1, m2)
                print(angle_finder(fin))
                x = img_dwn.copy()
                cv2.line(x, point1, point2, (0, 0, 255), 1) #RED
                cv2.imshow("win1", x)
            else : print("WTF")
            if cv2.waitKey(0) & 0xff == ord('q'):
                cv2.destroyAllWindows()
            ans = input("DO YOU WANt to Continue??(y/n)\t")
menu(img_dwn)

