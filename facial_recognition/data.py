def faces():
    import os
    import pickle

    with open('dataset_faces.pickle', 'rb') as f:
        data = pickle.load(f)
    known_names = list(data.keys())

    return(known_names)
