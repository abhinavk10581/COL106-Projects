from models import Node, Edge, RoadType
from navigator import MapNavigator

def create_sample_map() -> MapNavigator:
    """Create a sample map with nodes and edges"""
    navigator = MapNavigator()
    
    # Create nodes representing locations
    locations = [
        Node("A", 10, 10, "Downtown"),
        Node("B", 50, 15, "Mall"),
        Node("C", 20, 40, "Hospital"),
        Node("D", 60, 35, "Airport"),
        Node("E", 30, 60, "University"),
        Node("F", 70, 60, "Stadium"),
        Node("G", 15, 80, "Beach"),
        Node("H", 45, 75, "Park"),
        Node("I", 80, 20, "Industrial"),
        Node("J", 85, 45, "Suburbs")
    ]
    
    for node in locations:
        navigator.add_node(node)
    
    # Create edges representing roads
    roads = [
        # Highway connections (faster)
        Edge("A", "B", 8, RoadType.HIGHWAY),
        Edge("B", "D", 6, RoadType.HIGHWAY),
        Edge("D", "I", 5, RoadType.HIGHWAY),
        Edge("I", "J", 7, RoadType.HIGHWAY),
        
        # Main roads
        Edge("A", "C", 12, RoadType.MAIN_ROAD),
        Edge("C", "E", 10, RoadType.MAIN_ROAD),
        Edge("E", "H", 8, RoadType.MAIN_ROAD),
        Edge("H", "F", 9, RoadType.MAIN_ROAD),
        Edge("D", "F", 11, RoadType.MAIN_ROAD),
        Edge("F", "J", 8, RoadType.MAIN_ROAD),
        
        # Residential roads (slower)
        Edge("C", "G", 15, RoadType.RESIDENTIAL),
        Edge("E", "G", 12, RoadType.RESIDENTIAL),
        Edge("G", "H", 14, RoadType.RESIDENTIAL),
        
        # Bridge (can be closed)
        Edge("B", "C", 7, RoadType.BRIDGE),
        
        # Additional connections
        Edge("A", "E", 18, RoadType.RESIDENTIAL),
        Edge("B", "F", 20, RoadType.MAIN_ROAD),
        Edge("C", "H", 16, RoadType.RESIDENTIAL),
        Edge("D", "J", 6, RoadType.MAIN_ROAD)
    ]
    
    for edge in roads:
        navigator.add_edge(edge)
    
    return navigator