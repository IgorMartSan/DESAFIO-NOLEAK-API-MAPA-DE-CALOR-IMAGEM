import json, numpy as np, cv2
from PIL import Image
from datetime import datetime
import os

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def create_output_name(prefix, objeto_alvo):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{objeto_alvo}_{timestamp}.png"

def get_centroids(json_data, objeto_alvo):
    centroids = []
    for hit in json_data["hits"]["hits"]:
        msgs = hit["fields"].get("deepstream-msg", [])
        for msg in msgs:
            parts = msg.split("|")
            if len(parts) >= 7:
                _, xmin, ymin, xmax, ymax, obj, _ = parts
                if obj == objeto_alvo:
                    cx = (float(xmin) + float(xmax)) / 2
                    cy = (float(ymin) + float(ymax)) / 2
                    centroids.append((int(cx), int(cy)))
    return centroids

def draw_bounding_boxes(json_data, image_path, output_path, objeto_alvo="person"):
    image = np.array(Image.open(image_path).convert("RGB"))

    for hit in json_data["hits"]["hits"]:
        msgs = hit["fields"].get("deepstream-msg", [])
        for msg in msgs:
            parts = msg.split("|")
            if len(parts) >= 7:
                track_id, xmin, ymin, xmax, ymax, obj, region = parts
                if obj != objeto_alvo:
                    continue
                try:
                    xmin = int(float(xmin))
                    ymin = int(float(ymin))
                    xmax = int(float(xmax))
                    ymax = int(float(ymax))
                    color = (0, 255, 0)
                    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
                    label = f"{obj}#{track_id}"
                    cv2.putText(image, label, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, color, 1, cv2.LINE_AA)
                except ValueError:
                    continue
    cv2.imwrite(output_path, image)
    print(f"✅ Bounding boxes salvas: {output_path}")

def generate_heatmap(image_path, centroids, output_path="heatmap.png"):
    img = np.array(Image.open(image_path))
    heatmap = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    for (x, y) in centroids:
        if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
            heatmap[y, x] += 1

    heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=15)
    heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_color = cv2.applyColorMap(heatmap_norm.astype(np.uint8), cv2.COLORMAP_JET)
    blended = cv2.addWeighted(img, 0.6, heatmap_color, 0.4, 0)

    cv2.imwrite(output_path, blended)
    print(f"✅ Heatmap salvo: {output_path}")

def draw_heatmap_and_bounding_boxes(json_data, image_path, output_path, objeto_alvo="person"):
    img = np.array(Image.open(image_path).convert("RGB"))
    heatmap = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    for hit in json_data["hits"]["hits"]:
        msgs = hit["fields"].get("deepstream-msg", [])
        for msg in msgs:
            parts = msg.split("|")
            if len(parts) >= 7:
                track_id, xmin, ymin, xmax, ymax, obj, region = parts
                if obj != objeto_alvo:
                    continue
                try:
                    xmin = float(xmin)
                    ymin = float(ymin)
                    xmax = float(xmax)
                    ymax = float(ymax)
                    cx = int((xmin + xmax) / 2)
                    cy = int((ymin + ymax) / 2)
                    if 0 <= cx < img.shape[1] and 0 <= cy < img.shape[0]:
                        heatmap[cy, cx] += 1
                    cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                    label = f"{obj}#{track_id}"
                    cv2.putText(img, label, (int(xmin), int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 1, cv2.LINE_AA)
                except ValueError:
                    continue

    heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=15)
    heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_color = cv2.applyColorMap(heatmap_norm.astype(np.uint8), cv2.COLORMAP_JET)
    result = cv2.addWeighted(img, 0.6, heatmap_color, 0.4, 0)
    cv2.imwrite(output_path, result)
    print(f"✅ Heatmap + Bounding boxes salvo: {output_path}")

def main():
    objeto = "person"  # ou "chair", "tvmonitor", etc.
    json_path = "/workspaces/FIAP---Tech-Challenge-Fase-1---Vitivinicultura-Embrapa-API/backend/src/resp.json"
    image_path = "/workspaces/FIAP---Tech-Challenge-Fase-1---Vitivinicultura-Embrapa-API/backend/src/img.png"

    json_data = load_json(json_path)
    centroids = get_centroids(json_data, objeto)

    # Criar nomes de saída organizados
    bbox_name = create_output_name("bbox", objeto)
    heatmap_name = create_output_name("heatmap", objeto)
    fullmap_name = create_output_name("heatmap_bbox", objeto)

    draw_bounding_boxes(json_data, image_path, bbox_name, objeto_alvo=objeto)
    generate_heatmap(image_path, centroids, heatmap_name)
    draw_heatmap_and_bounding_boxes(json_data, image_path, fullmap_name, objeto_alvo=objeto)

if __name__ == "__main__":
    main()
