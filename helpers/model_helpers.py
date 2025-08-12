def get_trained_model(model_directory: str):
    """
    Gets the most recently trained model from the specified path.

    Args:
        model_directory (str): Path to the parent directory of the MLFLOW model structure.

    Return:
        trained_model: YOLO-model object initialized with the best weights of the most recent run.

    Raises:
        None.
    """
    import os
    from ultralytics import YOLO
    
    subdirectories = [d for d in os.listdir(model_directory) if os.path.isdir(os.path.join(model_directory, d))]
    most_recent_directory = max(subdirectories, key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 0)
    model_path = os.path.join(model_directory, most_recent_directory, 'weights', 'best.pt')
    print(f'Using {most_recent_directory}.')
    trained_model = YOLO(model_path)
    
    return trained_model, model_path


def copy_file(source_path, destination_path):
    import os, shutil, uuid
    """
    Copy a file from source_path to destination_path, prepending a unique ID to the filename.

    Args:
        source_path (str): The path to the source file.
        destination_path (str): The path to the destination directory where the file will be copied.

    Returns:
        None
    """
    try:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"The file '{source_path}' does not exist.")

        unique_id = str(uuid.uuid4())
        filename, extension = os.path.splitext(os.path.basename(source_path))
        new_filename = f"{unique_id}_{filename}{extension}"
        destination_path_with_id = os.path.join(os.path.dirname(destination_path), new_filename)
        os.makedirs(os.path.dirname(destination_path_with_id), exist_ok=True)
        shutil.copy2(source_path, destination_path_with_id)

        print(f"File '{source_path}' successfully copied to '{destination_path_with_id}'.")
    except Exception as e:
        print(f"An error occurred: {e}")