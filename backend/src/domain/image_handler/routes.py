from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from domain.image_handler.use_cases import UseCases

from PIL import Image
from io import BytesIO
from tempfile import NamedTemporaryFile
import shutil
import os

router = APIRouter(prefix="/draw", tags=["Visualização"])

# Caminho fixo do JSON de exemplo
JSON_PATH = r"/workspaces/DESAFIO-NOLEAK-API-MAPA-DE-CALOR-IMAGEM/backend/src/resp.json"
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


@router.post(
    "/bbox",
    summary="Desenhar bounding boxes",
    description="Recebe uma imagem e desenha bounding boxes baseadas nas informações do JSON. "
                "Você pode especificar o tipo de objeto desejado (ex: 'person', 'car')."
)
def gerar_bounding_boxes(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG", openapi_extra={"example": "exemplo.jpg"}),
    objeto_alvo: str = Form(
        OBJETO_ALVO_DEFAULT,
        description="Classe do objeto a ser destacada",
        examples={
            "person": {"value": "person"},
            "car": {"value": "car"},
        }
    )
):
    img = Image.open(BytesIO(image.file.read()))
    json_data = UseCases.load_json(JSON_PATH)
    result_image = UseCases.draw_bounding_boxes_from_image(json_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post(
    "/heatmap",
    summary="Gerar heatmap da imagem",
    description="Recebe uma imagem e retorna um heatmap baseado nas ocorrências do objeto alvo no JSON."
)
def gerar_heatmap(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG", openapi_extra={"example": "exemplo.jpg"}),
    objeto_alvo: str = Form(
        OBJETO_ALVO_DEFAULT,
        description="Classe do objeto para geração do heatmap",
        examples={
            "person": {"value": "person"},
            "vehicle": {"value": "vehicle"},
        }
    )
):
    img = Image.open(BytesIO(image.file.read()))
    json_data = UseCases.load_json(JSON_PATH)
    result_image = UseCases.generate_heatmap_from_image(json_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post(
    "/heatmap_bbox",
    summary="Gerar heatmap com bounding boxes",
    description="Recebe uma imagem e retorna um heatmap sobreposto com as bounding boxes dos objetos detectados."
)
def gerar_heatmap_com_bounding_boxes(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG", openapi_extra={"example": "exemplo.jpg"}),
    objeto_alvo: str = Form(
        OBJETO_ALVO_DEFAULT,
        description="Classe do objeto para gerar heatmap + boxes",
        examples={
            "person": {"value": "person"},
            "animal": {"value": "animal"},
        }
    )
):
    img = Image.open(BytesIO(image.file.read()))
    json_data = UseCases.load_json(JSON_PATH)
    result_image = UseCases.draw_heatmap_and_bounding_boxes_from_image(json_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
