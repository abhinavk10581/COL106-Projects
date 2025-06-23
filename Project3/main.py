from navigator import MapNavigator
from map_factory import create_sample_map
from models import TrafficLevel

def main():
    """Example usage of the MapNavigator"""
    # Create sample map
    navigator = create_sample_map()
    
    print("Map Navigator - Core Version")
    print("=" * 40)
    
    # Print initial map status
    navigator.print_map_status()
    
    print("\n" + "=" * 40)
    print("Finding path from Downtown (A) to Stadium (F)")
    
    # Find path using A* algorithm
    path, cost, search_info = navigator.a_star_search("A", "F", "euclidean")
    
    # Display results
    print(navigator.get_path_info(path, cost, search_info))
    
    print("\n" + "=" * 40)
    print("Simulating traffic updates...")
    
    # Simulate some traffic
    navigator.update_traffic("A", "B", TrafficLevel.HEAVY)
    navigator.update_traffic("B", "D", TrafficLevel.JAM)
    navigator.close_road("B", "C", True)  # Close bridge
    
    print("Updated traffic conditions:")
    print("- Heavy traffic on A → B")
    print("- Traffic jam on B → D")
    print("- Bridge B → C is closed")
    
    # Find new path with updated traffic
    print("\nFinding new path with updated traffic...")
    new_path, new_cost, new_search_info = navigator.a_star_search("A", "F", "euclidean")
    
    print(navigator.get_path_info(new_path, new_cost, new_search_info))
    
    # Compare paths
    if path != new_path:
        print(f"\nPath changed due to traffic!")
        print(f"Original cost: {cost:.2f}")
        print(f"New cost: {new_cost:.2f}")
        print(f"Cost difference: {new_cost - cost:.2f}")

if __name__ == "__main__":
    main()