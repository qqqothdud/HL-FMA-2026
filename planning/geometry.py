import math


def calculate_distance(current, target):

    dx = target["x"] - current["x"]
    dy = target["y"] - current["y"]

    distance = math.sqrt(dx**2 + dy**2)

    return distance