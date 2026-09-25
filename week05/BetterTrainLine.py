
from __future__ import annotations
from Station import *

class BetterTrainLine:

    def __init__(self, name: str):
        self.__name: str = name
        self.__head: Station = None
        self.__last: Station = None

    def __str__(self):
        return f"Better Train Line name: {self.__name}"

    def add(self, new_station:Station):
        if self.__head == None:
            self.__head = new_station
        else:
            self.__last.set_next(new_station)
        self.__last = new_station
