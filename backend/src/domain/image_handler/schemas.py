# domain/image_handler/schemas.py

from pydantic import BaseModel, Field
from typing import Dict, Any


class GenericElasticsearchJSONSchema(BaseModel):
    json_data: Dict[str, Any] = Field(
        ...,
        description="JSON completo da resposta do Elasticsearch contendo os campos 'hits.hits[*].fields.deepstream-msg'.",
        example={
            "hits": {
                "hits": [
                    {
                        "_index": "no_leak_demo",
                        "_id": "doc_001",
                        "_score": 1.0,
                        "fields": {
                            "deepstream-msg": [
                                "591|217.332|319.33|467.849|480|person|AREA1",
                                "0|148.393|86.8989|216.347|205.22|chair|AREA1"
                            ]
                        }
                    }
                ]
            }
        }
    )
