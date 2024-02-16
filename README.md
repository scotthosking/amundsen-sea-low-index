# Amundsen Sea Low Index (ASLI)

![GitHub License](https://img.shields.io/github/license/davidwilby/amundsen-sea-low-index)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdavidwilby%2Famundsen-sea-low-index%2Fpackaging%2Fpyproject.toml)
![tests](https://github.com/davidwilby/amundsen-sea-low-index/actions/workflows/tests.yml/badge.svg)

![ASL image](asl.jpg) 

The Amundsen Seas Low (ASL) is a highly dynamic and mobile climatological low pressure system located in the Pacific sector of the Southern Ocean. In this sector, variability in sea-level pressure is greater than anywhere in the Southern Hemisphere, making it challenging to isolate local fluctuations in the ASL from larger-scale shifts in atmospheric pressure. The position and strength of the ASL are crucial for understanding regional change over West Antarctica. 

This repository contains a python package (`asli`) which implements the ASL calculation methods described in [Hosking *et al.* (2016)](http://dx.doi.org/10.1002/2015GL067143), as well as notebooks illustrating its usage.

More information can be found [here](https://scotthosking.com/asl_index)

If using the `asli` package please cite both this repository (see "Cite this repository" at the top right on GitHub), as well as the original paper, e.g.

> Hosking, J. S., A. Orr, T. J. Bracegirdle, and J. Turner (2016), Future circulation changes off West Antarctica: Sensitivity of the Amundsen Sea Low to projected anthropogenic forcing, Geophys. Res. Lett., 43, 367–376, doi:10.1002/2015GL067143. 

> Hosking, J. S., & Wilby, D. asli [Computer software]. https://github.com/scotthosking/amundsen-sea-low-index

## Usage

### Installation

Using pip: `pip install git+https://github.com/scotthosking/amundsen-sea-low-index`
