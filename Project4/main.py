
"""
Command-line interface for the Event Calendar Scheduler
Usage: python main.py
"""

from datetime import datetime
from calendar import EventCalendar

def main():
    """Command-line interface for the Event Calendar Scheduler."""
    calendar = EventCalendar()
    
    print("🗓️  Event Calendar Scheduler with Conflict Detection")
    print("=" * 50)
    print("Commands:")
    print("1. add - Add new event")
    print("2. delete - Delete event by ID")
    print("3. list - List all events")
    print("4. conflicts - Show all conflicts")
    print("5. free - Find free slots")
    print("6. at - Events at specific time")
    print("7. density - Show event density")
    print("8. export - Export events to file")
    print("9. import - Import events from file")
    print("10. quit - Exit program")
    print("=" * 50)
    
    while True:
        try:
            command = input("\nEnter command: ").lower().strip()
            
            if command in ("quit", "q"):
                print("Goodbye!")
                break
            
            elif command in ("add", "1"):
                handle_add_event(calendar)
            
            elif command in ("delete", "2"):
                handle_delete_event(calendar)
            
            elif command in ("list", "3"):
                handle_list_events(calendar)
            
            elif command in ("conflicts", "4"):
                handle_show_conflicts(calendar)
            
            elif command in ("free", "5"):
                handle_find_free_slots(calendar)
            
            elif command in ("at", "6"):
                handle_events_at_time(calendar)
            
            elif command in ("density", "7"):
                handle_event_density(calendar)
            
            elif command in ("export", "8"):
                handle_export_events(calendar)
            
            elif command in ("import", "9"):
                handle_import_events(calendar)
            
            else:
                print("❌ Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def handle_add_event(calendar):
    """Handle adding a new event."""
    label = input("Event label: ")
    start_str = input("Start time (YYYY-MM-DD HH:MM): ")
    end_str = input("End time (YYYY-MM-DD HH:MM): ")
    
    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        
        success, message, event = calendar.add_event(start_time, end_time, label)
        print(f"✅ {message}" if success else f"❌ {message}")
        
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")

def handle_delete_event(calendar):
    """Handle deleting an event."""
    try:
        event_id = int(input("Event ID to delete: "))
        success, message = calendar.delete_event(event_id)
        print(f"✅ {message}" if success else f"❌ {message}")
    except ValueError:
        print("❌ Invalid event ID")

def handle_list_events(calendar):
    """Handle listing all events."""
    events = calendar.interval_tree.get_all_events()
    if events:
        print(f"\n📅 All Events ({len(events)} total):")
        for event in events:
            print(f"  [{event.event_id}] {event}")
    else:
        print("📅 No events scheduled")

def handle_show_conflicts(calendar):
    """Handle showing all conflicts."""
    conflicts = calendar.get_all_conflicts()
    if conflicts:
        print(f"\n⚠️  Conflicts Found ({len(conflicts)} events with conflicts):")
        for event, conflicting in conflicts:
            print(f"  📍 {event}")
            for conflict in conflicting:
                print(f"    ↳ Conflicts with: {conflict}")
    else:
        print("✅ No conflicts found")

def handle_find_free_slots(calendar):
    """Handle finding free slots."""
    try:
        duration = int(input("Duration in minutes: "))
        start_str = input("Search start time (YYYY-MM-DD HH:MM): ")
        end_str = input("Search end time (YYYY-MM-DD HH:MM): ")
        
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        
        free_slots = calendar.find_free_slots(duration, start_time, end_time)
        
        if free_slots:
            print(f"\n🕐 Free slots for {duration} minutes:")
            for i, (slot_start, slot_end) in enumerate(free_slots[:10], 1):  # Show first 10
                print(f"  {i}. {slot_start.strftime('%Y-%m-%d %H:%M')} - {slot_end.strftime('%H:%M')}")
            if len(free_slots) > 10:
                print(f"  ... and {len(free_slots) - 10} more slots")
        else:
            print(f"❌ No free slots found for {duration} minutes")
            
    except ValueError as e:
        print(f"❌ Invalid input: {e}")

def handle_events_at_time(calendar):
    """Handle showing events at a specific time."""
    try:
        time_str = input("Query time (YYYY-MM-DD HH:MM): ")
        query_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        
        events = calendar.get_events_at_time(query_time)
        
        if events:
            print(f"\n📍 Events at {query_time.strftime('%Y-%m-%d %H:%M')}:")
            for event in events:
                print(f"  • {event}")
        else:
            print(f"📍 No events at {query_time.strftime('%Y-%m-%d %H:%M')}")
            
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")

def handle_event_density(calendar):
    """Handle showing event density."""
    try:
        start_str = input("Start time (YYYY-MM-DD HH:MM): ")
        end_str = input("End time (YYYY-MM-DD HH:MM): ")
        slot_minutes = int(input("Slot duration in minutes (default 60): ") or "60")
        
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        
        density = calendar.get_event_density(start_time, end_time, slot_minutes)
        
        print(f"\n📊 Event Density ({slot_minutes}-minute slots):")
        for slot_time, count in density.items():
            bar = "█" * count if count > 0 else "░"
            print(f"  {slot_time.strftime('%H:%M')} │{bar:<10} {count} events")
            
    except ValueError as e:
        print(f"❌ Invalid input: {e}")

def handle_export_events(calendar):
    """Handle exporting events."""
    filename = input("Export filename (default: events.json): ") or "events.json"
    try:
        calendar.export_events(filename)
        print(f"✅ Events exported to {filename}")
    except Exception as e:
        print(f"❌ Export failed: {e}")

def handle_import_events(calendar):
    """Handle importing events."""
    filename = input("Import filename: ")
    success, message = calendar.import_events(filename)
    print(f"✅ {message}" if success else f"❌ {message}")

if __name__ == "__main__":
    main()