import json
import numpy as np
import cv2
from PIL import Image
from datetime import datetime
from typing import Tuple, List
from io import BytesIO


class UseCases:

    @staticmethod
    def load_json(path: str) -> dict:
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def create_output_name(prefix: str, objeto_alvo: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{objeto_alvo}_{timestamp}.png"

    @staticmethod
    def get_centroids(json_data: dict, objeto_alvo: str) -> List[Tuple[int, int]]:
        centroids = []
        for hit in json_data["hits"]["hits"]:
            msgs = hit["fields"].get("deepstream-msg", [])
            for msg in msgs:
                parts = msg.split("|")
                if len(parts) >= 7:
                    _, xmin, ymin, xmax, ymax, obj, _ = parts
                    if obj == objeto_alvo:
                        try:
                            cx = (float(xmin) + float(xmax)) / 2
                            cy = (float(ymin) + float(ymax)) / 2
                            centroids.append((int(cx), int(cy)))
                        except ValueError:
                            continue
        return centroids

    @staticmethod
    def draw_bounding_boxes_from_image(json_data: dict, image: Image.Image, objeto_alvo: str = "person") -> Image.Image:
        img_array = np.array(image.convert("RGB"))

        for hit in json_data["hits"]["hits"]:
            msgs = hit["fields"].get("deepstream-msg", [])
            for msg in msgs:
                parts = msg.split("|")
                if len(parts) >= 7:
                    track_id, xmin, ymin, xmax, ymax, obj, _ = parts
                    if obj != objeto_alvo:
                        continue
                    try:
                        xmin = int(float(xmin))
                        ymin = int(float(ymin))
                        xmax = int(float(xmax))
                        ymax = int(float(ymax))
                        cv2.rectangle(img_array, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        label = f"{obj}#{track_id}"
                        cv2.putText(img_array, label, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    except ValueError:
                        continue

        return Image.fromarray(img_array)

    @staticmethod
    def generate_heatmap_from_image(json_data: dict, image: Image.Image, objeto_alvo: str = "person") -> Image.Image:
        img_array = np.array(image.convert("RGB"))
        height, width = img_array.shape[:2]
        heatmap = np.zeros((height, width), dtype=np.float32)

        centroids = UseCases.get_centroids(json_data, objeto_alvo)
        for x, y in centroids:
            if 0 <= x < width and 0 <= y < height:
                heatmap[y, x] += 1

        heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=15)
        heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_color = cv2.applyColorMap(heatmap_norm.astype(np.uint8), cv2.COLORMAP_JET)
        blended = cv2.addWeighted(img_array, 0.6, heatmap_color, 0.4, 0)

        return Image.fromarray(blended)

    @staticmethod
    def draw_heatmap_and_bounding_boxes_from_image(json_data: dict, image: Image.Image, objeto_alvo: str = "person") -> Image.Image:
        img_array = np.array(image.convert("RGB"))
        height, width = img_array.shape[:2]
        heatmap = np.zeros((height, width), dtype=np.float32)

        for hit in json_data["hits"]["hits"]:
            msgs = hit["fields"].get("deepstream-msg", [])
            for msg in msgs:
                parts = msg.split("|")
                if len(parts) >= 7:
                    track_id, xmin, ymin, xmax, ymax, obj, _ = parts
                    if obj != objeto_alvo:
                        continue
                    try:
                        xmin = float(xmin)
                        ymin = float(ymin)
                        xmax = float(xmax)
                        ymax = float(ymax)
                        cx = int((xmin + xmax) / 2)
                        cy = int((ymin + ymax) / 2)
                        if 0 <= cx < width and 0 <= cy < height:
                            heatmap[cy, cx] += 1
                        cv2.rectangle(img_array, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                        label = f"{obj}#{track_id}"
                        cv2.putText(img_array, label, (int(xmin), int(ymin) - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    except ValueError:
                        continue

        heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=15)
        heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_color = cv2.applyColorMap(heatmap_norm.astype(np.uint8), cv2.COLORMAP_JET)
        result = cv2.addWeighted(img_array, 0.6, heatmap_color, 0.4, 0)

        return Image.fromarray(result)
