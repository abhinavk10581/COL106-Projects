import heapq
import math
import random
from typing import Dict, List, Tuple, Optional, Set
from models import Node, Edge, RoadType, TrafficLevel

class MapNavigator:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}
        self.traffic_updates_enabled = True
        self.last_path = []
        self.path_history = []
        
    def add_node(self, node: Node):
        """Add a node to the map"""
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = []
    
    def add_edge(self, edge: Edge):
        """Add a bidirectional edge to the map"""
        if edge.from_node not in self.edges:
            self.edges[edge.from_node] = []
        if edge.to_node not in self.edges:
            self.edges[edge.to_node] = []
            
        self.edges[edge.from_node].append(edge)
        # Add reverse edge
        reverse_edge = Edge(
            from_node=edge.to_node,
            to_node=edge.from_node,
            base_weight=edge.base_weight,
            road_type=edge.road_type,
            current_traffic=edge.current_traffic,
            is_closed=edge.is_closed
        )
        self.edges[edge.to_node].append(reverse_edge)
    
    def euclidean_distance(self, node1: Node, node2: Node) -> float:
        """Calculate Euclidean distance between two nodes"""
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    
    def manhattan_distance(self, node1: Node, node2: Node) -> float:
        """Calculate Manhattan distance between two nodes"""
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)
    
    def a_star_search(self, start_id: str, goal_id: str, heuristic_type: str = "euclidean") -> Tuple[List[str], float, Dict]:
        """
        A* search algorithm with detailed tracking
        Returns: (path, total_cost, search_info)
        """
        if start_id not in self.nodes or goal_id not in self.nodes:
            return [], float('inf'), {}
        
        start_node = self.nodes[start_id]
        goal_node = self.nodes[goal_id]
        
        # Choose heuristic function
        heuristic = self.euclidean_distance if heuristic_type == "euclidean" else self.manhattan_distance
        
        # Priority queue: (f_score, node_id)
        open_set = [(0, start_id)]
        came_from = {}
        g_score = {start_id: 0}
        f_score = {start_id: heuristic(start_node, goal_node)}
        
        # For visualization
        open_set_nodes = {start_id}
        closed_set_nodes = set()
        
        while open_set:
            current_f, current_id = heapq.heappop(open_set)
            
            if current_id in closed_set_nodes:
                continue
                
            open_set_nodes.discard(current_id)
            closed_set_nodes.add(current_id)
            
            if current_id == goal_id:
                # Reconstruct path
                path = []
                current = goal_id
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_id)
                path.reverse()
                
                search_info = {
                    'open_set': open_set_nodes.copy(),
                    'closed_set': closed_set_nodes.copy(),
                    'nodes_explored': len(closed_set_nodes)
                }
                
                return path, g_score[goal_id], search_info
            
            # Explore neighbors
            for edge in self.edges.get(current_id, []):
                neighbor_id = edge.to_node
                
                if neighbor_id in closed_set_nodes:
                    continue
                
                tentative_g_score = g_score[current_id] + edge.effective_weight
                
                if neighbor_id not in g_score or tentative_g_score < g_score[neighbor_id]:
                    came_from[neighbor_id] = current_id
                    g_score[neighbor_id] = tentative_g_score
                    neighbor_node = self.nodes[neighbor_id]
                    f_score[neighbor_id] = tentative_g_score + heuristic(neighbor_node, goal_node)
                    
                    if neighbor_id not in open_set_nodes:
                        heapq.heappush(open_set, (f_score[neighbor_id], neighbor_id))
                        open_set_nodes.add(neighbor_id)
        
        # No path found
        search_info = {
            'open_set': open_set_nodes.copy(),
            'closed_set': closed_set_nodes.copy(),
            'nodes_explored': len(closed_set_nodes)
        }
        return [], float('inf'), search_info
    
    def update_traffic(self, from_node: str, to_node: str, traffic_level: TrafficLevel):
        """Update traffic on a specific road segment"""
        for edge in self.edges.get(from_node, []):
            if edge.to_node == to_node:
                edge.current_traffic = traffic_level.value
                break
        
        # Update reverse direction
        for edge in self.edges.get(to_node, []):
            if edge.to_node == from_node:
                edge.current_traffic = traffic_level.value
                break
    
    def close_road(self, from_node: str, to_node: str, is_closed: bool = True):
        """Close or open a road segment"""
        for edge in self.edges.get(from_node, []):
            if edge.to_node == to_node:
                edge.is_closed = is_closed
                break
        
        # Update reverse direction
        for edge in self.edges.get(to_node, []):
            if edge.to_node == from_node:
                edge.is_closed = is_closed
                break
    
    def simulate_traffic_updates(self):
        """Simulate random traffic updates"""
        if not self.traffic_updates_enabled:
            return
            
        # Randomly update traffic on some edges
        all_edges = []
        for edge_list in self.edges.values():
            all_edges.extend(edge_list)
        
        if all_edges:
            # Update 10-20% of edges
            num_updates = max(1, len(all_edges) // 10)
            random_edges = random.sample(all_edges, min(num_updates, len(all_edges)))
            
            for edge in random_edges:
                # Random traffic level
                traffic_levels = [TrafficLevel.LIGHT, TrafficLevel.NORMAL, TrafficLevel.HEAVY]
                if random.random() < 0.1:  # 10% chance of jam
                    traffic_levels.append(TrafficLevel.JAM)
                
                new_traffic = random.choice(traffic_levels)
                edge.current_traffic = new_traffic.value
    
    def get_path_info(self, path: List[str], cost: float, search_info: Dict) -> str:
        """Get formatted path information"""
        if not path:
            return f"No path found! Nodes explored: {search_info.get('nodes_explored', 0)}"
        
        info = f"Path Found!\n"
        info += f"Route: {' → '.join(path)}\n"
        info += f"Total Cost: {cost:.2f}\n"
        info += f"Nodes Explored: {search_info.get('nodes_explored', 0)}\n"
        info += f"Path Length: {len(path)} stops\n\n"
        
        # Detailed path info
        info += "Detailed Route:\n"
        for i in range(len(path) - 1):
            from_node = self.nodes[path[i]]
            to_node = self.nodes[path[i + 1]]
            info += f"{from_node.name} → {to_node.name}\n"
        
        return info
    
    def print_map_status(self):
        """Print current map status"""
        print(f"Map Status:")
        print(f"Nodes: {len(self.nodes)}")
        print(f"Edges: {sum(len(edges) for edges in self.edges.values())}")
        
        # Print traffic status
        print("\nTraffic Status:")
        for from_node, edges in self.edges.items():
            for edge in edges:
                status = "CLOSED" if edge.is_closed else f"Traffic: {edge.current_traffic:.1f}x"
                print(f"{from_node} → {edge.to_node}: {status} ({edge.road_type.value})")