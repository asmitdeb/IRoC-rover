from multiprocessing import Process, Queue, Value, Manager, Lock
from ultralytics import YOLO
import cv2
import math
import time
from heading_i2c_test import SCM_init_test
# from heading_i2c import CM_init, SCM_init, send_instruction, send_instruction_addr, turn_to_angle

def align(inference_data, lock, SAMPLE_PICKED, SAMPLE_DROPPED, frame_x, prev_inst, STOP_SAMP, STOP_CONT):

    with lock:
        temp_data = inference_data
    [class_name, area, center_x] = temp_data
    # print(temp_data)
    if class_name == "SAMPLE" and not SAMPLE_PICKED.value:
        print(f"------------------{area}-----------------")
        if (center_x>frame_x.value +20 and not STOP_SAMP.value):
            if not prev_inst.value == 4:
                # send_instruction(4) .
                time.sleep(5)
            print("Right")
            prev_inst.value = 4
        elif (center_x<frame_x.value-20 and not STOP_SAMP.value):
            if not prev_inst.value == 3:
                # send_instruction(3) .
                time.sleep(5)
            print("Left")
            prev_inst.value = 3

        elif(frame_x.value-20 < center_x <frame_x.value+20 and not STOP_SAMP.value):
            if not prev_inst.value == 1:
                # send_instruction(5) .
                time.sleep(1)
                # send_instruction(1) .
            print("Forward")
            prev_inst.value = 1

        if area>32500 and not STOP_SAMP.value:
            #send_instruction(20)
            # send_instruction(5) .
            # send_instruction_addr(8,1) .
            # send_instruction(2)
            # send_instruction(5) .
            time.sleep(5)
            STOP_SAMP.value = 1
            SAMPLE_PICKED.value = 1
            # turn_to_angle(0)

    if class_name == "CONTAINER" and SAMPLE_PICKED.value:
        if (center_x>frame_x.value+20 and not STOP_CONT.value):
            if not prev_inst.value == 4:
                # send_instruction(4) .
                time.sleep(5)
            print("Right")
            prev_inst.value = 4
        elif (center_x<frame_x.value-20 and not STOP_CONT.value):
            if not prev_inst.value == 3:
                # send_instruction(3) .
                time.sleep(5)
            print("Left")
            prev_inst.value = 3

        elif(frame_x.value-20 < center_x <frame_x.value+20 and not STOP_CONT.value):
            if not prev_inst.value== 1:
                # send_instruction(5) .
                #time.sleep(1) 
                # send_instruction(1) .
                time.sleep(5)
            print("Forward")
            prev_inst.value = 1

        if area>43000 and not STOP_CONT.value:
            #send_instruction(20)
            # send_instruction(5) .
            # send_instruction_addr(8,2) .
            # send_instruction(2) .
            # send_instruction(5) .
            time.sleep(5)
            STOP_CONT.value = 1
            SAMPLE_DROPPED.value = 1


def inference_cam(inference_data):
    print("Looking for container")
    # SAMPLE_PICKED = False
    # SAMPLE_DROPPED = False
    # start webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # frame_x = 320
    # frame_y = 240
    # model
    model = YOLO("balchal.pt")
    # model_ob = YOLO("dday.pt")

    # prev_inst = 5

    # STOP_SAMP = False
    # STOP_CONT = False
    # object classes
    classNames = ["OB150","OB300","SAMPLE", "CONTAINER"]
    #classNames = ["C20","C40"]
    # classNames = ["CONTAINER"]



    while True:
        success, img = cap.read()
        results_cont = model(img, stream=True, conf=0.6, verbose= False)
        #results = model(img, stream=True, conf=0.6)
        # coordinates
        for r in results_cont:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                center_x,center_y = (x2+x1)/2,(y2+y1)/2
                area = (x2-x1)*(y2-y1)

                # turn_to_angle(360-container_heading(center_x,center_y))
                cls = int(box.cls[0])
                class_name = classNames[cls]

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                # print(center_x,center_y )
                
                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                #cv2.putText(img, center, [center_x,center_y], font, fontScale, color, thickness)

                inference_data[:] = [class_name, area, center_x]
                # print(inference_data)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows() 


if __name__ == '__main__':
    # model = Queue()
    # curr_mode = Value('i', 0)
    #curr_mode = 0 for CM, 1 for AM
    SAMPLE_PICKED = Value('i', 0)
    SAMPLE_DROPPED = Value('i', 0)

    frame_x = Value('i', 320)
    frame_y = Value('i', 240)

    prev_inst = Value('i', 5)

    STOP_SAMP = Value('i', 0)
    STOP_CONT = Value('i', 0)

    manager = Manager()
    inference_data = manager.list()

    lock = Lock()

    MODE_INIT_RUNNING = False
    CAM_START = True

    inference_cam_process = Process(target=inference_cam, args=(inference_data, ))
    print("cam and inference started ")
    inference_cam_process.start()


    # while not MODE_INIT_RUNNING:
    while True:
        # MODE_INIT_RUNNING = True
        MODE = input("Enter mode: ")
        print(f"----------------------------CURRENTLY IN {MODE} MODE----------------------------")
        if(MODE == "SM"):
            continue
        elif(MODE == "CM"):
            # curr_mode.value = 0

            # if(CAM_START == True):
            #     print("cam started")
            #     inference_cam_process.start()
            #     CAM_START = False

            print("scm mode started")
            # MODE_INIT_RUNNING = True
            SCM_init_test()
            print("scm mode finished")
            # MODE_INIT_RUNNING = False

        elif(MODE == "AM"):
            # curr_mode.value = 1

            # if(CAM_START == True):
            #     print("cam started")
            #     inference_cam_process.start()
            #     CAM_START = False

            # MODE_INIT_RUNNING = True
            print("am mode started")
            # time.sleep(10)
            print("alignment process started")
            while True:
                if SAMPLE_DROPPED.value :
                    break
                align_process = Process(target=align, args=(inference_data, lock, SAMPLE_PICKED, SAMPLE_DROPPED, frame_x, prev_inst, STOP_SAMP, STOP_CONT))
                align_process.start()
                print("aligning rover")
                align_process.join()

            # align_process.join() #required?
            print("Reached final position")
            # MODE_INIT_RUNNING = False
        




