from PIL import Image, ImageDraw, ImageColor
import pandas as pd
from scipy.spatial import ConvexHull
import numpy as np


def create_image(size, background, letters, line, dataset_path, output_dataset_path):
    # Створюємо зображення
    image = Image.new("RGB", size, ImageColor.getcolor(background, "RGB"))
    draw = ImageDraw.Draw(image)

    # Зчитуємо датасет
    pixels = pd.read_csv(dataset_path, sep=" ", header=None).values
    points = pixels[:, :2]

    # Створюємо оболонку
    hull = ConvexHull(points)

    # Створюємо датасет з координатами точок з оболонки
    convex_hull_dataset = pd.DataFrame(points[hull.vertices], columns=['x', 'y'])
    convex_hull_dataset.to_csv(output_dataset_path, index=False, header=None, sep=' ')

    pixel_color = ImageColor.getcolor(letters, "RGB")

    # Малюємо точки
    for point in points:
        draw.point(tuple(point), fill=pixel_color)

    pixel_color = ImageColor.getcolor(line, "RGB")

    # Малюємо оболонку
    for simplex in hull.simplices:
        for i in range(len(simplex)):
            start_point = tuple(points[simplex[i]])
            end_point = tuple(points[simplex[(i + 1) % len(simplex)]])
            draw.line([start_point, end_point], fill=pixel_color)

    return image


image_size = (540, 960)

dataset_path = 'DS4.txt'
obolonka = 'obolonka.png'
obolonka_dataset = 'obolonka_dataset.txt'

result_image = create_image(image_size, "#FFFF55", "#00FF00", "#0000FF", dataset_path, obolonka_dataset)

result_image.save(obolonka)
