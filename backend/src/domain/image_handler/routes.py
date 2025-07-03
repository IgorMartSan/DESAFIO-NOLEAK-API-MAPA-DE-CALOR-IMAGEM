from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from domain.image_handler.use_cases import UseCases

from PIL import Image
from io import BytesIO
from tempfile import NamedTemporaryFile
import shutil
import os

router = APIRouter(prefix="/draw", tags=["Visualização"])

JSON_PATH = "/workspaces/FIAP---Tech-Challenge-Fase-1---Vitivinicultura-Embrapa-API/backend/src/resp.json"
OBJETO_ALVO_DEFAULT = "person"


def salvar_upload_temp(image: UploadFile) -> str:
    try:
        suffix = os.path.splitext(image.filename)[-1]
        temp = NamedTemporaryFile(delete=False, suffix=suffix)
        with temp as f:
            shutil.copyfileobj(image.file, f)
        return temp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")


@router.post("/bbox")
def gerar_bounding_boxes(image: UploadFile = File(...), objeto_alvo: str = OBJETO_ALVO_DEFAULT):
    img = Image.open(BytesIO(image.file.read()))
    json_data = UseCases.load_json(JSON_PATH)
    result_image = UseCases.draw_bounding_boxes_from_image(json_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post("/heatmap")
def gerar_heatmap(image: UploadFile = File(...), objeto_alvo: str = OBJETO_ALVO_DEFAULT):
    img = Image.open(BytesIO(image.file.read()))
    json_data = UseCases.load_json(JSON_PATH)
    result_image = UseCases.generate_heatmap_from_image(json_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post("/heatmap_bbox")
def gerar_heatmap_com_bounding_boxes(image: UploadFile = File(...), objeto_alvo: str = OBJETO_ALVO_DEFAULT):
    img = Image.open(BytesIO(image.file.read()))
    json_data = UseCases.load_json(JSON_PATH)
    result_image = UseCases.draw_heatmap_and_bounding_boxes_from_image(json_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
