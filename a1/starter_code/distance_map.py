"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """ Stores the distance between two cities.

    === Private Attributes ===
    _distances:
    """
    _distances: Dict[str, Dict[str, int]]

    def __init__(self) -> None:
        """Initialize a DistanceMap."""
        self._distances = {}

    def add_distance(self, city1: str, city2: str,
                     distance1: int, distance2: int = 0) -> None:
        """Store the distance from <city1> to <city2>.

        Preconditions:
        - distance1 > 0
        - If distance2 is given, then distance2 > 0
        - city1 and city2 are different cities

        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> m._distances['Toronto']
        {'Hamilton': 9}
        >>> m._distances['Toronto']['Hamilton']
        9
        >>> m._distances['Hamilton']['Toronto']
        9
        """
        if city1 in self._distances:
            self._distances[city1][city2] = distance1
        else:
            self._distances[city1] = {}
            self._distances[city1][city2] = distance1

        if distance2 == 0:
            if city2 in self._distances:
                self._distances[city2][city1] = distance1
            else:
                self._distances[city2] = {}
                self._distances[city2][city1] = distance1
        else:
            if city2 in self._distances:
                # DEPENDING ON DESIGN DECISION: see failed doctest example.
                # if city1 not in self._distances[city2]:
                #     self._distances[city2][city1] = distance1
                self._distances[city2][city1] = distance2
            else:
                self._distances[city2] = {}
                self._distances[city2][city1] = distance2

    def distance(self, city1: str, city2: str) -> int:
        """Returns the distance from <city1> to <city2>.



        Preconditions:
        - city1 and city2 are different cities

        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9, 10)
        >>> m.distance('Toronto', 'Hamilton')
        9
        >>> m.distance('Toronto', 'Ottawa')
        -1
        >>> m.distance('Hamilton', 'Toronto')
        10
        >>> m.add_distance('Hamilton', 'Toronto', 10)
        >>> m.distance('Toronto', 'Hamilton')
        10
        >>> m.distance('Hamilton', 'Toronto')
        10

        """
        if city1 in self._distances:
            if city2 in self._distances[city1]:
                return self._distances[city1][city2]
            return -1
        return -1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
