#########################
# CS415 Project 3
# By Seth Nuzum and Adam Erskine
#########################

# All imports here:
from PIL import Image
import numpy as np
import heapq


# Here we are seeing if a pixel is valid (wall or path)
def is_valid_pixel(pixel, threshold=(100, 100, 100)):
    return any(channel > threshold[i] for i, channel in enumerate(pixel))


# Red line movement, no diagonals:
def get_neighbors_4dir(x, y, width, height):  # For BFS
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]  # 4-directional
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))
    return neighbors


def get_neighbors_8dir(x, y, width, height):
    directions = [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))
    return neighbors


def heuristic(curr, goal):
    return (
        (curr[0] - goal[0]) ** 2 + (curr[1] - goal[1]) ** 2
    ) ** 0.5  # Euclidean distance


# First algo done:
def bfs(image, start, goal):
    width, height = image.size
    queue = [start]
    visited = set()
    visited.add(start)
    prev = {start: None}
    distances = {start: 0}
    path_found = False

    while queue:
        x, y = queue.pop(0)
        if (x, y) == goal:
            path_found = True
            break

        for nx, ny in get_neighbors_4dir(x, y, width, height):
            if (nx, ny) not in visited and is_valid_pixel(image.getpixel((nx, ny))):
                queue.append((nx, ny))
                visited.add((nx, ny))
                prev[(nx, ny)] = (x, y)
                distances[(nx, ny)] = distances[(x, y)] + 1

    path = []
    if path_found:
        curr = goal
        while curr:
            path.append(curr)
            curr = prev[curr]
        path.reverse()
    return path, visited


# second algo done:
def best_first_search(image, start, goal):
    width, height = image.size
    queue = [(0 + heuristic(start, goal), start)]
    visited = set()
    visited.add(start)
    prev = {start: None}
    distances = {start: 0}
    path_found = False

    while queue:
        _, (x, y) = heapq.heappop(queue)
        if (x, y) == goal:
            path_found = True
            break

        for nx, ny in get_neighbors_8dir(x, y, width, height):
            if (nx, ny) not in visited and is_valid_pixel(image.getpixel((nx, ny))):
                heapq.heappush(
                    queue, (distances[(x, y)] + 1 + heuristic((nx, ny), goal), (nx, ny))
                )
                visited.add((nx, ny))
                prev[(nx, ny)] = (x, y)
                distances[(nx, ny)] = distances[(x, y)] + 1

    path = []
    if path_found:
        curr = goal
        while curr:
            path.append(curr)
            curr = prev[curr]
        path.reverse()
    return path, visited


def create_output_image(input_image, path, visited):
    output_image = input_image.copy()
    for x, y in visited:
        output_image.putpixel((x, y), (0, 255, 0))  # green
    for x, y in path:
        output_image.putpixel((x, y), (255, 0, 0))  # red
    return output_image


# Main function to fit spec:
def main():
    # Request input BMP file name
    input_file = input("Enter the name of the input BMP file: ")

    # Request starting vertex coordinates
    start_coords = input(
        "Enter the starting vertex coordinates (x, y) separated by a comma: "
    )
    start_x, start_y = map(int, start_coords.split(","))

    # Request goal vertex coordinates
    goal_coords = input(
        "Enter the goal vertex coordinates (x, y) separated by a comma: "
    )
    goal_x, goal_y = map(int, goal_coords.split(","))

    # Open the image
    image = Image.open(input_file)

    # Run BFS and Best-First Search
    bfs_path, bfs_visited = bfs(image, (start_x, start_y), (goal_x, goal_y))
    a_star_path, a_star_visited = best_first_search(
        image, (start_x, start_y), (goal_x, goal_y)
    )

    # Output the lengths of the shortest paths
    print("Length of the shortest path (BFS):", len(bfs_path))
    print("Length of the shortest path (Best-First Search):", len(a_star_path))

    # Request names for the output files
    bfs_output_file = input("Enter the name of the BFS output file (BMP file): ")
    a_star_output_file = input(
        "Enter the name of the Best-First Search output file (BMP file): "
    )

    # Create output images and save them
    bfs_output_image = create_output_image(image, bfs_path, bfs_visited)
    a_star_output_image = create_output_image(image, a_star_path, a_star_visited)

    bfs_output_image.save(bfs_output_file)
    a_star_output_image.save(a_star_output_file)


if __name__ == "__main__":
    main()
