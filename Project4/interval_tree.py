#!/usr/bin/env python3
"""
AVL-based Interval Tree implementation for efficient overlap detection
Time Complexity: O(log n) for insert, delete, search
Space Complexity: O(n)
"""

from typing import List, Optional
from models import Event

class IntervalTreeNode:
    """Node for Interval Tree implementation."""
    
    def __init__(self, event: Event):
        self.event = event
        self.max_end = event.end_time
        self.left: Optional['IntervalTreeNode'] = None
        self.right: Optional['IntervalTreeNode'] = None
        self.height = 1

class IntervalTree:
    """AVL-based Interval Tree for efficient overlap detection."""
    
    def __init__(self):
        self.root: Optional[IntervalTreeNode] = None
        self.size = 0
    
    def _height(self, node: Optional[IntervalTreeNode]) -> int:
        return node.height if node else 0
    
    def _balance_factor(self, node: Optional[IntervalTreeNode]) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0
    
    def _update_height(self, node: Optional[IntervalTreeNode]) -> None:
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    def _update_max_end(self, node: Optional[IntervalTreeNode]) -> None:
        if node:
            node.max_end = node.event.end_time
            if node.left and node.left.max_end > node.max_end:
                node.max_end = node.left.max_end
            if node.right and node.right.max_end > node.max_end:
                node.max_end = node.right.max_end
    
    def _rotate_right(self, y: IntervalTreeNode) -> IntervalTreeNode:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        self._update_max_end(y)
        self._update_max_end(x)
        return x
    
    def _rotate_left(self, x: IntervalTreeNode) -> IntervalTreeNode:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        self._update_max_end(x)
        self._update_max_end(y)
        return y
    
    def _insert(self, node: Optional[IntervalTreeNode], event: Event) -> IntervalTreeNode:
        # BST insertion based on start time
        if not node:
            self.size += 1
            return IntervalTreeNode(event)
        
        if event.start_time < node.event.start_time:
            node.left = self._insert(node.left, event)
        else:
            node.right = self._insert(node.right, event)
        
        # Update height and max_end
        self._update_height(node)
        self._update_max_end(node)
        
        # AVL balancing
        balance = self._balance_factor(node)
        
        # Left Left Case
        if balance > 1 and event.start_time < node.left.event.start_time:
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and event.start_time >= node.right.event.start_time:
            return self._rotate_left(node)
        
        # Left Right Case
        if balance > 1 and event.start_time >= node.left.event.start_time:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Left Case
        if balance < -1 and event.start_time < node.right.event.start_time:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _find_min(self, node: IntervalTreeNode) -> IntervalTreeNode:
        while node.left:
            node = node.left
        return node
    
    def _delete(self, node: Optional[IntervalTreeNode], event_id: int) -> Optional[IntervalTreeNode]:
        if not node:
            return node
        
        if event_id < node.event.event_id:
            node.left = self._delete(node.left, event_id)
        elif event_id > node.event.event_id:
            node.right = self._delete(node.right, event_id)
        else:
            # Node to be deleted found
            self.size -= 1
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node with two children
            temp = self._find_min(node.right)
            node.event = temp.event
            node.right = self._delete(node.right, temp.event.event_id)
        
        if not node:
            return node
        
        # Update height and max_end
        self._update_height(node)
        self._update_max_end(node)
        
        # AVL balancing
        balance = self._balance_factor(node)
        
        # Left Left Case
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        # Left Right Case
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        # Right Left Case
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def insert(self, event: Event) -> None:
        """Insert an event into the interval tree."""
        self.root = self._insert(self.root, event)
    
    def delete(self, event_id: int) -> None:
        """Delete an event by ID from the interval tree."""
        self.root = self._delete(self.root, event_id)
    
    def find_overlapping(self, query_event: Event) -> List[Event]:
        """Find all events that overlap with the query event."""
        overlapping = []
        self._find_overlapping_helper(self.root, query_event, overlapping)
        return overlapping
    
    def _find_overlapping_helper(self, node: Optional[IntervalTreeNode], query_event: Event, result: List[Event]) -> None:
        if not node:
            return
        
        # If query event starts after the maximum end time in this subtree
        if query_event.start_time >= node.max_end:
            return
        
        # Check current node
        if node.event.overlaps_with(query_event):
            result.append(node.event)
        
        # Recursively search left subtree
        self._find_overlapping_helper(node.left, query_event, result)
        
        # Search right subtree only if necessary
        if node.event.start_time < query_event.end_time:
            self._find_overlapping_helper(node.right, query_event, result)
    
    def get_all_events(self) -> List[Event]:
        """Get all events in chronological order."""
        events = []
        self._inorder_traversal(self.root, events)
        return events
    
    def _inorder_traversal(self, node: Optional[IntervalTreeNode], events: List[Event]) -> None:
        if node:
            self._inorder_traversal(node.left, events)
            events.append(node.event)
            self._inorder_traversal(node.right, events)