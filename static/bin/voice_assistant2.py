import pyttsx3
import speech_recognition as sr
import winsound
import time
import os
import datetime
import sys
from imageai.Detection import ObjectDetection
from imageai.Detection import VideoObjectDetection
import cv2
import numpy as np
import pyowm


def voic():
    talk = pyttsx3.init()

    voices = talk.getProperty('voices')
    talk.setProperty('voice', voices[0].id)

    file = open('Voice/comands/opts.txt', 'r', encoding='utf-8')
    sets = file.readlines()
    file.close()

    file2 = open('Voice/comands/answer.txt', 'r', encoding='utf-8')
    com = file2.readlines()
    file2.close()

    hi = 0

    # Добавление нового лица
    def add_face():
        sys.path.append(os.path.abspath("Voice/FacialRecognitionProject"))
        Respond(
            'Когда появится окно, посмотрите в разные стороны, а пока подготовтесь и смотрите, чтобы кроме вас никто не попал в кадр')

        from face_detected_real_time import first
        first()

        from face_detected_real_time import second
        second()

        Respond('Напишите то, как я должна называть это существо)')

        name = input('')
        file = open('Voice/FacialRecognitionProject/names.txt', 'a', encoding='utf-8')
        file.write(',' + name)
        file.close()

        Respond('Готово')

    # Распознование лиц с камеры в режиме real time
    def face_detected():
        Respond('Распознаю')
        sys.path.append(os.path.abspath("Voice/FacialRecognitionProject"))

        file = open('Voice/FacialRecognitionProject/names.txt', 'r', encoding='utf-8')
        names = file.read().split(',')
        file.close()

        from face_detected_real_time import third
        third(names)
        Respond('Лучше бы я этого не видела')

    # Распознование объектов на видео
    def video1():
        # Запись видео
        Respond("Чтобы остановить запись нажмите на клавишу 'Esc'")

        cap = cv2.VideoCapture(0)
        codec = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('Voice/captured.avi', codec, 25.0, (640, 480))
        while (cap.isOpened()):
            ret, frame = cap.read()
            if cv2.waitKey(10) == 27:
                break
            cv2.imshow('frame', frame)
            out.write(frame)

        out.release()
        cap.release()
        cv2.destroyAllWindows()

        # Обработка видео
        Respond("Обрабатываю видео...")
        execution_path = os.getcwd()

        detector = VideoObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path, "Voice/yolo.h5"))
        detector.loadModel()

        video_path = detector.detectObjectsFromVideo(
            input_file_path=os.path.join(execution_path, "Voice/captured.avi"),
            output_file_path=os.path.join(execution_path, "Voice/video_detected"),
            frames_per_second=20,
            log_progress=True
        )
        os.remove('Voice/captured.avi')

        print(video_path)

        # Воспроизведение готового видео
        try:
            Respond("Готово, вот что получилось:")
            while (True):
                cap = cv2.VideoCapture('Voice/video_detected.avi')
                while (cap.isOpened()):
                    ret, frame = cap.read()

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    cv2.imshow('frame', frame)
                    cv2.waitKey(30)

            cap.release()
            cv2.destroyAllWindows()
        except:
            cv2.destroyAllWindows()

    # Распознование фото по камере
    def phot1():
        try:
            cap = cv2.VideoCapture(0)
            Respond("Чтобы сделать фото нажмите на 'Q'")
            while (True):
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('Нажмите на "Q"', frame)

                # цвет cv2.imshow('frame',gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # Делаем снимок
                    ret, frame = cap.read()
                    # Записываем в файл
                    cv2.imwrite('Voice/objects.jpg', frame)
                    break

            Respond("Одну секундочку...")
            cap.release()
            cv2.destroyAllWindows()

            exec_path = os.getcwd()

            detector = ObjectDetection()
            detector.setModelTypeAsRetinaNet()
            detector.setModelPath(os.path.join(exec_path, "Voice/resnet50_coco_best_v2.0.1.h5"))
            detector.loadModel()

            list = detector.detectObjectsFromImage(
                input_image=os.path.join(exec_path, 'Voice/objects.jpg'),
                output_image_path=os.path.join(exec_path, 'Voice/new_objects.jpg'),
                minimum_percentage_probability=30
            )
            os.remove('Voice/objects.jpg')
            Respond("Готово!")

            cv2.imshow("Распознано", cv2.imread('Voice/new_objects.jpg'))
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        except:
            Respond('Произошла ошибка с импортом команд из текстового документа')

    def Decide(listen):
        # see what user said is in which list or not
        try:

            called = speech.recognize_google(voice, language="ru-RU").lower()

            for x in sets[0].split(","):
                if (x == (called.split()[0])) or (hi == 1):
                    leg = 1

                    cmd = called
                    for x in sets[0].split(","):
                        if x == (called.split()[0]):
                            cmd = cmd.replace(x, "").strip()  # все слова после Анисько
                        else:
                            cmd = cmd.replace(x, "").strip()

                    if (cmd != "") and (hi == 0):
                        cmd = recognize_cmd(cmd)
                        if cmd == 'hello':
                            execute_cmd(cmd)
                            return (1)

                    # распознаем и выполняем команду

                    if (cmd != "") and (hi == 1):
                        cmd = recognize_cmd(cmd)
                        execute_cmd(cmd)
                    elif (hi == 0):
                        Respond("Вас не учили здороваться?")
                        return (0)

                    break

            # Это для того, если ещё пользователь не поздаровался и первым словом не вызвал alias
            if hi == 0:
                Respond('Это вы кому?')
                return (0)




        except sr.UnknownValueError:
            Respond("я не смогла понять то, что вы сказали")
        except:
            print("не удалось запросить результаты")

    def recognize_cmd(cmd):
        for i in range(len(sets)):
            for j in sets[i].split(","):
                if j == cmd:
                    return sets[i].split(",")[0]

    def Respond(t):
        print(f"Анечка: {t}")  # to debug and see if everythings going okay

        talk.say(t)
        # talk.setProperty('rate', 300) #90 words per minute
        talk.runAndWait()

    def execute_cmd(cmd):
        m = 0
        try:
            for i in range(len(com)):
                if cmd == com[i].split()[0]:
                    i += 1
                    while com[i][0][0] != ';':
                        exec(com[i])
                        i += 1
                        m = 1
                    break
        except:
            Respond('Произошла ошибка с импортом команд из текстового документа')
            m = 1

        if m == 0:
            Respond('Команда не распознана, повторите!')

    while True:  # forever loop

        """
        The robot needs a WakeUp command so that it
        can start listening to.
        """
        try:
            print('\nГоворите')
            speech = sr.Recognizer()

            # take input from microphone
            with sr.Microphone() as source:
                # print("Вы сказали>>>")
                voice = speech.listen(source)
                print('...')
                called = speech.recognize_google(voice, language="ru-RU").lower()
                print(called)  # print what it heard just to debug

                if hi == 0:
                    hi = Decide(called)
                else:
                    Decide(called)

                if called in call_list:
                    comm = Listen()  # listen to what user says

                    Decide(comm)  # take decision and respond

        except:  # No wake up word found
            pass  # Do nothing avoiding the error

    print("""</body>
            </html>""")
