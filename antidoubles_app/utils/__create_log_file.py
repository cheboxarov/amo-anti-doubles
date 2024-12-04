import os
import time

def create_log_file(dir: str, file_name: str, content: str) -> str:
    os.makedirs(dir, exist_ok=True)
    filename = f"{dir}/{file_name}_{time.time()}.log"
    with open(filename, "w+") as file:
        file.write(content)
    return filename