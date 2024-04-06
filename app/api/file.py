import os
from datetime import datetime
from fastapi import APIRouter, File, UploadFile, Form
from typing import List, Optional
from uuid import uuid4
file = APIRouter()


@file.post("/upload", summary="文件上传")
def upload(file: UploadFile, name: str = Form(None, description="文件名"), path: str = Form(None, description="文件上传路径")):
    try:
        base_dir = "public/storage/upload"
        now = datetime.now().strftime('%Y-%m-%d')
        dir_path = os.path.join(base_dir, now)

        if name:
            unique_filename = name
        else:
            unique_filename = f"{uuid4()}-{file.filename}"

        if path:
            dir_path = os.path.join(base_dir, path)

        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, unique_filename)

        with open(file_path, "wb") as f:
            for line in file.file:
                f.write(line)

        return {"path": file_path, "code": 200}
    except OSError as e:
        return {"error": f"An error occurred: {e}"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

    finally:
        pass
