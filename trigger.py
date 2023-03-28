from enum import Enum

class Trigger(Enum):
    PENDING = "pending"
    TRIGGERED = "triggered"
    RESOLVED = "resolved"