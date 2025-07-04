from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from domain.image_handler.use_cases import UseCases
from PIL import Image
from io import BytesIO
import json

router = APIRouter(prefix="/draw", tags=["Image handle (Sem Autenticação JWT)"])

OBJETO_ALVO_DEFAULT = "person"

json_example = (
    '{"hits": {"hits": ['
    '{"fields": {"deepstream-msg": ['
    '"591|217.332|319.33|467.849|480|person|AREA1", '
    '"0|148.393|86.8989|216.347|205.22|chair|AREA1"'
    ']}}]}}'
)


@router.post(
    "/bbox",
    summary="Desenhar bounding boxes",
    description="Recebe uma imagem e desenha bounding boxes com base no JSON do Elasticsearch."
)


def gerar_bounding_boxes(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG"),
    objeto_alvo: str = Form(OBJETO_ALVO_DEFAULT, description="Classe do objeto a ser destacada"),
    json_data: str = Form(json_example, description="JSON no formato do Elasticsearch")
):
    try:
        parsed_data = json.loads(json_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao interpretar JSON: {e}")

    img = Image.open(BytesIO(image.file.read()))
    result_image = UseCases.draw_bounding_boxes_from_image(parsed_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@router.post(
    "/heatmap",
    summary="Gerar heatmap da imagem",
    description="Recebe uma imagem e JSON do Elasticsearch para gerar o heatmap."
)
def gerar_heatmap(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG"),
    objeto_alvo: str = Form(OBJETO_ALVO_DEFAULT, description="Classe do objeto para o heatmap"),
    json_data: str = Form(json_example, description="JSON no formato do Elasticsearch", example=json_example)
):
    try:
        parsed_data = json.loads(json_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao interpretar JSON: {e}")

    img = Image.open(BytesIO(image.file.read()))
    result_image = UseCases.generate_heatmap_from_image(parsed_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post(
    "/heatmap_bbox",
    summary="Gerar heatmap com bounding boxes",
    description="Recebe imagem e JSON do Elasticsearch e retorna heatmap + boxes."
)
def gerar_heatmap_com_bounding_boxes(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG"),
    objeto_alvo: str = Form(OBJETO_ALVO_DEFAULT, description="Classe do objeto para visualizar"),
    json_data: str = Form(json_example, description="JSON no formato do Elasticsearch", example=json_example)
):
    try:
        parsed_data = json.loads(json_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao interpretar JSON: {e}")

    img = Image.open(BytesIO(image.file.read()))
    result_image = UseCases.draw_heatmap_and_bounding_boxes_from_image(parsed_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post(
    "/bbox_file",
    summary="Desenhar bounding boxes (com arquivo JSON)",
    description="Recebe uma imagem e um arquivo JSON com dados do Elasticsearch para desenhar bounding boxes."
)
def gerar_bounding_boxes_com_arquivo(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG"),
    json_file: UploadFile = File(..., description="Arquivo JSON com dados do Elasticsearch"),
    objeto_alvo: str = Form(OBJETO_ALVO_DEFAULT, description="Classe do objeto a ser destacada")
):
    try:
        parsed_data = json.load(json_file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler JSON do arquivo: {e}")

    img = Image.open(BytesIO(image.file.read()))
    result_image = UseCases.draw_bounding_boxes_from_image(parsed_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post(
    "/heatmap_file",
    summary="Gerar heatmap da imagem (com arquivo JSON)",
    description="Recebe uma imagem e um arquivo JSON com dados do Elasticsearch para gerar o heatmap."
)
def gerar_heatmap_com_arquivo(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG"),
    json_file: UploadFile = File(..., description="Arquivo JSON com dados do Elasticsearch"),
    objeto_alvo: str = Form(OBJETO_ALVO_DEFAULT, description="Classe do objeto para o heatmap")
):
    try:
        parsed_data = json.load(json_file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler JSON do arquivo: {e}")

    img = Image.open(BytesIO(image.file.read()))
    result_image = UseCases.generate_heatmap_from_image(parsed_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@router.post(
    "/heatmap_bbox_file",
    summary="Gerar heatmap com bounding boxes (com arquivo JSON)",
    description="Recebe imagem e um arquivo JSON com dados do Elasticsearch para gerar heatmap + boxes."
)
def gerar_heatmap_e_bounding_boxes_com_arquivo(
    image: UploadFile = File(..., description="Imagem no formato JPG ou PNG"),
    json_file: UploadFile = File(..., description="Arquivo JSON com dados do Elasticsearch"),
    objeto_alvo: str = Form(OBJETO_ALVO_DEFAULT, description="Classe do objeto para visualizar")
):
    try:
        parsed_data = json.load(json_file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler JSON do arquivo: {e}")

    img = Image.open(BytesIO(image.file.read()))
    result_image = UseCases.draw_heatmap_and_bounding_boxes_from_image(parsed_data, img, objeto_alvo)

    buf = BytesIO()
    result_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

