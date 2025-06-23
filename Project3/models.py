from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, Optional, Set

class RoadType(Enum):
    HIGHWAY = "highway"
    MAIN_ROAD = "main_road"
    RESIDENTIAL = "residential"
    BRIDGE = "bridge"

class TrafficLevel(Enum):
    LIGHT = 0.8
    NORMAL = 1.0
    HEAVY = 1.5
    JAM = 2.5
    BLOCKED = float('inf')

@dataclass
class Node:
    id: str
    x: float
    y: float
    name: str = ""
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

@dataclass
class Edge:
    from_node: str
    to_node: str
    base_weight: float
    road_type: RoadType
    current_traffic: float = 1.0  # Traffic multiplier (1.0 = normal, 2.0 = double time)
    is_closed: bool = False
    
    @property
    def effective_weight(self) -> float:
        if self.is_closed:
            return float('inf')
        return self.base_weight * self.current_traffic