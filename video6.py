import numpy as np
import cv2
import os

cap = cv2.VideoCapture(0)

# выбор кодека и параметры исходного видео
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('demo.avi',fourcc, 10.0, (640,480))

# счетчик кадров
i = 0

# границы желаемого цвеа
# lower, upper =  ([25, 5, 58], [50, 36, 85]) #красный
# lower, upper =  ([238, 190, 71], [255, 255, 90]) #ярко синий
# lower, upper =  ([239, 250, 239], [255, 255, 255]) #зелено белый
lower, upper =  ([120, 250, 114], [255, 255, 254])
# преобразование границ в numpy формат
lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")



while(cap.isOpened()):
	# захватываем видео покадрово
    ret, frame = cap.read()
    
    # делаем нашу маску по цвету
    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask = mask)
    
    # если нет старой маски присваиваем текущей
    if "output_sum" not in globals():
        output_sum = output


    # прибавляем старую и новую маску
    output_sum  = cv2.add(output_sum,output)
    
    # очистить по нажатию клавиши r
    if cv2.waitKey(1) & 0xFF == ord('r'):
        output_sum = output

    # прибавляем кадр и маску
    frame = cv2.add(frame,output_sum)



    # отображаем результат
    cv2.imshow('frame',frame)

    # Режим только рисунок
    # cv2.imshow('frame',output_sum)
    

    # Дополнительно сохраняем кадры в папку images
    img_dir = 'images'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    path = img_dir + os.sep + 'frame{}.jpg'.format(i)
    cv2.imwrite(path,frame) 
    # увеличиваем счетчик кадров
    i += 1

    # записываем кадр
    out.write(frame)

    # выход по нажатию клавиши q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if not ret:
        break

# Отрубаем все и закрываем окно
cap.release()
out.release()
cv2.destroyAllWindows()