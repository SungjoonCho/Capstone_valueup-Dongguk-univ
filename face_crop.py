
import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 칼라로 얼굴 부분 버튼 크롭

# 전체 사진에서 얼굴 부위만 잘라 리턴
def face_extractor(img):
    # 흑백처리
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 얼굴 찾기
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    # 찾은 얼굴이 없으면 None으로 리턴
    if faces is ():
        return None
    # 얼굴들이 있으면
    for (x, y, w, h) in faces:
        # 해당 얼굴 크기만큼 cropped_face에 잘라 넣기
        # 근데... 얼굴이 2개 이상 감지되면??
        # 가장 마지막의 얼굴만 남을 듯
        cropped_face = img[y:y + h, x:x + w]
    # cropped_face 리턴
    return cropped_face


user_id = input("이름을 입력하세요")

cap = cv2.VideoCapture(0)
face = None
while True:
    ret, frame = cap.read()

    face = face_extractor(frame)
    if face is not None:
        file_name_path = user_id + '.jpg'
        cv2.imwrite(file_name_path, face)
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()