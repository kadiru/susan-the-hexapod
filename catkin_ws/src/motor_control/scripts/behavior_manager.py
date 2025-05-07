import threading
import time

class BehaviorManager:
    def __init__(self):
        self.behaviors = {}
        self.current_thread = None
        self.stop_event = threading.Event()
        self.current_behavior_name = None

    def register(self, name, func):
        """Register a new behavior by name."""
        self.behaviors[name] = func

    def start(self, name, *args, **kwargs):
        """Start a named behavior in a new thread."""
        if name not in self.behaviors:
            print(f"[ERROR] Behavior '{name}' not found.")
            return

        self.stop()  # Ensure clean stop of any current behavior
        self.stop_event.clear()
        behavior_func = self.behaviors[name]

        def run():
            print(f"[INFO] Starting behavior: {name}")
            try:
                behavior_func(*args, stop_event=self.stop_event, **kwargs)
            finally:
                print(f"[INFO] Behavior '{name}' ended.")
                self.current_behavior_name = None

        self.current_behavior_name = name
        self.current_thread = threading.Thread(target=run)
        self.current_thread.start()

    def stop(self):
        """Stop the current behavior if running."""
        if self.current_thread and self.current_thread.is_alive():
            print(f"[INFO] Stopping behavior: {self.current_behavior_name}")
            self.stop_event.set()
            self.current_thread.join()

    def is_running(self):
        return self.current_thread and self.current_thread.is_alive()

    def current_behavior(self):
        return self.current_behavior_name

    def list_behaviors(self):
        return list(self.behaviors.keys())
