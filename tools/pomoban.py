import curses
import sqlite3
import time
import threading
import sys
from datetime import date

# --- DATABASE ---
DB_NAME = "pomoban.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY, task TEXT, status TEXT, 
                      pomos INTEGER DEFAULT 0, created_at DATE)''')

def get_tasks_by_status(status):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT id, task, status, pomos FROM tasks WHERE status = ?", (status,)).fetchall()

def move_task(task_id, current_status, direction):
    flow = ["TODO", "DOING", "DONE"]
    curr_idx = flow.index(current_status)
    new_idx = curr_idx + direction
    if 0 <= new_idx < len(flow):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (flow[new_idx], task_id))

def add_new_task(text):
    if text.strip():
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO tasks (task, status, created_at) VALUES (?, 'TODO', ?)", (text, date.today()))

def add_pomodoro(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET pomos = pomos + 1 WHERE id = ?", (task_id,))

# --- BIG CLOCK DATA ---
NUMS = {
    '0': ["███", "█ █", "█ █", "█ █", "███"], '1': ["  █", "  █", "  █", "  █", "  █"],
    '2': ["███", "  █", "███", "█  ", "███"], '3': ["███", "  █", "███", "  █", "███"],
    '4': ["█ █", "█ █", "███", "  █", "  █"], '5': ["███", "█  ", "███", "  █", "███"],
    '6': ["███", "█  ", "███", "█ █", "███"], '7': ["███", "  █", "  █", "  █", "  █"],
    '8': ["███", "█ █", "███", "█ █", "███"], '9': ["███", "█ █", "███", "  █", "███"],
    ':': ["   ", " █ ", "   ", " █ ", "   "]
}

# --- GLOBAL STATE ---
timer_running = False
time_left = 1500
active_task_id = None

def timer_loop():
    global time_left, timer_running, active_task_id
    while True:
        if timer_running and time_left > 0:
            time.sleep(1)
            time_left -= 1
            if time_left == 0:
                timer_running = False
                if active_task_id: add_pomodoro(active_task_id)
                sys.stdout.write('\a')
                sys.stdout.flush()
        else:
            time.sleep(0.2)

def draw_big_clock(stdscr, y_off, x_off):
    mins, secs = divmod(time_left, 60)
    time_str = f"{mins:02d}:{secs:02d}"
    h, w = stdscr.getmaxyx()
    
    # Check if clock fits on screen
    if y_off + 5 >= h or x_off + 30 >= w:
        stdscr.addstr(1, (w-20)//2, f"TIMER: {time_str}", curses.color_pair(2) | curses.A_BOLD)
        return

    for line_i in range(5):
        display_line = ""
        for char in time_str:
            # FIXED: NUMS[char][line_i] is the string we need to concatenate
            display_line += NUMS[char][line_i] + "  "
        stdscr.addstr(y_off + line_i, x_off, display_line, curses.color_pair(2))

def main(stdscr):
    global timer_running, time_left, active_task_id
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1) # Selection
    curses.init_pair(2, curses.COLOR_RED, -1)  # Timer
    curses.curs_set(0)
    stdscr.nodelay(True)

    col_idx = 0
    row_idx = 0
    statuses = ["TODO", "DOING", "DONE"]

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()

        # Data Management
        columns = [get_tasks_by_status(s) for s in statuses]
        current_list = columns[col_idx]
        if row_idx >= len(current_list) and len(current_list) > 0:
            row_idx = len(current_list) - 1

        # Header
        stdscr.addstr(0, 2, "POMOBAN v2.1", curses.A_BOLD)
        controls = "[A]Add [ENT]Next [BCK]Prev [S]Start/Stop [Q]Quit"
        if w > len(controls) + 20:
            stdscr.addstr(0, w - len(controls) - 2, controls)

        # Big Clock
        clock_width = 32 # Approx width of the 5-digit ASCII clock
        clock_x = max(0, (w - clock_width) // 2)
        draw_big_clock(stdscr, 2, clock_x)

        # Columns
        col_w = w // 3
        for i, status in enumerate(statuses):
            title_attr = curses.A_BOLD | curses.A_UNDERLINE if i == col_idx else curses.A_DIM
            stdscr.addstr(8, i * col_w + 2, f" {status} ", title_attr)
            
            for j, task in enumerate(columns[i]):
                label = f"{task[1]} ({task[3]}🍅)"
                # Clean label for small terminals
                display_text = label[:col_w-6]
                
                if i == col_idx and j == row_idx:
                    stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                    stdscr.addstr(10 + j, i * col_w + 2, f"> {display_text}")
                    stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.addstr(10 + j, i * col_w + 2, f"  {display_text}")

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'): break
        elif key == curses.KEY_RIGHT: 
            col_idx = (col_idx + 1) % 3
            row_idx = 0
        elif key == curses.KEY_LEFT: 
            col_idx = (col_idx - 1) % 3
            row_idx = 0
        elif key == curses.KEY_UP and row_idx > 0:
            row_idx -= 1
        elif key == curses.KEY_DOWN and row_idx < len(current_list) - 1:
            row_idx += 1
        elif key == ord('a'):
            stdscr.nodelay(False)
            curses.echo()
            stdscr.addstr(h-1, 2, "Task Description: ")
            new_t = stdscr.getstr().decode('utf-8')
            add_new_task(new_t)
            curses.noecho()
            stdscr.nodelay(True)
        elif key in [10, 13]: # Enter
            if current_list:
                move_task(current_list[row_idx][0], statuses[col_idx], 1)
        elif key in [curses.KEY_BACKSPACE, 127, 8]: # Backspace
            if current_list:
                move_task(current_list[row_idx][0], statuses[col_idx], -1)
        elif key == ord('s'):
            if col_idx == 1 and current_list:
                active_task_id = current_list[row_idx][0]
                timer_running = not timer_running
                if not timer_running: time_left = 1500
            else:
                stdscr.addstr(h-1, 2, "!! Move task to DOING column first !!", curses.color_pair(2))
                stdscr.refresh()
                time.sleep(0.8)

        time.sleep(0.05)

if __name__ == "__main__":
    init_db()
    if "--stats" in sys.argv:
        with sqlite3.connect(DB_NAME) as conn:
            res = conn.execute("SELECT task, pomos FROM tasks WHERE created_at=?", (date.today(),)).fetchall()
            print(f"\n--- PomoBan Stats for {date.today()} ---")
            if not res: print("No work recorded today.")
            for r in res: print(f"🍅 {r[0]}: {r[1]} cycles")
    else:
        threading.Thread(target=timer_loop, daemon=True).start()
        curses.wrapper(main)