import numpy as np
from scipy import signal

from view.TargetItms import Pole, Zero


class AllPass:
    def __init__(self, a):
        self.a = a


class Filter:
    def __init__(self, poles=None, zeros=None, gain=1):
        self.poles = []
        self.zeros = []
        self.poles_values = poles if poles else []
        self.zeros_values = zeros if zeros else []
        self.all_pass = []
        self.gain = gain

    def add_pole(self, pole: Pole):
        self.poles.append(pole)

    def add_zero(self, zero: Zero):
        self.zeros.append(zero)

    def add_all_pass(self, all_pass: AllPass):
        self.all_pass.append(all_pass)

    def delete_all_pass(self, all_pass: AllPass):
        if all_pass in self.all_pass:
            self.all_pass.remove(all_pass)

    def delete_all_passes(self):
        for all_pass in self.all_pass.copy():
            self.delete_all_pass(all_pass)

    def delete_poles(self):
        for pole in self.poles.copy():
            pole.delete()

    def delete_zeros(self):
        for zero in self.zeros.copy():
            zero.delete()

    def delete_all(self):
        self.delete_poles()
        self.delete_zeros()

    def delete_pole(self, pole: Pole):
        if pole in self.poles:
            self.poles.remove(pole)

    def delete_zero(self, zero: Zero):
        if zero in self.zeros:
            self.zeros.remove(zero)

    def get_poles(self):
        original_poles = [
            complex(pole.pos().x(), pole.pos().y()) for pole in self.poles
        ]
        all_pass_poles = [all_pass.a for all_pass in self.all_pass]

        if len(self.poles_values) == 0:
            return [*original_poles, *all_pass_poles]
        return self.poles_values

    def get_zeros(self):
        original_zeros = [
            complex(zero.pos().x(), zero.pos().y()) for zero in self.zeros
        ]
        all_pass_zeros = [1 / np.conj(all_pass.a) for all_pass in self.all_pass]

        if len(self.zeros_values) == 0:
            return [*original_zeros, *all_pass_zeros]
        return self.zeros_values

    def get_gain(self):
        return self.gain

    def get_all_pass(self):
        return self.all_pass

    def response(self):
        zeros_values = [complex(zero.pos().x(), zero.pos().y()) for zero in self.zeros]
        poles_values = [complex(pole.pos().x(), pole.pos().y()) for pole in self.poles]
        w, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))
        return w, magnitude, phase

    def all_pass_response(self):
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        w, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))
        return w, magnitude, phase
