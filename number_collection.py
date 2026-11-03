"""
CPTR 2265 - Lab 7, Part B (optional starter)
============================================

A simple data structure whose sorting algorithm is chosen with an if/elif
chain on a string. Adding a new algorithm means editing this class, and the
client must know the magic strings.

Your task: apply the STRATEGY pattern so that
  * each sorting algorithm lives in its own class with a common interface
    (e.g. a SortStrategy base class / Protocol with a sort(values) method),
  * NumberCollection receives a strategy (constructor and/or a setter),
  * the client can switch algorithms at runtime WITHOUT changing the code
    inside NumberCollection.

You may use this file, or write your own simple data structure instead.
"""


class BubbleSort:
    def sort(self, values):
        data = list(values)
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

class MergeSort:
    def sort(self, values):
        return self._merge_sort(list(values))

    def _merge_sort(self, data):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self._merge_sort(data[:mid])
        right = self._merge_sort(data[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

class NumberCollection:
    _strategies = {
        "bubble": BubbleSort(),
        "merge": MergeSort()
    }

    def __init__(self, values=None, strategy=None):
        self._values = list(values) if values else []
        if isinstance(strategy, str):
            self._strategy = self._strategies.get(strategy, BubbleSort())
        elif strategy is not None:
            self._strategy = strategy
        else:
            self._strategy = self._strategies["bubble"]

    def set_strategy(self, strategy):
        """Allows setting or switching the strategy at runtime via object or string name."""
        if isinstance(strategy, str):
            if strategy in self._strategies:
                self._strategy = self._strategies[strategy]
            else:
                raise ValueError("Unknown sorting algorithm: " + strategy)
        else:
            self._strategy = strategy

    def add(self, value):
        self._values.append(value)

    def values(self):
        return list(self._values)

    def sort(self, algorithm=None):
        """Delegates sorting to the current strategy, supporting legacy string arguments."""
        if algorithm is not None:
            self.set_strategy(algorithm)
        self._values = self._strategy.sort(self._values)
        return self._values
    


# ---------------------------------------------------------------- client ---
if __name__ == "__main__":
    nums = NumberCollection([42, 7, 19, 3, 88, 25, 61])
    nums.sort("bubble")
    print("Bubble sort:", nums.values())

    nums = NumberCollection([42, 7, 19, 3, 88, 25, 61])
    nums.sort("merge")
    print("Merge sort: ", nums.values())
