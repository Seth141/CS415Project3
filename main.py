#########################
# CS415 Project 3
# By Seth Nuzum and Adam E
#########################


from PIL import Image, ImageDraw
from collections import deque
import heapq


# This one checks if a pixel is valid:
def is_valid_pixel(pixel):
    r, g, b = pixel
    return r > 100 or g > 100 or b > 100


from PIL import Image, ImageDraw
from collections import deque


def bfs(image, start, goal):
    width, height = image.size
    start = (start[1], start[0])
    goal = (goal[1], goal[0])

    def get_neighbors(pos):
        x, y = pos
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [
            (nx, ny) for nx, ny in neighbors if 0 <= nx < width and 0 <= ny < height
        ]

    def is_valid_pixel(pixel):
        r, g, b = pixel
        return r > 100 or g > 100 or b > 100

    queue = deque([start])
    visited = {start}
    prev = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in visited and is_valid_pixel(image.getpixel(neighbor)):
                queue.append(neighbor)
                visited.add(neighbor)
                prev[neighbor] = current

    path_length = 0
    path_pixels = []

    # Backtrack from goal to start to find path
    at = goal
    while at is not None:
        path_pixels.append(at)
        at = prev[at]
        path_length += 1

    # Create a copy of the image to draw the path
    output_image = image.copy()
    draw = ImageDraw.Draw(output_image)

    # Draw the path in red and visited nodes in green
    for pixel in path_pixels:
        draw.point(pixel, (255, 0, 0))  # Red for path
    for pixel in visited - set(path_pixels):
        draw.point(pixel, (0, 255, 0))  # Green for visited nodes

    return path_length - 1, output_image


def best_first_search(image, start, goal):
    width, height = image.size
    start = (start[1], start[0])  # Convert (row, col) to (x, y)
    goal = (goal[1], goal[0])  # Convert (row, col) to (x, y)

    def get_neighbors(pos):
        x, y = pos
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [
            (nx, ny) for nx, ny in neighbors if 0 <= nx < width and 0 <= ny < height
        ]

    def heuristic(pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    priority_queue = [(0 + heuristic(start, goal), 0, start)]
    visited = {start}
    prev = {start: None}
    distances = {start: 0}

    while priority_queue:
        _, dist, current = heapq.heappop(priority_queue)
        if current == goal:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in visited and is_valid_pixel(image.getpixel(neighbor)):
                visited.add(neighbor)
                prev[neighbor] = current
                distances[neighbor] = dist + 1
                heapq.heappush(
                    priority_queue,
                    (
                        distances[neighbor] + heuristic(neighbor, goal),
                        distances[neighbor],
                        neighbor,
                    ),
                )

    path_length = 0
    path_pixels = []

    # Backtrack from goal to start to find path
    at = goal
    while at is not None:
        path_pixels.append(at)
        at = prev[at]
        path_length += 1

    # Create a copy of the image to draw the path
    output_image = image.copy()
    draw = ImageDraw.Draw(output_image)

    # Draw the path in red and visited nodes in green
    for pixel in path_pixels:
        draw.point(pixel, (255, 0, 0))  # Red for path
    for pixel in visited - set(path_pixels):
        draw.point(pixel, (0, 255, 0))  # Green for visited nodes

    return path_length - 1, output_image


# Main Function
def main():
    input_image_name = input("Enter the name of the input BMP file: ")
    start_row = int(input("Enter the start row: "))
    start_col = int(input("Enter the start column: "))
    goal_row = int(input("Enter the goal row: "))
    goal_col = int(input("Enter the goal column: "))
    output_image_name_bfs = input("Enter the name of the output BMP file for BFS: ")
    output_image_name_bestfs = input(
        "Enter the name of the output BMP file for BestFS: "
    )

    # Load the image
    image = Image.open(input_image_name)

    # Run BFS
    bfs_path_length, bfs_image = bfs(
        image, (start_row, start_col), (goal_row, goal_col)
    )
    bfs_image.save(output_image_name_bfs)
    print(f"BFS Path Length: {bfs_path_length}")

    # Run BestFS
    bestfs_path_length, bestfs_image = best_first_search(
        image, (start_row, start_col), (goal_row, goal_col)
    )
    bestfs_image.save(output_image_name_bestfs)
    print(f"BestFS Path Length: {bestfs_path_length}")


if __name__ == "__main__":
    main()
