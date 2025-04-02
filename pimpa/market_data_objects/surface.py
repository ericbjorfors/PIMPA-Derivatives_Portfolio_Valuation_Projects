""" Class that implements surface interpolation

Base day counting is done in unit of days, not of years
"""

import numpy as np

from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
from sympy import interpolate
from ..utils.calendar_utils import translate_tenor_to_years


class Surface:
    def __init__(self, vol_surface) -> None:
        self.tenors = np.asarray([translate_tenor_to_years(x)
                                 for x in vol_surface.columns])
        self.strikes = np.asarray([x for x in vol_surface.index])
        self.values = vol_surface.to_numpy()
        self.interpolated_implied_vols = interp2d(
            self.tenors,
            self.strikes,
            self.values,
            kind='linear',
            bounds_error=False,
            fill_value=None)

    def get_interpolated_surface(self, K, t):
        return self.interpolated_implied_vols(t, K)

    def get_interpolated_ATM_curve(self, t):
        return self.interpolated_implied_vols(t, 1)
