import logging
import contouring.datareader
import contouring.parser
import argparse
from types import SimpleNamespace
import datetime
import contouring.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

argparser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

params_a = argparser.add_argument_group('params', 'General settings for general stuff')
params_a.add_argument("--url", help="WFS service address", default="http://smartmet.fmi.fi/wfs")
params_a.add_argument("--storedquery_id", help="Name of the predefined WFS-query")
params_a.add_argument("--year", help="Generate WFS-requests starting this year. Ignored if starttime is given", type=int)
params_a.add_argument("--month", help="Generate WFS-requests starting this month. Ignored if starttime is given", type=int)
params_a.add_argument("--verbose", help="Set logging to show all messages", action="store_true")

params_b = argparser.add_argument_group('Stored query params', 'Direct fields and values for query string.')
params_b.add_argument("--limits", help="Contouring high and low values, when contouring")
params_b.add_argument("--source", help="What type of data should be used by smartmet-server", choices=['grid', 'querydata'], default='grid')
params_b.add_argument("--bbox", help="Bounding box coordinates for contouring area", default='21,60,24,64')
params_b.add_argument("--crs", help="Coordinate system used in responses", default='EPSG:4326')
params_b.add_argument("--starttime", help="Begin time for requests.")
params_b.add_argument("--endtime", help="Last time interval for wfs request.")

args = argparser.parse_args()
if not args.verbose:
    log.setLevel(logging.WARN)

def create_datareader():
    datareader = contouring.datareader.Datareader(args.url)
    datareader.stored_query_id = args.storedquery_id
    datareader.stored_query_params.limits = args.limits
    datareader.stored_query_params.source = args.source
    datareader.stored_query_params.bbox = args.bbox
    datareader.stored_query_params.crs = args.crs
    return datareader

def request_with_defined_times(datareader, starttime, endtime):
    log.debug(f"Fetch data with given starttime {starttime} and endtime {endtime}")
    datareader.stored_query_params.starttime = starttime
    datareader.stored_query_params.endtime = endtime
    return datareader.getWFS()


def object_to_db(parsed_data, session):
    stormcell = contouring.orm.StormCell(
        point_in_time = parsed_data['point_in_time'],
        weather_parameter = parsed_data['weather_parameter'],
        unit= parsed_data['unit'],
        low_limit = parsed_data['low_limit'],
        high_limit = parsed_data['high_limit'],
        geom = parsed_data['geometry']
    )
    log.debug(f"Schema shall be {stormcell.metadata.schema}")
    log.debug('Add object to session')
    session.add(stormcell)


def main():
    
    
    dialect = 'postgresql'
    driver = 'psycopg2'
    username = 'fminames_user'
    password = 'OmaHassuSalasana1234!'
    host = 'fminames-db'
    port = '5432'
    database = 'fminames'
    database_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(database_url, echo=True)
    
    log.debug('Create all here')
    contouring.orm.Base.metadata.create_all(engine)
    log.debug('Created all')

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    datareader = create_datareader()
    dataparser = contouring.parser.Parser()

    if args.year and args.month:
        log.debug(f"Fetch data for {args.year}/{args.month}")
        for starttime in contouring.datareader.starttimes(args.year, args.month):
            formatted_starttime = starttime.strftime("%Y-%m-%dT%H:%M:%SZ")
            results = request_with_defined_times(datareader, formatted_starttime, formatted_starttime)
            log.debug(f"Save results to database, or something...")
            data = results.read()
            parsed = dataparser.list_contours_in_wfs(data)
            try:
                object_to_db(parsed[0], session)
            except IndexError:
                pass
            else:
                log.debug(f"Commit session")
                session.commit()
    elif args.starttime:
        log.debug(f"Fetch data with given starttime {args.starttime}")
        endtime = args.endtime if args.endtime else args.starttime
        results = request_with_defined_times(datareader, args.starttime, endtime)
        data = results.read()
        log.debug(f"Save results to database, or something...")
        parsed = dataparser.list_contours_in_wfs(data)
        # log.debug(parsed)

    else:
        log.error("Not timeframe defined")
        msg = (
            "Define either --year and --month or "
            "--starttime (with optional --endtime)"
        )   
        argparser.error(msg)
        

if __name__ == '__main__':
    main()

