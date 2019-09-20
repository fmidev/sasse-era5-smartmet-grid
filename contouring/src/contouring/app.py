import logging
import contouring.datareader
import contouring.parser
import argparse
from types import SimpleNamespace


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

params = parser.add_argument_group('params', 'General settings for general stuff')
params.add_argument("--url", help="WFS service address", default="http://smartmet.fmi.fi/wfs")
params.add_argument("--storedquery_id", help="Name of the predefined WFS-query")
params.add_argument("--year", help="Generate WFS-requests starting this year. Ignored if starttime is given", type=int)
params.add_argument("--month", help="Generate WFS-requests starting this month. Ignored if starttime is given", type=int)
params.add_argument("--verbose", help="Set logging to show all messages", action="store_true")

params = parser.add_argument_group('Stored query settings', 'Query string fields and values.')
params.add_argument("--limits", help="Contouring high and low values, when contouring")
params.add_argument("--source", help="What type of data should be used by smartmet-server", choices=['grid', 'querydata'], default='grid')
params.add_argument("--bbox", help="Bounding box coordinates for contouring area", default='21,60,24,64')
params.add_argument("--crs", help="Coordinate system used in responses", default='EPSG:4326')
params.add_argument("--starttime", help="Begin time for requests.")
params.add_argument("--endtime", help="Last time interval for wfs request.")

args = parser.parse_args()
if not args.verbose:
    log.setLevel(logging.WARN)



def main():
    dr = contouring.datareader.Datareader(args.url)
    
    # Iterate over WFS-requests
    if args.year and args.month:
        log.debug("Iterate stuff from generated times")
    elif args.starttime:
        log.debug("Fetch user defined time frame")
    else:
        log.error("Not timeframe defined")
        msg = (
            "Define either --year and --month or "
            "--starttime (with optional --endtime)"
        )   
        parser.error(msg)

    # for starttime in dr.starttimes(args.year, args.month):

    #     # stored_query_params can be built here
    #     log.debug(f"{starttime}")
    #     log.info(f"Hommaa")

        ## Make request
        # dr.getWFS()

        ## Create orm-object

        ## Write to data base

if __name__ == '__main__':
    main()


# import asyncio
# import time
# async def count():
#     print("One")
#     await asyncio.sleep(1)
#     print("Two")
# async def main():
#     await asyncio.gather(count(), count(), count())
# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
#     import time
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")
