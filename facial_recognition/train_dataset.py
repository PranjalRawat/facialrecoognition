def train():
    import face_recognition
    import cv2
    import os
    import pickle
    from facial_recognition.settings.local import BASE_DIR

    KNOWN_FACES_DIR = str(BASE_DIR)+"/known_faces"


    os.system('clear')
    print("Loading all the Faces {0}".format('.'*55))
    print()

    known_faces = []
    known_names = []


    all_face_encodings = {}

    dataset_faces = 'dataset_faces.pickle'

    if os.path.exists(dataset_faces):
        with open("dataset_faces.pickle", "rb") as file:
            all_face_encodings = pickle.load(file)

    for name in os.listdir(KNOWN_FACES_DIR):
        print('Training {0} face {1} ( Processed )'.format(name,'.'*(50-len(name))))
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            
            try:
                encoding = face_recognition.face_encodings(image)[0]
                all_face_encodings[name] = encoding
            except IndexError:
                print('{0} is not suitable for Training the dataset'.format(filename))
                    
                
            

    print()
    print("All faces has been trained")
    print()

    with open("dataset_faces.pickle", "wb") as file:
        pickle.dump(all_face_encodings, file)
