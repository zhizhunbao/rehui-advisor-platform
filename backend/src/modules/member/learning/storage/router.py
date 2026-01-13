"""文件存储路由"""
from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.responses import Response

from src.common.auth import get_current_user
from src.common.response import success_response
from .service import StorageService
from .converter import DocumentConverter

router = APIRouter(prefix="/storage", tags=["learning-storage"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    category: str = Query("general"),  # labs, assignments, resources
    user: dict = Depends(get_current_user),
):
    service = StorageService()
    content = await file.read()
    result = service.upload(user["id"], file.filename, content, category)
    return success_response(result.model_dump(mode="json"))


@router.get("")
def list_files(
    category: str | None = Query(None),
    user: dict = Depends(get_current_user),
):
    service = StorageService()
    files = service.list(user["id"], category)
    return success_response([f.model_dump(mode="json") for f in files])


@router.get("/{file_id}")
def get_file(file_id: str, user: dict = Depends(get_current_user)):
    service = StorageService()
    file = service.get(file_id, user["id"])
    return success_response(file.model_dump(mode="json"))


@router.get("/{file_id}/download")
def download_file(file_id: str, user: dict = Depends(get_current_user)):
    service = StorageService()
    filename, content = service.get_content(file_id, user["id"])
    
    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/{file_id}/convert")
def convert_to_markdown(file_id: str, user: dict = Depends(get_current_user)):
    """将 docx/pdf 转换为 markdown"""
    storage = StorageService()
    filename, content = storage.get_content(file_id, user["id"])
    
    converter = DocumentConverter()
    markdown = converter.convert(filename, content)
    
    return success_response({
        "file_id": file_id,
        "markdown": markdown,
        "original_filename": filename,
    })


@router.delete("/{file_id}")
def delete_file(file_id: str, user: dict = Depends(get_current_user)):
    service = StorageService()
    service.delete(file_id, user["id"])
    return success_response(None)
