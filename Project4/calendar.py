#!/usr/bin/env python3
"""
Event Calendar with conflict detection and scheduling features
Implements greedy algorithms and dynamic programming for optimization
"""

import json
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict

from models import Event
from interval_tree import IntervalTree

class EventCalendar:
    """Main calendar system with conflict detection and scheduling features."""
    
    def __init__(self):
        self.interval_tree = IntervalTree()
        self.events_by_id: Dict[int, Event] = {}
        self.next_event_id = 1
    
    def add_event(self, start_time: datetime, end_time: datetime, label: str) -> Tuple[bool, str, Optional[Event]]:
        """Add an event to the calendar. Returns (success, message, event)."""
        try:
            event = Event(start_time, end_time, label, self.next_event_id)
            self.next_event_id += 1
            
            # Check for conflicts
            conflicts = self.interval_tree.find_overlapping(event)
            if conflicts:
                conflict_names = [c.label for c in conflicts]
                return False, f"Event conflicts with: {', '.join(conflict_names)}", event
            
            # Add event
            self.interval_tree.insert(event)
            self.events_by_id[event.event_id] = event
            
            return True, f"Event '{label}' added successfully", event
            
        except ValueError as e:
            return False, str(e), None
    
    def delete_event(self, event_id: int) -> Tuple[bool, str]:
        """Delete an event by ID."""
        if event_id not in self.events_by_id:
            return False, "Event not found"
        
        event = self.events_by_id[event_id]
        self.interval_tree.delete(event_id)
        del self.events_by_id[event_id]
        
        return True, f"Event '{event.label}' deleted successfully"
    
    def get_events_at_time(self, query_time: datetime) -> List[Event]:
        """Get all events happening at a specific time."""
        # Create a 1-minute interval for the query
        query_event = Event(query_time, query_time + timedelta(minutes=1), "query")
        return self.interval_tree.find_overlapping(query_event)
    
    def find_free_slots(self, duration_minutes: int, start_time: datetime, end_time: datetime) -> List[Tuple[datetime, datetime]]:
        """Find free slots of specified duration within a time range using greedy approach."""
        events = self.get_events_in_range(start_time, end_time)
        events.sort(key=lambda e: e.start_time)
        
        free_slots = []
        current_time = start_time
        
        for event in events:
            # Check if there's a gap before this event
            if current_time < event.start_time:
                gap_duration = int((event.start_time - current_time).total_seconds() / 60)
                if gap_duration >= duration_minutes:
                    slot_end = current_time + timedelta(minutes=duration_minutes)
                    if slot_end <= event.start_time:
                        free_slots.append((current_time, slot_end))
            
            # Update current time to after this event
            current_time = max(current_time, event.end_time)
        
        # Check for a slot after the last event
        if current_time < end_time:
            gap_duration = int((end_time - current_time).total_seconds() / 60)
            if gap_duration >= duration_minutes:
                slot_end = current_time + timedelta(minutes=duration_minutes)
                if slot_end <= end_time:
                    free_slots.append((current_time, slot_end))
        
        return free_slots
    
    def get_next_free_slot(self, duration_minutes: int, after_time: Optional[datetime] = None) -> Optional[Tuple[datetime, datetime]]:
        """Get the next available free slot of specified duration."""
        if after_time is None:
            after_time = datetime.now().replace(second=0, microsecond=0)
        
        # Look for slots in the next 7 days
        end_search = after_time + timedelta(days=7)
        free_slots = self.find_free_slots(duration_minutes, after_time, end_search)
        
        return free_slots[0] if free_slots else None
    
    def get_events_in_range(self, start_time: datetime, end_time: datetime) -> List[Event]:
        """Get all events within a time range."""
        query_event = Event(start_time, end_time, "range_query")
        return self.interval_tree.find_overlapping(query_event)
    
    def get_all_conflicts(self) -> List[Tuple[Event, List[Event]]]:
        """Get all conflicting events using dynamic programming approach."""
        all_events = self.interval_tree.get_all_events()
        conflicts = []
        
        # Use memoization for conflict detection
        conflict_memo: Dict[int, List[Event]] = {}
        
        for event in all_events:
            if event.event_id not in conflict_memo:
                overlapping = self.interval_tree.find_overlapping(event)
                # Remove the event itself from overlapping
                overlapping = [e for e in overlapping if e.event_id != event.event_id]
                
                if overlapping:
                    conflicts.append((event, overlapping))
                    # Memoize results
                    conflict_memo[event.event_id] = overlapping
        
        return conflicts
    
    def get_event_density(self, start_time: datetime, end_time: datetime, slot_minutes: int = 60) -> Dict[datetime, int]:
        """Calculate event density (number of events per time slot) for visualization."""
        density = {}
        current_slot = start_time
        
        while current_slot < end_time:
            slot_end = current_slot + timedelta(minutes=slot_minutes)
            events_in_slot = self.get_events_in_range(current_slot, slot_end)
            density[current_slot] = len(events_in_slot)
            current_slot = slot_end
        
        return density
    
    def optimize_schedule(self, events_to_schedule: List[Tuple[int, str]]) -> List[Tuple[datetime, datetime, str]]:
        """
        Optimize scheduling of events with durations using dynamic programming.
        events_to_schedule: List of (duration_minutes, label) tuples
        Returns: List of (start_time, end_time, label) tuples
        """
        if not events_to_schedule:
            return []
        
        # Sort events by duration (shortest first) for greedy optimization
        events_to_schedule.sort(key=lambda x: x[0])
        
        scheduled = []
        start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)  # Start at 9 AM
        end_time = start_time.replace(hour=17)  # End at 5 PM
        
        for duration, label in events_to_schedule:
            free_slot = self.find_free_slots(duration, start_time, end_time)
            if free_slot:
                slot_start, slot_end = free_slot[0]
                scheduled.append((slot_start, slot_start + timedelta(minutes=duration), label))
                # Temporarily add to avoid double booking
                temp_event = Event(slot_start, slot_start + timedelta(minutes=duration), label)
                self.interval_tree.insert(temp_event)
        
        return scheduled
    
    def export_events(self, filename: str) -> None:
        """Export events to JSON file."""
        events_data = []
        for event in self.interval_tree.get_all_events():
            events_data.append({
                'id': event.event_id,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat(),
                'label': event.label
            })
        
        with open(filename, 'w') as f:
            json.dump(events_data, f, indent=2)
    
    def import_events(self, filename: str) -> Tuple[bool, str]:
        """Import events from JSON file."""
        try:
            with open(filename, 'r') as f:
                events_data = json.load(f)
            
            imported_count = 0
            for event_data in events_data:
                start_time = datetime.fromisoformat(event_data['start_time'])
                end_time = datetime.fromisoformat(event_data['end_time'])
                label = event_data['label']
                success, _, _ = self.add_event(start_time, end_time, label)
                if success:
                    imported_count += 1
            
            return True, f"Imported {imported_count}/{len(events_data)} events successfully"
        except Exception as e:
            return False, f"Import failed: {str(e)}"