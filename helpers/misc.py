def show_directory(path: str, 
                   show_files=False) -> None:
    import os
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        if (os.path.basename(root).startswith('.') or os.path.basename(root).startswith('__')):
            continue
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        if show_files:
            for f in files:
                print('{}{}'.format(subindent, f))


def move_file(source_path: str,
              destination_path: str) -> None:
    
    """
    Copy a file from source_path to destination_path, prepending a unique ID to the filename.

    Args:
        source_path (str): The path to the source file.
        destination_path (str): The path to the destination directory where the file will be copied.

    Returns:
        None
    """
    
    import os, shutil, uuid

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