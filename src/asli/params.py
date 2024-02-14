from types import MappingProxyType

"""
Parameters used by all modules
"""

# Version of the calculation method (*NOT* the package version)
CALCULATION_VERSION = "3.20210820"

# Bounds of the Amundsen Sea region
ASL_REGION = MappingProxyType({
    'west':170.0,
    'east':298.0,
    'south':-80.0,
    'north':-60.0
    })

# Theshold for land-sea mask percentage land per pixel
MASK_THRESHOLD = 0.5

