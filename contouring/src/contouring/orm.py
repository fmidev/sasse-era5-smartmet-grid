import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint, MetaData
from sqlalchemy import DDL
from sqlalchemy import event
from geoalchemy2 import Geometry

# Really annoying to define the schema here, and not in the app.py
# It'd be nice to figure out a way to pass it as an argument somehow.
schema_name = 'sasse'
metadata = MetaData(schema=schema_name) 
Base = declarative_base(metadata=metadata)

# Add schema to database if it's not there
event.listen(
    Base.metadata,
    'before_create',
    DDL(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
)

class StormCell(Base):
    __tablename__ = 'stormcell'
    
    id = Column(Integer, primary_key=True)
    storm_id = Column(Integer,
        doc="Referring to storm that consists of multiple storm cells",
        comment="Referring to storm that consists of multiple storm cells"
        )
    point_in_time = Column(
        DateTime(timezone=True),
        doc="Occurrance time of the weather phenomenon",
        comment="Occurrance time of the weather phenomenon"
        )
    weather_parameter = Column(
        String, 
        doc="Name of weather phenomenon",
        comment="Name of weather phenomenon"
        )
    unit = Column(String)
    low_limit = Column(Integer)
    high_limit = Column(Integer)
    geom =  Column(Geometry('POLYGON'))
    created = Column(
        DateTime(timezone=True), 
        default=datetime.datetime.utcnow
        )
    modified = Column(
        DateTime(timezone=True), 
        onupdate=datetime.datetime.utcnow
        )