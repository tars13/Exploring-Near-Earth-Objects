"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import math

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info.get("designation")
        self.name = info.get("name")
        self.diameter = info.get("diameter")
        if not self.diameter:
            self.diameter = float("nan")
        self.hazardous = info.get("hazardous")

        # an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if not self.name:
            return f"{self.designation}"
        return f"{self.designation} ({self.name})"

    def __str__(self):
        """Return `str(self)`."""
       
        result = f'NEO {self.fullname} has'
        if math.isnan(self.diameter):
            result += "an unknown diameter"
        else:
            result += f" a diameter of {self.diameter:3f} km"
        if self.hazardous:
            result += " and is potentially hazardous."
        else:
            result += " and is not potentially hazardous."
        return result

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        neo_dict = dict()
        if self.name is None:
            neo_dict['name'] = ""

        else:
            neo_dict['name'] = "{name}".format(name = self.name)
        
        neo_dict['designation'] = "{designation}".format(designation = self.designation)
        neo_dict['diameter_km'] = self.diameter
        neo_dict['potentially_hazardous'] = self.hazardous

        return neo_dict


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info.get("designation")
        self.time = cd_to_datetime(info.get("time"))  
        self.distance = info.get("distance", float("nan"))
        self.velocity = info.get("velocity", float("nan"))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = info.get("neo")

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # formatted representation of the approach time.
        # a fullname for this object.
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # human-readable string representation.

        return f"On {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        appraoch_dict = dict()
        appraoch_dict['datetime_utc'] = "{dt}".format(dt = self.time_str)
        appraoch_dict['distance_au'] = self.distance
        appraoch_dict['velocity_km_s'] = self.velocity

        return appraoch_dict
