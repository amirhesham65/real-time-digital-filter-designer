from enum import Enum
import numpy as np
from scipy import signal


class PointType(Enum):
    ZERO = "zero"
    POLE = "pole"


class Filter:
    def __init__(self, zeros=None, poles=None, gain=1) -> None:
        """
        Initialize the Filter class with zeros, poles, and gain.
        If zeros and poles are not given, they are set to an empty list.
        The default value for gain is 1.
        """
        self.__zeros = zeros if zeros else []
        self.__poles = poles if poles else []
        self.__all_pass = []
        self.__gain = gain

    # Define getters
    def get_zeros(self):
        """
        Get the zeros of the filter.
        """
        return self.__zeros[:]

    def get_poles(self):
        """
        Get the poles of the filter.
        """
        return self.__poles[:]

    def get_gain(self):
        """
        Get the gain of the filter.
        """
        return self.__gain

    def get_all_pass(self):
        """
        Set the all-passes of the filter.
        """
        return self.__all_pass[:]

    # Define setters
    def set_zeros(self, zeros: list) -> None:
        """
        Set the zeros of the filter.
        """
        self.__zeros = [*self.__zeros, *zeros]

    def set_poles(self, poles: list) -> None:
        """
        Set the poles of the filter.
        """
        self.__poles = [*self.__poles, *poles]

    def set_gain(self, gain: float) -> None:
        """
        Set the gain of the filter.
        """
        self.__gain = gain

    # Define instance methods
    def response(self, w=None) -> tuple:
        """
        Get the response of the filter at a given frequency (w).
        If w is not given, compute the response at a range of frequencies.
        Returns a tuple of w (frequency), magnitude, and phase.
        """
        if w is None:
            w, response = signal.freqz_zpk(self.__zeros, self.__poles, self.__gain)
            # `w` is the x_axis from 0 hz to fmax hz (default value normalized from 0 to pi)
            # `response` is the complex output of z_transform where we can get the magnitude & phase
        else:
            response = signal.zpk_eval_response(self.__zeros, self.__poles, self.__gain, w)
        magnitude = 20 * np.log10(np.abs(response))
        # convert from hz into decibels
        phase = np.unwrap(np.angle(response))   # `np.unwrap` to remove phase discontinuities
        return w, magnitude, phase

    def add_all_pass(self, a: complex):
        """
        Add one all-pass filter with coefficient a to the filter.
        """
        self.__all_pass.append(a)
        self.__poles.append(a)
        self.__zeros.append(1 / np.conj(a))

    def add_list_all_pass(self, a_list: list):
        """
        Add one or more all-pass filters with coefficient a to the filter.
        """
        self.__all_pass = a_list.copy()
        self.__poles = [*self.__poles, *a_list]
        b_list = []
        for i in range(len(a_list)):
            b_list.append(1 / np.conj(a_list[i]))
        self.__zeros = [*self.__zeros, *b_list]

    def remove_zero(self, zero:complex):
        """
        Remove one zero from the filter.
        """
        self.__zeros.remove(zero)

    def remove_pole(self, pole:complex):
        """
        Remove one pole from the filter.
        """
        self.__poles.remove(pole)

    def remove_all_zeros(self):
        """
        Remove all zeros from the filter.
        """
        self.__zeros = []

    def remove_all_poles(self):
        """
        Remove all poles from the filter.
        """
        self.__poles= []

    def remove_all_pass(self, a:complex):
        """
        Remove one all-pass filter with coefficient a to the filter.
        """
        self.__all_pass.remove(a)
        self.__poles.remove(a)
        self.__zeros.remove(1 / np.conj(a))

    def remove_all_all_passes(self):
        """
        Remove all all-pass filters from the filter.
        """
        self.__zeros = self.__zeros[0:len(self.__zeros) - len(self.__all_pass)]
        self.__poles = self.__poles[0:len(self.__poles) - len(self.__all_pass)]
        self.__all_pass = []

    def apply_filter(self, values: list) -> []:
        numerator , denominator = signal.zpk2tf(self.__zeros,self.__poles, self.__gain)
        filtered_signal = np.real(signal.lfilter(numerator, denominator, values))
        return filtered_signal