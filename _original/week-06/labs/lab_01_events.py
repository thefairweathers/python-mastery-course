"""
Lab 6.1: Event System — Build a publish/subscribe system (Observer pattern).
TODO: Implement EventBus with subscribe, emit, and @on decorator.
"""
from collections import defaultdict
from typing import Callable

class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable):
        # TODO
        pass

    def on(self, event_name: str):
        # TODO: Return a decorator that subscribes the function
        pass

    def emit(self, event_name: str, **data):
        # TODO: Call all handlers registered for this event
        pass

if __name__ == "__main__":
    bus = EventBus()
    @bus.on("user.created")
    def log_user(event):
        print(f"  New user: {event}")
    bus.emit("user.created", username="Alice")
