def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0 and n > 2:
        return False
    r = int(n**0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    candidate = max(3, n + 1)
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 1

class HashSet:
    def __init__(self, collision_type, params):
        if collision_type != "Chain":
            raise NotImplementedError("Only chaining is implemented")
        z, table_size = params
        self.z = z
        self.size = next_prime(table_size)
        self.count = 0
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        h = 0
        for c in key:
            h = (h * self.z + ord(c)) % self.size
        return h

    def insert(self, key):
        idx = self._hash(key)
        bucket = self.table[idx]
        if key in bucket:
            return
        bucket.append(key)
        self.count += 1
        if self.count / self.size >= 0.5:
            self._rehash()

    def find(self, key):
        idx = self._hash(key)
        return key in self.table[idx]

    def get_slot(self, key):
        return self._hash(key)

    def get_load(self):
        return self.count / self.size

    def __str__(self):
        parts = []
        for bucket in self.table:
            if bucket:
                parts.append(" ; ".join(bucket))
            else:
                parts.append("⟨EMPTY⟩")
        return " | ".join(parts)

    def _rehash(self):
        old = self.table
        new_size = next_prime(self.size * 2)
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        old_count = self.count
        self.count = 0
        for bucket in old:
            for key in bucket:
                self.insert(key)
        # Verify count is preserved
        assert self.count == old_count

class HashMap:
    def __init__(self, collision_type, params):
        if collision_type != "Chain":
            raise NotImplementedError("Only chaining is implemented")
        z, table_size = params
        self.z = z
        self.size = next_prime(table_size)
        self.count = 0
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        h = 0
        for c in key:
            h = (h * self.z + ord(c)) % self.size
        return h

    def insert(self, key, value):
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1
        if self.count / self.size >= 0.5:
            self._rehash()

    def find(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def get_slot(self, key):
        return self._hash(key)

    def get_load(self):
        return self.count / self.size

    def __str__(self):
        parts = []
        for bucket in self.table:
            if bucket:
                parts.append(" ; ".join(f"({k}, {v})" for k, v in bucket))
            else:
                parts.append("⟨EMPTY⟩")
        return " | ".join(parts)

    def _rehash(self):
        old = self.table
        new_size = next_prime(self.size * 2)
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        old_count = self.count
        self.count = 0
        for bucket in old:
            for k, v in bucket:
                self.insert(k, v)
        # Verify count is preserved
        assert self.count == old_count
