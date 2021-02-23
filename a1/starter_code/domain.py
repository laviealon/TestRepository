"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """ A parcel to be delivered.

    === Public Attributes ===
    _id: the parcel's unique id number.
    vol: the volume of the parcel.
    source: the parcel's source city.
    dest: the parcel's destination city.

    === Representation Invariants ===
    - A parcel's volume is a positive integer greater than 0.
    - A parcel's source and dest are both valid cities.
    - No two parcel's have the same id number.
    """
    id: int
    vol: int
    source: str
    dest: str

    def __init__(self, unique_id: int,
                 vol: int, source: str, dest: str) -> None:
        self.id = unique_id
        self.vol = vol
        self.source = source
        self.dest = dest


class Truck:
    """ A truck for making deliveries.

    === Public Attributes ===
    capacity: the volume of the truck's cargo compartment.
    route: the truck's delivery route.
    parcels: the parcels packed in the truck.
    _id: the truck's unique id number.

    === Representation Invariants ===
    - A truck's capacity is a positive integer greater than 0.
    - A truck's route is made up of valid cities.
    - No two trucks have the same id number.
    - The total volume of parcels packed in a truck is
        less than its capacity.
    """
    id: int
    capacity: int
    route: List[str]
    parcels: List[Parcel]

    def __init__(self, unique_id: int, capacity: int, depot: str) -> None:
        """Initializes a truck."""
        self.id = unique_id
        self.capacity = capacity
        self.parcels = []
        self.route = [depot]

    def stored_vol(self) -> int:
        """Returns the total volume of items stored in the truck."""
        t = 0
        for parcel in self.parcels:
            t += parcel.vol
        return t

    def pack(self, parcel: Parcel) -> bool:
        """Pack a parcel into the truck and return True if there is enough
        space for the parcel; do nothing and return False if there isn't
        space for the parcel.
        """
        if parcel.vol + self.stored_vol() <= self.capacity:
            self.parcels.append(parcel)
            self.route.append(parcel.dest)
            return True
        return False

    def fullness(self) -> float:
        """Returns the percentage of the capacity the total volume
        of items stored the truck takes up."""
        percentage = 100 * (self.stored_vol() / self.capacity)
        return round(percentage, 1)

    def is_empty(self) -> bool:
        """Returns True if the truck is empty, and False
        if the truck is not empty.
        """
        return len(self.parcels) == 0


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet.
        """
        string = ''
        for truck in self.trucks:
            string += f'{str(truck)}\n'
        return string

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        count = 0
        for truck in self.trucks:
            if not truck.is_empty():
                count += 1
        return count

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        d = {}
        for truck in self.trucks:
            d[truck.id] = []
            for parcel in truck.parcels:
                d[truck.id].append(parcel.id)
        return d

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        s = 0
        for truck in self.trucks:
            if not truck.is_empty():
                s += truck.capacity - truck.stored_vol()
        return s

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        s = 0
        for truck in self.trucks:
            if not truck.is_empty():
                s += truck.fullness()
        return s

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        fullness_values = []
        for truck in self.trucks:
            if not truck.is_empty():
                fullness_values.append(truck.fullness())
        avg_fullness = sum(fullness_values) / self.num_nonempty_trucks()
        return round(avg_fullness, 1)

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        s = 0
        for truck in self.trucks:
            # Make sure the truck has more than just the depot in its route
            if len(truck.route) > 1:
                # Loop through all cities in route
                for i in range(len(truck.route[1:])):
                    start_city = truck.route[i-1]
                    end_city = truck.route[i]
                    # Make sure distance is stored
                    s += dmap.distance(start_city, end_city)
                # Add distance from final city to depot.
                s += dmap.distance(truck.route[-1], truck.route[0])
        return s

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        avg_distances = []
        num_trucks = 0
        for truck in self.trucks:
            # Make sure the truck has more than just the depot in its route
            if len(truck.route) > 1:
                s = 0
                # Loop through all cities in route
                for i in range(len(truck.route[1:])):
                    start_city = truck.route[i-1]
                    end_city = truck.route[i]
                    # Make sure distance is stored
                    s += dmap.distance(start_city, end_city)
                # Add distance from final city to depot
                s += dmap.distance(truck.route[-1], truck.route[0])
                avg_distances.append(s)
                num_trucks += 1
        avg = sum(avg_distances) / num_trucks
        return round(avg, 2)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
