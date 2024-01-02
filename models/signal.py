import numpy as np
from typing import List


class Signal:
    """
    Represents a signal with x and y vectors.
    """

    def __init__(self, x_vec: List[float], y_vec: List[float]) -> None:
        """
        Initialize the Signal with x and y vectors.

        Args:
        x_vec (List[float]): The x vector.
        y_vec (List[float]): The y vector.
        """
        self.x_vec = x_vec
        self.y_vec = y_vec
        self.last_drawn_index = 0
        self.hidden = False

    def get_statistics(self, index):
        """
        Get statistics for the signal up to the given index.

        Args:
        index (int): The index up to which statistics are calculated.

        Returns:
        dict: A dictionary containing the calculated statistics.
        """
        start = max(index - 360, 0)
        y_vec = self.y_vec[start:index]
        statistics = {
            "mean": round(np.mean(y_vec), 2),
            "median": round(np.median(y_vec), 2),
            "std": round(np.std(y_vec), 2),
            "max_value": round(max(y_vec), 2),
            "min_value": round(min(y_vec), 2),
        }
        return statistics
