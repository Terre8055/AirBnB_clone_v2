#!/usr/bin/python3
""" Amenity Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    '''Amenity class
    more like services eg WI-FI?
    '''
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary='place_amenity',
                                   viewonly=False)

    def __init__(self, *args, **kwargs):
        '''initializes Amenity'''
        super().__init__(*args, **kwargs)
