from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass

class ConsoleNotification(NotificationStrategy):
    def notify(self, message: str) -> None:
        print(f"[Notification] {message}")
