"""Result enums for username checks."""
from enum import Enum, auto


class CheckResult(Enum):
    """Possible outcomes of a username check."""
    FOUND = auto()
    NOT_FOUND = auto()
    RATE_LIMITED = auto()
    TIMEOUT = auto()
    NETWORK_ERROR = auto()
    UNKNOWN_ERROR = auto()
    
    def is_success(self) -> bool:
        """Check if this is a definitive result."""
        return self in (CheckResult.FOUND, CheckResult.NOT_FOUND)
    
    def is_error(self) -> bool:
        """Check if this result indicates an error."""
        return self in (
            CheckResult.RATE_LIMITED,
            CheckResult.TIMEOUT,
            CheckResult.NETWORK_ERROR,
            CheckResult.UNKNOWN_ERROR,
        )
