"""Rate limiter with persistence."""
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any


RATE_LIMIT_FILE = Path.home() / ".navarro_rate_limits.json"


class RateLimiter:
    """Rate limiter with persistence."""
    
    def __init__(self):
        self.limits: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"count": 0, "reset_time": datetime.now()}
        )
        self.delays: Dict[str, float] = defaultdict(lambda: 0.5)  # Base delay per platform
        self.last_request: Dict[str, datetime] = defaultdict(lambda: datetime.now())
        self.load_limits()
    
    def load_limits(self):
        """Load saved rate limits from disk."""
        if RATE_LIMIT_FILE.exists():
            try:
                with open(RATE_LIMIT_FILE, 'r') as f:
                    saved_data = json.load(f)
                    for platform, limit_data in saved_data.get('limits', {}).items():
                        try:
                            reset_time = datetime.fromisoformat(
                                limit_data.get("reset_time", datetime.now().isoformat())
                            )
                        except (ValueError, TypeError):
                            reset_time = datetime.now()
                        
                        self.limits[platform] = {
                            "count": limit_data.get("count", 0),
                            "reset_time": reset_time
                        }
                    self.delays.update(saved_data.get('delays', {}))
            except Exception:
                pass
    
    def save_limits(self):
        """Save rate limits to disk."""
        try:
            limits_to_save = {}
            for platform, limit_data in self.limits.items():
                limits_to_save[platform] = {
                    "count": limit_data["count"],
                    "reset_time": (
                        limit_data["reset_time"].isoformat() 
                        if isinstance(limit_data["reset_time"], datetime) 
                        else limit_data["reset_time"]
                    )
                }
            
            with open(RATE_LIMIT_FILE, 'w') as f:
                json.dump({
                    'limits': limits_to_save,
                    'delays': dict(self.delays)
                }, f, indent=2)
        except Exception:
            pass
    
    def should_wait(self, platform: str) -> float:
        """Calculate wait time for platform."""
        now = datetime.now()
        
        reset_time = self.limits[platform]["reset_time"]
        if isinstance(reset_time, str):
            try:
                reset_time = datetime.fromisoformat(reset_time)
            except (ValueError, TypeError):
                reset_time = now
        
        if reset_time > now:
            return (reset_time - now).total_seconds()
        
        # Calculate adaptive delay
        time_since_last = (now - self.last_request[platform]).total_seconds()
        if time_since_last < self.delays[platform]:
            return self.delays[platform] - time_since_last
        
        return 0
    
    def record_request(self, platform: str, was_rate_limited: bool = False):
        """Record a request and update delays."""
        now = datetime.now()
        self.last_request[platform] = now
        
        if was_rate_limited:
            self.delays[platform] = min(self.delays[platform] * 2, 30)  # Max 30s delay
            self.limits[platform]["reset_time"] = now + timedelta(seconds=60)
        else:
            self.delays[platform] = max(self.delays[platform] * 0.9, 0.5)  # Min 0.5s delay
        
        self.save_limits()
