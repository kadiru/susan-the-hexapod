import curses
from threading import Event
from behavior_manager import BehaviorManager  # assuming you save the class in a module
from behaviors import ALL_BEHAVIORS, retractAll

def interactive_menu(stdscr, manager: BehaviorManager):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(100)

    behaviors = manager.list_behaviors()
    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "🦿 Six-Legged Robot Behavior Menu", curses.A_BOLD)
        stdscr.addstr(1, 0, "↑↓ to navigate | Enter to start | 's' to stop | 'r' retract | 'q' quit", curses.A_DIM)

        # Highlight selection
        for i, name in enumerate(behaviors):
            if i == current_selection:
                stdscr.addstr(i + 3, 2, f"> {name}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 3, 4, name)

        # Show currently running
        running = manager.current_behavior()
        if running:
            stdscr.addstr(len(behaviors) + 5, 0, f"✅ Running: {running}", curses.A_BOLD)
        else:
            stdscr.addstr(len(behaviors) + 5, 0, "🛑 No active behavior", curses.A_DIM)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(behaviors) - 1:
            current_selection += 1
        elif key in [10, 13]:  # Enter key
            selected = behaviors[current_selection]
            manager.start(selected)
        elif key == ord('s'):
            manager.stop()
        elif key == ord('r'):
            manager.stop()
            dummy_event = Event()
            retractAll(duration=1000, speed=255, fade_in=0, fade_out=0, stop_event=dummy_event)
        elif key == ord('q'):
            manager.stop()
            break

def run_curses_ui():
    manager = BehaviorManager()
    
    # Register your behaviors here
    for name, func in ALL_BEHAVIORS.items():
        manager.register(name, func)

    curses.wrapper(interactive_menu, manager)

if __name__ == "__main__":
    run_curses_ui()
