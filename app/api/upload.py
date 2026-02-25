from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.utils.file_upload import get_upload_path, save_upload_file

upload_router = APIRouter(prefix="/api", tags=["upload"])


@upload_router.post("/upload", response_model=dict)
async def upload_file(file: UploadFile = File(...)):
    if file.size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty",
        )

    try:
        upload_dir = get_upload_path()
        filename = save_upload_file(file, str(upload_dir))
        return {"url": f"/uploads/{filename}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}",
        )
