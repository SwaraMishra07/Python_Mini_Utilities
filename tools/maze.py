import argparse
import sys
import random
import json
import heapq
from typing import List, Tuple, Optional

def generate_maze(width: int, height: int) -> List[List[int]]:
    """Generate perfect maze (1=wall, 0=path)."""
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1
    
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve(cx: int, cy: int):
        maze[cy][cx] = 0
        dirs = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(dirs)
        
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny][nx] == 1:
                maze[cy + dy//2][cx + dx//2] = 0
                carve(nx, ny)
    
    carve(1, 1)
    
    # Ensure start and exit are open
    maze[1][1] = 0  # Start
    maze[height-2][width-2] = 0  # Exit
    
    return maze

def render_maze(maze: List[List[int]], solution: Optional[List[Tuple[int,int]]] = None) -> List[str]:
    """Clean Unicode rendering with PERFECT solution path."""
    height, width = len(maze), len(maze[0])
    path_set = set(solution) if solution else set()
    
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            if maze[y][x] == 1:
                line += "███"  # Full block wall
            elif (x, y) == (1, 1):
                line += " S "  # Start
            elif (x, y) == (len(maze[0])-2, len(maze)-2):
                line += " E "  # Exit
            elif (x, y) in path_set:
                line += "▓▓▓"  # DISTINCT solution path (not █)
            else:
                line += "   "  # Empty path
        lines.append(line)
    return lines

def solve_maze(maze: List[List[int]]) -> List[Tuple[int,int]]:
    """A* pathfinding with correct coordinates."""
    height, width = len(maze), len(maze[0])
    start = (1, 1)
    goal = (width-2, height-2)
    
    def heuristic(pos: Tuple[int,int]) -> int:
        return (abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))
    
    open_set = [(0, 0, start)]  # (f_score, g_score, pos)
    came_from = {}
    g_score = {start: 0}
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            
            if (0 <= nx < width and 0 <= ny < height and 
                maze[ny][nx] == 0 and (nx, ny) not in g_score):
                
                g_score[(nx, ny)] = current_g + 1
                f_score = g_score[(nx, ny)] + heuristic((nx, ny))
                came_from[(nx, ny)] = current
                heapq.heappush(open_set, (f_score, g_score[(nx, ny)], (nx, ny)))
    
    return []

def save_maze(maze: List[List[int]], filename: str):
    with open(filename, 'w') as f:
        json.dump(maze, f)

def load_maze(filename: str) -> List[List[int]]:
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Maze Generator & Solver")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    gen_parser = subparsers.add_parser("gen")
    gen_parser.add_argument("size", help="WIDTHxHEIGHT")
    gen_parser.add_argument("--solve", action="store_true")
    gen_parser.add_argument("--save")
    
    solve_parser = subparsers.add_parser("solve")
    solve_parser.add_argument("filename")
    
    args = parser.parse_args()
    
    try:
        if args.command == "gen":
            w, h = map(int, args.size.split('x'))
            maze = generate_maze(w, h)
            
            print("\n" + "═" * 50)
            print(f"MAZE: {w}x{h}")
            print("═" * 50)
            
            lines = render_maze(maze)
            for line in lines:
                print(line.rstrip())
            
            if args.solve:
                print("\n" + "═" * 50)
                print("SOLUTION:")
                print("═" * 50)
                solution = solve_maze(maze)
                if solution:
                    lines = render_maze(maze, solution)
                    for line in lines:
                        print(line.rstrip())
                    print(f"\n✅ Path: {len(solution)-1} steps ✓")
                else:
                    print("❌ No path found")
            
            if args.save:
                save_maze(maze, args.save)
                print(f"Saved: {args.save}")
                
        elif args.command == "solve":
            maze = load_maze(args.filename)
            print("\n" + "═" * 50)
            print("ORIGINAL MAZE:")
            print("═" * 50)
            for line in render_maze(maze):
                print(line.rstrip())
            
            solution = solve_maze(maze)
            if solution:
                print("\n" + "═" * 50)
                print("SOLUTION:")
                print("═" * 50)
                for line in render_maze(maze, solution):
                    print(line.rstrip())
                print(f"✅ Path: {len(solution)-1} steps")
            else:
                print("❌ No solution")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
