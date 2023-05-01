from dataclasses import dataclass, field
from typing import Optional, List, Dict

import matplotlib.pyplot as plt

from solar_system import Solar_System
from utils import load_system

@dataclass
class Viewer:
    """
    Visualise (& more) a Solar_System object

    Args:
        system (Solar_System): A Solar_System object\n
        planets_to_use (List[str]): Select speficif planets (leave blank for all)\n
        compute_3D (bool): Show in 3D\n
        target_fps (int): Animation's fps, might be lower if system not powerful enough\n
    """
    system: Solar_System
    planets_to_use: List[str] = field(default_factory=list)
    compute_3D: Optional[bool] = field(default= False)
    target_fps: Optional[int] = field(default=30)
    
    orbit_data: Dict[str, Dict[str, List[float]]] = field(init=False, default_factory=dict)
    
    fig: plt.figure = field(init=False)
    ax: plt.Axes = field(init=False)
    
    tmax: float = field(init=False)
    dt: float = field(init=False)
    t: float = field(init=False, default=0)
    
    
    
    
    def __post_init__(self):
        
        if not self.planets_to_use:
            self.planets_to_use = list(self.system.planets.keys())
        
        self.system.planets = dict(sorted(self.system.planets.items(), key=lambda planet: planet[1].P))
        self.orbit_data = [planet.compute_orbit(compute_3D=self.compute_3D) for planet in list(map(self.system.planets.get, self.planets_to_use))]

        self.tmax = 4 * list(map(self.system.planets.get, self.planets_to_use))[-1].P
        self.dt = self.tmax/2500
        
        if self.compute_3D:
            self.fig: plt.figure = plt.figure()
            self.ax: plt.Axes = self.fig.add_subplot(projection='3d')
            self.ax.view_init(None, 225)
          
        else:
            self.fig, self.ax = plt.subplots()
            
            #set aspect ratio to 1
            RATIO = 1.0
            x_left, x_right = self.ax.get_xlim()
            y_low, y_high = self.ax.get_ylim()
            self.ax.set_aspect(abs((x_right - x_left)/(y_low - y_high)) * RATIO)
    
    def __str__(self) -> str:
        return f"Planets: {self.system.__str__()}\n3D: {self.compute_3D}\nAnimation FPS: {self.target_fps}"
        
        
        
    def plot_orbit(self, orbit_data: Dict[str, List[float]]) -> None:
        """
        Plots the orbit of a planet

        Args:
            orbit_data (Dict): Dictionary containing orbit data (planet name, x, y, z)\n
            ax (plt.Axes): Axes to draw the orbit on\n
            
        Returns:
            plt.Axes: Axes with new orbit drawn on
                    
        """
        
        if "z" in orbit_data:
            # Draw 3D
            self.ax.plot(orbit_data["x"], orbit_data["y"], orbit_data["z"], label=f"{orbit_data['name']}'s orbit")
        else:
            # Draw 2D
            self.ax.plot(orbit_data["x"], orbit_data["y"], label=f"{orbit_data['name']}'s orbit")
            
    def plot_planet(self, planet_data: Dict[str, float]) -> None:
        """
        Plots a planet on self.ax               
        """
        if "z" in planet_data.keys():
            # Draw 3D
            self.ax.scatter(planet_data["x"], planet_data["y"], planet_data["z"], label=planet_data["name"], s=25)
        else:
            # Draw 2D
            self.ax.scatter(planet_data["x"], planet_data["y"], label=planet_data["name"], s=25)
             
    def plot_sun(self) -> None:
        """
        Draw Sun on axes on self.ax
        """

        if self.compute_3D:
            self.ax.scatter(0, 0, 0, s=100, label="Sun", c="y")
            
        else:
            self.ax.scatter(0, 0, s=100, label="Sun", c="y")
            
    def show_orbits(self) -> None:
        """
        Show the orbits of the selected planets
        """
        self.plot_sun()
        
        for planet_orbit_data in self.orbit_data:
            self.plot_orbit(orbit_data=planet_orbit_data)  
        
        plt.title("Planet orbits")
        self.ax.set_xlabel('x (AU)')
        self.ax.set_ylabel('y (AU)')
        if self.compute_3D:
            self.ax.set_zlabel('z (AU)')
            
        plt.legend()
        plt.grid()
        plt.show()
            
    def animate_orbits(self) -> None:
        """
        Animate the orbits of the selected planets
        """
        while self.t < self.tmax:
            self.plot_sun()
            
            for planet_orbit_data in self.orbit_data:
                self.plot_orbit(orbit_data=planet_orbit_data)    

            planet_data = [planet.compute_position(compute_3D=self.compute_3D, t=self.t) for planet in list(map(self.system.planets.get, self.planets_to_use))]
            for planet_planet_data in planet_data:
                self.plot_planet(planet_data=planet_planet_data)

            self.t += self.dt
        
            plt.title("Planet orbits")
            self.ax.set_xlabel('x (AU)')
            self.ax.set_ylabel('y (AU)')
            
            if self.compute_3D:
                self.ax.set_zlabel('z (AU)')
            
            plt.legend()
            plt.grid()
            plt.pause(1/self.target_fps)
            plt.cla()