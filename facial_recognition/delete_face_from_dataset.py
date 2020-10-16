def deletee(title):
    import face_recognition
    import cv2
    import os
    import pickle
    import sys

    dataset_faces = 'dataset_faces.pickle'

    if os.path.exists(dataset_faces):
        with open("dataset_faces.pickle", "rb") as file:
            all_face_encodings = pickle.load(file)

    os.system('clear')    
    name = title
    if name in all_face_encodings:
        all_face_encodings.pop(name)
        with open("dataset_faces.pickle", "wb") as file:
            pickle.dump(all_face_encodings, file)
        print('Done')
        return True
    else:
        print('Not Done')
        return False

    
