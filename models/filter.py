from typing import List

from models.signal import Signal


class Filter:
    def __init__(self, coefficients: List[float]) -> None:
        """
        Initialize the Filter with the given coefficients.

        Args:
        coefficients (List[float]): The coefficients of the digital filter.
        """
        self.coefficients = coefficients

    def apply(self, signal: Signal) -> Signal:
        """
        Apply the digital filter to the given signal.

        Args:
        signal (Signal): The input signal to filter.

        Returns:
        Signal: The filtered output signal.
        """
        # Implementation of filter logic goes here
        pass
