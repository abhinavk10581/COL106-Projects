#!/usr/bin/env python3
"""
Core data structures for Event Calendar Scheduler
"""

from datetime import datetime
from typing import Optional

class Event:
    """Represents a calendar event with start time, end time, and label."""
    
    def __init__(self, start_time: datetime, end_time: datetime, label: str, event_id: Optional[int] = None):
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        
        self.start_time = start_time
        self.end_time = end_time
        self.label = label
        self.event_id = event_id or id(self)
    
    def overlaps_with(self, other: 'Event') -> bool:
        """Check if this event overlaps with another event."""
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)
    
    def duration_minutes(self) -> int:
        """Get event duration in minutes."""
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    def __str__(self) -> str:
        return f"{self.label}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    def __repr__(self) -> str:
        return f"Event({self.start_time}, {self.end_time}, '{self.label}')"