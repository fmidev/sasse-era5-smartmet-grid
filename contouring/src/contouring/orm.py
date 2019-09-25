from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint
from geoalchemy2 import Geometry
import datetime

Base = declarative_base()


class Storm(Base):
    __tablename__ = 'storm'

    id = Column(Integer, primary_key=True)
    point_in_time = Column(
        DateTime(timezone=True),
        doc="Occurrance time of the weather phenomenon",
        comment="Occurrance time of the weather phenomenon"
    )
    created = Column(
        DateTime(timezone=True), 
        default=datetime.datetime.utcnow
    )
    modified = Column(
        DateTime(timezone=True), 
        onupdate=datetime.datetime.utcnow
    )
    tag = Column(
        String, 
        doc="Coverage of: {parameter}-{low_limit}-{high_limit}",
        comment="Coverage of: {parameter}-{low_limit}-{high_limit}"
    )
    geom =  Column(Geometry('MULTIPOLYGON'))
    PrimaryKeyConstraint('id', 'point_in_time', 'tag', name='storm_pk')
