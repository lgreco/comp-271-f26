from __future__ import annotations
from Station import *

class Trainline:

    def __init__(self, name: str):
        self.__name: str = name
        self.__head: Station = None

    def __str__(self):
        return f"Trainline name: {self.__name}"

    def add(self, new_station: Station):
        if self.__head is None:
            # Trainline is empty and this new stations
            # becomes the head of the trainline
            self.__head = new_station
        else:
            # Ok, there are stations in the line, we
            # have to find the last one.
            last_station: Station = self.__head
            while last_station.has_next():
                last_station = last_station.get_name()
            # At the end of the loop, the traveler is at
            # the last station.
            last_station.set_next(new_station)