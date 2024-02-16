"""Download and organise data for ASLI calculations"""

import argparse
from datetime import datetime
import logging 
from pathlib import Path

import cdsapi

from .params import ASL_REGION

logging.getLogger('asli').addHandler(logging.NullHandler())

class CDSDownloader:
    def __init__(self, data_dir:str, request_params:dict, output_filename:str, area:dict):
        self.data_dir = data_dir
        self.request_params = request_params
        self.output_path = Path(self.data_dir, output_filename)

        if area:
            logging.info(f"Downloading with bounding area: {area}")
            self.request_params.update({'area': [area['north'],
                                        area['west'],
                                        area['south'],
                                        area['east']
                                        ]})
        else:
            logging.info(f"No bounding area specified, downloading with no bounding area, i.e. whole earth.")

    def download(self):
        c = cdsapi.Client()
        c.retrieve(
            'reanalysis-era5-single-levels-monthly-means',
            self.request_params,
            self.output_path)


def get_era5_monthly(data_dir: str, vars:list = ["msl"], start_year: int = 2006, end_year: int = 2023, area: dict = ASL_REGION, border:float=None) -> None:
    """
    Download the ERA5 monthly averaged variables from the Climate Data Store (CDS).
    Uses the CDS API and therefore requires CDS account and API key.
    Please see the CDS API documentation: https://cds.climate.copernicus.eu/api-how-to
    If running for the first time, may require agreement to CDS T&Cs per dataset. See output for details.

    Downloads may queue for a considerable time depending on the CDS.
    Request progress can be tracked through your CDS account at: https://cds.climate.copernicus.eu/cdsapp#!/yourrequests

    data_dir(str): path of data directory
    vars (Sequence[str]): list of strings specifying variables to download. Can be one or more of "msl" (default), "tas", "uas", 
        "vas" corresponding to "mean_sea_level_pressure", "2m_temperature", "10m_u_component_of_wind", and "10m_v_component_of_wind, respectively.
    start_year(int): earliest year of data to download
    start_year(int): latest year of data to download
    area(dict): either dictionary containing keys 'north', 'south', 'east', 'west' bounding coordinates of area to download (default) or None.
    """

    variables = [
        '10m_u_component_of_wind' if "uas" in vars else None,
        '10m_v_component_of_wind' if "vas" in vars else None,
        '2m_temperature' if "tas" in vars else None,
        'mean_sea_level_pressure' if "msl" in vars else None,
        ]
    variables = [e for e in variables if e is not None] # remove None values
    
    request_params = {
            'format':'netcdf',
            'product_type':'monthly_averaged_reanalysis',
            'variable': variables,
            'year': list(map(str,list(range(start_year,end_year+1,1)))),
            'month':[
                '01','02','03',
                '04','05','06',
                '07','08','09',
                '10','11','12'
            ],
            'time':'00:00',
            }
    
    data_downloader = CDSDownloader(data_dir,request_params=request_params, output_filename=f"ERA5/monthly/era5_{'_'.join(variables)}_monthly_{start_year}-{end_year}.nc", area=_get_request_area(area, border))
    data_downloader.download()


def _cli_get_era5_monthly():
    """
    CLI for get_era5_monthly, designed to be used via package entrypoint
    """
    parser = argparse.ArgumentParser(
                    prog='asli_data_era5',
                    description='Downloads the ERA5 monthly averaged data from the Climate Data Store (CDS). \
                                Uses the CDS API and therefore requires CDS account and API key. \
                                Please see the CDS API documentation: https://cds.climate.copernicus.eu/api-how-to \
                                If running for the first time, may require agreement to CDS T&Cs per dataset. See output for details. \
                                \n \
                                Downloads may queue for a considerable time depending on the CDS. \
                                Request progress can be tracked through your CDS account at: https://cds.climate.copernicus.eu/cdsapp#!/yourrequests')
    parser = _cli_data_common_args(parser)    
    parser.add_argument("-v", "--vars", nargs='?', default="msl,", help="comma-separated list of strings specifying variables to download. Can be one or more of 'msl' (default), 'tas', 'uas', \
                        'vas' corresponding to 'mean_sea_level_pressure', '2m_temperature', '10m_u_component_of_wind', and '10m_v_component_of_wind', respectively.")
    parser.add_argument("-s", "--start", default=1979, type=int, help="Earliest year to download. (Default: 1979)")
    parser.add_argument("-n", "--end", default=datetime.now().year, type=int, help=f"Latest year to download. (Default: {datetime.now().year})")

    args = parser.parse_args()

    if args.e == True:
        logging.info("'-e' flag specified. Will download whole Earth.")
        area_dict = None
    else:
        area_dict = {
            'north': args.area_bounds[0],
            'west': args.area_bounds[1],
            'south': args.area_bounds[2],
            'east': args.area_bounds[3],
        }

    vars = list(args.vars.split(","))
    logging.info(f"variables to download: {vars}")

    get_era5_monthly(data_dir=Path(args.datadir), vars=vars, start_year=args.start, end_year=args.end, area=area_dict)


