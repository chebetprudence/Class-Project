import numpy as np
import random

class Person:
    """Represents an individual in the simulation with position, state, and movement."""
    
    # State constants
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    DECEASED = 3
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Velocity for random movement
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        
        # Health state
        self.state = Person.SUSCEPTIBLE
        self.infection_time = 0
        self.infection_duration = 0
        
    def update_position(self, speed_factor=1.0):
        """Update position based on velocity with random walk."""
        if self.state == Person.DECEASED:
            return  # Dead people don't move
            
        # Random walk with some inertia
        self.vx += random.uniform(-0.3, 0.3)
        self.vy += random.uniform(-0.3, 0.3)
        
        # Limit velocity
        speed = np.sqrt(self.vx**2 + self.vy**2)
        if speed > 2:
            self.vx = (self.vx / speed) * 2
            self.vy = (self.vy / speed) * 2
        
        # Update position with speed factor (for social distancing)
        self.x += self.vx * speed_factor
        self.y += self.vy * speed_factor
        
        # Bounce off walls
        if self.x <= 0 or self.x >= self.width:
            self.vx *= -1
            self.x = max(0, min(self.width, self.x))
        if self.y <= 0 or self.y >= self.height:
            self.vy *= -1
            self.y = max(0, min(self.height, self.y))
    
    def distance_to(self, other):
        """Calculate distance to another person."""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def infect(self, recovery_time):
        """Infect this person."""
        if self.state == Person.SUSCEPTIBLE:
            self.state = Person.INFECTED
            self.infection_time = 0
            self.infection_duration = recovery_time + random.randint(-20, 20)
    
    def update_infection(self, mortality_rate):
        """Update infection status based on time."""
        if self.state == Person.INFECTED:
            self.infection_time += 1
            
            if self.infection_time >= self.infection_duration:
                # Either recover or die
                if random.random() < mortality_rate:
                    self.state = Person.DECEASED
                else:
                    self.state = Person.RECOVERED


class COVIDSimulation:
    """Main simulation class managing all people and infection dynamics."""
    
    def __init__(self, width=800, height=600, population=200):
        self.width = width
        self.height = height
        self.population_size = population
        
        # Simulation parameters
        self.infection_radius = 20
        self.transmission_probability = 0.5
        self.recovery_time = 200  # frames
        self.mortality_rate = 0.02
        self.movement_speed = 1.0
        self.lockdown = False
        
        # People in simulation
        self.people = []
        self.transmission_events = []  # Store recent transmission events for visualization
        
        # Statistics
        self.time_step = 0
        self.history = {
            'susceptible': [],
            'infected': [],
            'recovered': [],
            'deceased': []
        }
        
        self.initialize_population()
    
    def initialize_population(self):
        """Create initial population with one infected person."""
        self.people = []
        self.time_step = 0
        self.transmission_events = []
        self.history = {
            'susceptible': [],
            'infected': [],
            'recovered': [],
            'deceased': []
        }
        
        for i in range(self.population_size):
            x = random.uniform(50, self.width - 50)
            y = random.uniform(50, self.height - 50)
            person = Person(x, y, self.width, self.height)
            self.people.append(person)
        
        # Infect patient zero
        if self.people:
            self.people[0].infect(self.recovery_time)
    
    def update(self):
        """Update simulation by one time step."""
        self.time_step += 1
        self.transmission_events = []
        
        # Move people
        speed = 0 if self.lockdown else self.movement_speed
        for person in self.people:
            person.update_position(speed)
        
        # Check for infections
        infected_people = [p for p in self.people if p.state == Person.INFECTED]
        susceptible_people = [p for p in self.people if p.state == Person.SUSCEPTIBLE]
        
        for infected in infected_people:
            for susceptible in susceptible_people:
                distance = infected.distance_to(susceptible)
                
                if distance <= self.infection_radius:
                    if random.random() < self.transmission_probability:
                        susceptible.infect(self.recovery_time)
                        # Record transmission event for visualization
                        self.transmission_events.append((infected, susceptible))
        
        # Update infection status
        for person in self.people:
            person.update_infection(self.mortality_rate)
        
        # Record statistics
        self.record_statistics()
    
    def record_statistics(self):
        """Record current statistics for graphing."""
        stats = self.get_statistics()
        self.history['susceptible'].append(stats['susceptible'])
        self.history['infected'].append(stats['infected'])
        self.history['recovered'].append(stats['recovered'])
        self.history['deceased'].append(stats['deceased'])
    
    def get_statistics(self):
        """Get current population statistics."""
        stats = {
            'susceptible': 0,
            'infected': 0,
            'recovered': 0,
            'deceased': 0
        }
        
        for person in self.people:
            if person.state == Person.SUSCEPTIBLE:
                stats['susceptible'] += 1
            elif person.state == Person.INFECTED:
                stats['infected'] += 1
            elif person.state == Person.RECOVERED:
                stats['recovered'] += 1
            elif person.state == Person.DECEASED:
                stats['deceased'] += 1
        
        return stats
    
    def set_infection_radius(self, radius):
        """Set infection radius (for mask intervention)."""
        self.infection_radius = radius
    
    def set_movement_speed(self, speed):
        """Set movement speed (for social distancing)."""
        self.movement_speed = speed
    
    def set_lockdown(self, active):
        """Enable/disable lockdown."""
        self.lockdown = active
    
    def set_transmission_probability(self, prob):
        """Set transmission probability."""
        self.transmission_probability = prob
    
    def set_mortality_rate(self, rate):
        """Set mortality rate."""
        self.mortality_rate = rate
