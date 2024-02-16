"""Amundsen Sea Low detection from mean sea level pressure fields."""

# Import the asli class here for nicer namespace
from .asli import ASLICalculator

from . import data, plot, utils

from .params import CALCULATION_VERSION, ASL_REGION, SOFTWARE_VERSION
