def capture_images(num_imgs: int,
                   classes: list,
                   img_path: str,
                   device: int = 0,
                   delay: int = 3,
                   show: bool = True) -> None:
    """
    Captures images from a specified video device and saves them to disk.

    Args:
        num_imgs (int): The number of images to capture per class.
        classes (list): A list of strings representing the classes or labels for which images are to be captured.
        img_path (str): The directory path where the captured images will be saved.
        device (int, optional): The index of the video capturing device. Defaults to 0.
        delay (int, optional): The delay in seconds between capturing each image. Defaults to 3.
        show (bool, optional): If True, displays the current captured image during the process. Defaults to True.

    Returns:
        None

    Raises:
        None
    """
    import cv2, time, os, uuid
    cap = cv2.VideoCapture(device)
    if not os.path.exists(img_path):
        os.makedirs(img_path)
        
    for label in classes:
        print('Bilder für Label: {}'.format(label))
        time.sleep(3)
        
        for img_num in range(num_imgs):
            print('Aufnahme für {}, Bild {}'.format(label, img_num))
            
            ret, frame = cap.read()
            imgname = os.path.join(img_path, label+'.'+str(uuid.uuid1())+'.jpg')
            cv2.imwrite(imgname, frame)
            
            if show:
                cv2.imshow('Aktuelles Bild', frame)
            
            time.sleep(delay)
            if cv2.waitKey(1) == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()
    print(f'Images saved at {img_path}.')



def display_images(directory_path):
    """
    Display all images in the specified directory in a grid using Matplotlib.

    Args:
        directory_path (str): The path to the directory containing the images.

    Returns:
        None
    """
    import os, math
    import matplotlib.pyplot as plt
    from matplotlib.image import imread
    
    files = os.listdir(directory_path)
    image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    num_images = len(image_files)
    cols = 4  
    rows = math.ceil(num_images / cols)  
    fig, axes = plt.subplots(rows, cols, figsize=(12, 12))
    
    for i, file in enumerate(image_files):
        row = i // cols
        col = i % cols
        img_path = os.path.join(directory_path, file)
        img = imread(img_path)
        if img is not None:
            axes[row, col].imshow(img)
            axes[row, col].axis('off')
            axes[row, col].set_title(file.split('.')[0])
    
    plt.tight_layout()
    plt.show()

def display_video_with_inference(video_path: str,
                                 model) -> None:
    import cv2
    cap = cv2.VideoCapture(video_path) # Definieren des Aufnahmegeräts (hier freilich ein Video und kein 'Gerät')

    ### Wir extrahieren die Frames aus dem Video und lassen das Modell eine Vorhersage auf allen treffen
    ### Dann visualisieren wir die Frames
    while cap.isOpened():
        success, frame = cap.read() # Aufnehmen eines Frames aus dem Video
    
        if success: # Wenn der Frame nicht fehlerhaft ist...
    
            # Modell trifft Vorhersage
            results = model(frame)
    
            # Visualisieren des Bildes mit Bounding Boxes
            annot_img = results[0].plot()
            cv2.imshow("Model Prediction", annot_img)
    
            # Beende die Schleife, falls q gedrückt wird (um vorzeitig aus dem Vorhersage-Loop rauszukommen)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Beende die Schleife, falls das Ende des Videos erreicht wurde
            break
    
    ### Ressourcen freigeben und alle Fenster schließen
    cap.release()
    cv2.destroyAllWindows()


def inference_with_webcam(model,
                          device: int = 0) -> None:
    import cv2
    ### Hier haben wir etwas verändert
    cap = cv2.VideoCapture(device) # Definieren des Aufnahmegeräts: Webcam || Die integrierte Webcam ist normalerweise Gerät 0
                              # Wenn eine USB-Webcam (oder ein anderes Aufnahmegerät) verwendet werden soll, muss dieser Wert angepasst werden.
                              # Oft ist die USB-Webcam dann Gerät 1, bei mir z.B. aber Gerät 4. Da hilft nur Ausprobieren.
    
    ### Ab hier ist wieder alles gleich wie beim "normalen" Video
    while cap.isOpened():
        success, frame = cap.read() 
    
        if success: 
            results = model(frame)
            annot_img = results[0].plot()
            cv2.imshow("Model Prediction", annot_img)
    
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    
    cap.release()
    cv2.destroyAllWindows()
