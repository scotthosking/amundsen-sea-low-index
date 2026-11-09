# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## Fixed

+ Updated test fixture csv file and default number of header lines to 34.

## 0.2.8 - 2026-09-11

### Fixed
+ Fix bug where minima falling exactly on the edge of the region box were excluded due to erroneous use of `<`/`>` vs `<=`/`>=`.

## 0.2.7 - 2026-05-28

### Added
+ Note on known issue in ERA5 May-Oct 1996 which affects the Amundsen Sea.

## 0.2.6 - 2026-05-21

### Fixed
+ Write new line in CSV after template header.

## 0.2.5 - 2026-05-21

### Fixed
+ Fixed jinja template package loder broken since package name change in 0.2.2.
+ Corrected units in csv output template from `hPA` to `hPa`.

## 0.2.4 - 2026-05-07

No changes.

## 0.2.3 - 2026-05-07

No changes.

## 0.2.2 - 2026-05-07

### Breaking Changes
+ Package name is now `bas-asli` to facilitate PyPI hosting, note that import name is still `asli`.

## 0.2.1 - 2026-05-05

### Fixed
+ Bug in `asli download --lsm`, added `-f/--filename` option to CLI.

## 0.2.0 - 2026-04-02

### Breaking changes
+ Command line interface has changed from `asli_calc` type separated program structure to one main program with subcommands, e.g. `asli calc`
  + `asli_calc` is now `asli calc`
  + `asli_data_lsm` is now `asli download --lsm`
  + `asli_data_era5` is now `asli download`
  + `asli_plot` is now `asli plot`
+ `--datadir` option for `asli calc` and `asli plot` has been removed; with the corresponding arguments in the python interface to `ASLICalculator` being removed. Data paths are now specified as full paths in order to improve user experience in the command line interface via utilising normal tab completion.
+ `filename` argument is changed to `filepath` throughout, reflecting change from specifying files relative to `data_dir`.
+ `asli.data.get_land_sea_mask` now downloads with `area=ASL_REGION` by default.
+ Substantial changes to the plotting interface, both the CLI and python API.
  + Plotting methods have been removed from the `ASLICalculator` class.
  + Python interface now implements a `asli.plot.Plotter` class to handle plotting, which takes an `ASLICalculator` instance as the sole init argument
  + `Plotter` objects have `plot_all`, `plot_year` and `plot_month` methods and return a matplotlib figure and axes.
  + `asli plot` now takes optional `--year` and `--month` options.

### Added
+ Log warning when no output file specified to `asli calc`.

## 0.1.0 - 2026-03-20
