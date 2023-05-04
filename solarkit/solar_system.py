from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional

from planet import Planet


@dataclass
class Solar_System:
    """
    Solar system class

    Holds the planet data
    """
    system_name: Optional[str] = field(default="Solar System")
    planets: Dict[str, Planet] = field(init=False, default_factory=dict)
    
    
    def __str__(self):
        return f"{self.system_name}({', '.join([planet_name for planet_name in self.planets])})"
    
    
    def add(self, planet: Planet, force_add: bool = False) -> None:
        """
        Add a planet to the system

        Args:
            planet (Planet): A Planet object\n
            force_add (bool): Ignore the constraint
        
        The planet's .a property must be greater than 0 for it to be added
        """
        
        if planet.a > 0 or force_add:
            self.planets[planet.name] = planet
            
    def compute_relative_vector(self, origin_planet_data: Dict[str, float], target_planet_data: Dict[str, float]) -> Dict[str, float]:
        """
        Comput the vector between two planets

        Args:
            origin_planet_data Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis, 
                    y: list of points on y-axis,
                    z: list of point on z-axis}: The position of the planet to be used as a centre\n
                    
            target_planet_data Dict: {name: planet name, 
                    c: colour,
                    x: list of points on x-axis., 
                    y: list of points on y-axis,
                    z: list of point on z-axis}: The position of the planet you want to calculate the offset with respect to the planet at the origin\n
            
            
        Returns:
            Dict: {name (str): planet name, 
                    c (str): colour,
                    x (float): list of points on x-axis., 
                    y (float): list of points on y-axis,
                    z (float): list of point on z-axis}
        """
        
        if "z" in origin_planet_data.keys() and "z" in target_planet_data.keys():
            return {"name": target_planet_data["name"],
                    "c": target_planet_data["c"],
                    "x": (target_planet_data["x"] - origin_planet_data["x"]),
                    "y": (target_planet_data["y"] - origin_planet_data["y"]),
                    "z": (target_planet_data["z"] - origin_planet_data["z"])}
        else:
            return {"name": target_planet_data["name"],
                    "c": target_planet_data["c"],
                    "x": (target_planet_data["x"] - origin_planet_data["x"]),
                    "y": (target_planet_data["y"] - origin_planet_data["y"])} 
        
