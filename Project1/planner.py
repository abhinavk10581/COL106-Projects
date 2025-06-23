from flight import Flight
import heapq
from collections import deque, defaultdict

class Planner:
    def __init__(self, flights):
        """Initialize the planner with flight data"""
        # Build adjacency list for graph representation
        self.graph = defaultdict(list)
        for flight in flights:
            self.graph[flight.start_city].append(flight)
        
        # Sort flights by departure time for each city for efficiency
        for city in self.graph:
            self.graph[city].sort(key=lambda f: f.departure_time)
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Find route with minimum flights, breaking ties by earliest arrival
        Uses BFS for optimal solution
        """
        if start_city == end_city:
            return []
        
        # BFS queue: (num_flights, current_time, city, path)
        queue = deque([(0, t1, start_city, [])])
        
        # Track best state for each city: (min_flights, earliest_time_for_min_flights)
        best_state = {}
        
        min_flights = float('inf')
        best_route = None
        best_arrival_time = float('inf')
        
        while queue:
            num_flights, current_time, city, path = queue.popleft()
            
            # Pruning: if we already found a solution with fewer flights, skip
            if num_flights > min_flights:
                continue
            
            # State pruning: skip if we've seen this city with better or equal state
            if city in best_state:
                prev_flights, prev_time = best_state[city]
                if prev_flights < num_flights or (prev_flights == num_flights and prev_time <= current_time):
                    continue
            
            best_state[city] = (num_flights, current_time)
            
            # Check if we reached destination
            if city == end_city:
                if num_flights < min_flights or (num_flights == min_flights and current_time < best_arrival_time):
                    min_flights = num_flights
                    best_arrival_time = current_time
                    best_route = path[:]
                continue
            
            # Explore neighbors
            for flight in self.graph[city]:
                # Check time constraints
                min_departure = current_time + (20 if path else 0)  # 20 min connection time
                
                if (flight.departure_time >= max(min_departure, t1) and 
                    flight.arrival_time <= t2):
                    
                    new_path = path + [flight]
                    queue.append((num_flights + 1, flight.arrival_time, flight.end_city, new_path))
        
        return best_route if best_route else []
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Find route with minimum total fare
        Uses Dijkstra's algorithm
        """
        if start_city == end_city:
            return []
        
        # Priority queue: (total_fare, current_time, city, path)
        pq = [(0, t1, start_city, [])]
        
        # Track minimum cost to reach each city at each time
        # Key: (city, time), Value: min_cost
        best_cost = {}
        
        while pq:
            total_fare, current_time, city, path = heapq.heappop(pq)
            
            # Check if we reached destination
            if city == end_city:
                return path
            
            # State pruning
            state_key = (city, current_time)
            if state_key in best_cost and best_cost[state_key] <= total_fare:
                continue
            best_cost[state_key] = total_fare
            
            # Explore neighbors
            for flight in self.graph[city]:
                min_departure = current_time + (20 if path else 0)
                
                if (flight.departure_time >= max(min_departure, t1) and 
                    flight.arrival_time <= t2):
                    
                    new_fare = total_fare + flight.fare
                    new_path = path + [flight]
                    heapq.heappush(pq, (new_fare, flight.arrival_time, flight.end_city, new_path))
        
        return []
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Find route with minimum flights, breaking ties by minimum cost
        Uses modified Dijkstra with lexicographic ordering
        """
        if start_city == end_city:
            return []
        
        # Priority queue: (num_flights, total_fare, current_time, city, path)
        pq = [(0, 0, t1, start_city, [])]
        
        # Track best state for each city: (min_flights, min_cost_for_min_flights)
        best_state = {}
        
        while pq:
            num_flights, total_fare, current_time, city, path = heapq.heappop(pq)
            
            # Check if we reached destination
            if city == end_city:
                return path
            
            # State pruning
            if city in best_state:
                prev_flights, prev_cost = best_state[city]
                if (prev_flights < num_flights or 
                    (prev_flights == num_flights and prev_cost <= total_fare)):
                    continue
            
            best_state[city] = (num_flights, total_fare)
            
            # Explore neighbors
            for flight in self.graph[city]:
                min_departure = current_time + (20 if path else 0)
                
                if (flight.departure_time >= max(min_departure, t1) and 
                    flight.arrival_time <= t2):
                    
                    new_flights = num_flights + 1
                    new_fare = total_fare + flight.fare
                    new_path = path + [flight]
                    
                    heapq.heappush(pq, (new_flights, new_fare, flight.arrival_time, 
                                      flight.end_city, new_path))
        
        return []


# Additional utility classes if needed for custom implementations
class OptimizedQueue:
    """Optimized queue using deque for O(1) operations"""
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        return self.items.popleft() if self.items else None
    
    def is_empty(self):
        return len(self.items) == 0


class StateTracker:
    """Efficient state tracking using dictionary"""
    def __init__(self):
        self.states = {}
    
    def update_state(self, key, value):
        self.states[key] = value
    
    def get_state(self, key):
        return self.states.get(key)
    
    def is_better_state(self, key, new_value, comparison_func):
        """Check if new state is better than existing state"""
        existing = self.get_state(key)
        if existing is None:
            return True
        return comparison_func(new_value, existing)