def get_land_sea_mask(data_dir: str, filename:str = "era5_lsm.nc", area:dict = None, border:float = None):
    """
    Download the ERA5 land-sea mask from the Climate Data Store (CDS).
    Uses the CDS API and therefore requires CDS account and API key.
    Please see the CDS API documentation: https://cds.climate.copernicus.eu/api-how-to
    If running for the first time, may require agreement to CDS T&Cs per dataset. See output for details.

    Downloads may queue for a considerable time depending on the CDS.
    Request progress can be tracked through your CDS account at: https://cds.climate.copernicus.eu/cdsapp#!/yourrequests

    Params
    data_dir(str): path of data directory
    area(dict): either dictionary containing keys 'north', 'south', 'east', 'west' bounding coordinates of area to download (default) or None.
    """

    request_params = {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': 'land_sea_mask',
        'year': '2023',
        'month': '12',
        'time': '00:00',
        }
    
    data_downloader = CDSDownloader(data_dir,request_params=request_params, output_filename=filename, area=_get_request_area(area, border))
    data_downloader.download()

def _get_request_area(area:dict, border: float) -> dict:
    if area:
        logging.info(f"Area of N:{area['north']}, W:{area['west']}, S:{area['south']}, E:{area['east']}specified.")
        if border==None:
            request_area = area
        else:
            logging.info(f"Border of {border} specified.")
            request_area = {
                'north': area['north']+border,
                'south': area['south']-border,
                'east': area['east']+border,
                'west': area['west']-border
            }
        logging.info(f"Requesting: N:{area['north']}, W:{area['west']}, S:{area['south']}, E:{area['east']}.")
        return request_area
    else:
        return None

def _cli_get_land_sea_mask():
    """
    CLI for get_land_sea_mask, designed to be used via package entrypoint
    """

    args = _get_cli_lsm_args()
    get_land_sea_mask(data_dir=Path(args.datadir), filename=args.filename, area=args.area_dict, border=args.border)

def _get_cli_lsm_args():
    parser = argparse.ArgumentParser(
                    prog='asli_data_lsm',
                    description='Downloads the ERA5 land-sea mask from the Climate Data Store (CDS). \
                                Uses the CDS API and therefore requires CDS account and API key. \
                                Please see the CDS API documentation: https://cds.climate.copernicus.eu/api-how-to \
                                If running for the first time, may require agreement to CDS T&Cs per dataset. See output for details. \
                                \n \
                                Downloads may queue for a considerable time depending on the CDS. \
                                Request progress can be tracked through your CDS account at: https://cds.climate.copernicus.eu/cdsapp#!/yourrequests')
    parser = _cli_data_common_args(parser)
    parser.add_argument("-f", "--filename", default="era5_lsm.nc", help="Filename for data once downloaded. (Default: era5_lsm.nc)")

    args = parser.parse_args()

    if args.e == True:
        logging.info("'-e' flag specified. Will download whole Earth.")
        args.area_dict = None
        args.border = None
    else:
        args.area_dict = {
            'north': args.area[0],
            'west': args.area[1],
            'south': args.area[2],
            'east': args.area[3],
        }

    return args

def _cli_data_common_args(parser:argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Adds options that are common to the data download CLIs"""

    parser.add_argument("-d", "--datadir", default="./data", help="Path to directory in which to put downloaded data. (Default: ./data)")
    parser.add_argument("-e", action='store_true', help="Download entire earth. i.e. don't restrict to bounds specified using '-a'.")
    parser.add_argument("-a", "--area", type=float, nargs=4, default=[ASL_REGION['north'], ASL_REGION['west'], ASL_REGION['south'], ASL_REGION['east']],
                        help=f"Bounding coordinates for data download: N W S E. Optional. Overridden by '-e' option. \
                            (Default: bounds of Amundsen Sea: North: {ASL_REGION['north']}, West: {ASL_REGION['west']}, South: {ASL_REGION['south']}, East: {ASL_REGION['east']})")
    parser.add_argument("-b", "--border", type=float, nargs="?", default=0.0, help="Additional border around <area> to download in degrees")

    return parser
