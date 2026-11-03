from collections.abc import Hashable, Iterator


class HashMap[K: Hashable, V]:
    def __init__(self) -> None:
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(8)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _index(self, key: K, capacity: int | None = None) -> int:
        return hash(key) % (len(self._buckets) if capacity is None else capacity)

    def set(self, key: K, value: V) -> bool:
        bucket = self._buckets[self._index(key)]
        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[i] = (key, value)
                return False
        bucket.append((key, value))
        self._size += 1
        if self._size * 4 > len(self._buckets) * 3:
            self._resize(2 * len(self._buckets))
        return True

    def _resize(self, capacity: int) -> None:
        buckets: list[list[tuple[K, V]]] = [[] for _ in range(capacity)]
        for bucket in self._buckets:
            for key, value in bucket:
                buckets[self._index(key, capacity)].append((key, value))
        self._buckets = buckets

    def get(self, key: K) -> V:
        for stored_key, value in self._buckets[self._index(key)]:
            if stored_key == key:
                return value
        raise KeyError(key)

    def delete(self, key: K) -> bool:
        bucket = self._buckets[self._index(key)]
        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def items(self) -> Iterator[tuple[K, V]]:
        for bucket in self._buckets:
            yield from bucket
