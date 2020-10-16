def recognizer():
    import face_recognition
    import cv2
    import os
    import pickle
    import numpy as np
    import time
    from facial_recognition.settings.local import BASE_DIR
    

    start = time.time()
    KNOWN_FACES_DIR = str(BASE_DIR)+"/known_faces"
    UNKNOWN_FACES_DIR = str(BASE_DIR)+"/unknown_faces"
    TOLERANCE = 0.6
    FRAME_THICKENESS = 3
    FONT_THICKENESS = 2
    MODEL = "cnn"  #hog cnn
    TOTAL = 0 
    li=[]

    with open('dataset_faces.pickle', 'rb') as f:
        data = pickle.load(f)
    known_names = list(data.keys())
    known_faces = np.array(list(data.values()))

    os.system('clear')

    print("Processing unknown faces.............")
    print()

    for filename in os.listdir(UNKNOWN_FACES_DIR):
        print('Processing {0} image'.format(filename))

        TOTAL +=1

        image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
        scale_percent = 80 # percent of original size
        width = image.shape[1]
        height = image.shape[0]
        width = (1080 if 1080 < int(width * scale_percent / 100) else int(width * scale_percent / 100))
        height = (600 if 600 < int(height * scale_percent / 100) else int(height * scale_percent / 100))
        dim = (width, height) 
        image = cv2.resize(image, dim, cv2.INTER_AREA)
        locations = face_recognition.face_locations(image,model=MODEL)
        encodings = face_recognition.face_encodings(image,locations)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(known_faces,face_encoding,TOLERANCE)
            match = None

            if True in results:
                match = known_names[results.index(True)]
                match = match.replace('_',' ')
                if match not in li:
                    li.append(match)
            else:
                match = 'unknown'   

            top_left = (face_location[3],face_location[0])
            bottom_right = (face_location[1],face_location[2])

            color = [250,250,250]

            cv2.rectangle(image,top_left, bottom_right, color, FRAME_THICKENESS)

            top_left = (face_location[3],face_location[2])
            bottom_right = (face_location[1],face_location[2]+22)

            cv2.rectangle(image,top_left, bottom_right, color, cv2.FILLED)

            
            cv2.putText(image,match,(face_location[3]+10,face_location[2]+15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),FONT_THICKENESS)
        
        

        # cv2.imshow(filename, image)
        # cv2.waitKey(4000)
        # cv2.destroyAllWindows() 

    end = time.time()    
    processed_time = (end-start)
    min = processed_time // 60
    sec = processed_time % 60
    hrs=0

    if (min >= 60):
        hrs = min // 60;  
        min = min % 60; 
    time = [int(hrs),int(min),int(sec)]
    print()
    print('Total image Processed ',TOTAL)
    if len(li) == 0:
        print('NO Known Faces Found ... ')
    else:
        print('Known Faces in images are ....')
        print('[',end=' ')
        print(*li,sep = ', ',end=' ]')
        print()
    print("Runtime of the program is ------  {0}H {1}M {2}S".format(int(hrs),int(min),int(sec)))
    m=[]
    m.append(li)
    m.append(TOTAL)
    m.append(time)
    return(m)