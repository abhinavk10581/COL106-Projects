from hash_table import HashSet, HashMap

class PlagiarismEngine:
    def __init__(self, collision_type, params, n):
        if n < 1:
            raise ValueError("n-gram size must be at least 1")
        self.n = n
        self.collision_type = collision_type
        self.params = params
        # Map title -> HashSet of n-grams
        self.docs = HashMap("Chain", params)
        self.titles = []

    def add_document(self, title, word_list):
        # Check if title already exists
        if self.docs.find(title) is not None:
            raise ValueError(f"Document title '{title}' already exists")
        
        if not word_list:
            raise ValueError("Document cannot be empty")
        
        W = len(word_list)
        hset = HashSet(self.collision_type, self.params)
        
        if W >= self.n:
            # Generate n-grams
            for i in range(W - self.n + 1):
                ngram = " ".join(word_list[i:i+self.n])
                hset.insert(ngram)
        else:
            # If document is shorter than n, treat the whole document as one n-gram
            ngram = " ".join(word_list)
            hset.insert(ngram)
        
        # Store the document
        self.docs.insert(title, hset)
        self.titles.append(title)

    def get_distinct_count(self, title):
        hset = self.docs.find(title)
        if hset is None:
            return 0
        return hset.count

    def compare_pair(self, title1, title2):
        set1 = self.docs.find(title1)
        set2 = self.docs.find(title2)
        if set1 is None or set2 is None:
            return 0.0
        
        if set1.count == 0 and set2.count == 0:
            return 1.0  # Both empty sets are identical
        
        if set1.count == 0 or set2.count == 0:
            return 0.0  # One empty, one non-empty

        # Iterate through the smaller set for efficiency
        if set1.count <= set2.count:
            small, large = set1, set2
        else:
            small, large = set2, set1

        inter = 0
        # Count intersection by iterating through smaller set
        for bucket in small.table:
            for key in bucket:
                if large.find(key):
                    inter += 1

        union = set1.count + set2.count - inter
        return inter / union if union > 0 else 0.0

    def find_most_similar(self, title):
        if title not in self.titles:
            raise ValueError(f"Document '{title}' not found")
        
        if len(self.titles) <= 1:
            return [], 0.0  # No other documents to compare
        
        best = []
        best_score = -1.0
        
        for other in self.titles:
            if other == title:
                continue
            score = self.compare_pair(title, other)
            if score > best_score:
                best_score = score
                best = [other]
            elif score == best_score:
                best.append(other)
        
        return best, best_score

    def report_similar_pairs(self, threshold):
        if not (0 <= threshold <= 1):
            raise ValueError("Threshold must be between 0 and 1")
        
        results = []
        K = len(self.titles)
        
        for i in range(K):
            for j in range(i+1, K):
                t1 = self.titles[i]
                t2 = self.titles[j]
                score = self.compare_pair(t1, t2)
                if score >= threshold:
                    results.append((t1, t2, score))
        
        return sorted(results, key=lambda x: x[2], reverse=True)  # Sort by score descending

