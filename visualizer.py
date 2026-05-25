import pygame
import sys
from simulation import COVIDSimulation, Person

class SimulationVisualizer:
    """Handles visualization and user interface for the COVID simulation."""
    
    # Colors
    COLOR_SUSCEPTIBLE = (100, 149, 237)  # Blue
    COLOR_INFECTED = (220, 20, 60)       # Red
    COLOR_RECOVERED = (50, 205, 50)      # Green
    COLOR_DECEASED = (30, 30, 30)        # Black
    COLOR_TRANSMISSION = (255, 140, 0)   # Orange
    COLOR_BG = (245, 245, 245)           # Light gray
    COLOR_UI_BG = (255, 255, 255)        # White
    COLOR_TEXT = (50, 50, 50)            # Dark gray
    COLOR_BUTTON = (70, 130, 180)        # Steel blue
    
    def __init__(self, width=1200, height=700):
        pygame.init()
        
        self.width = width
        self.height = height
        self.sim_width = 800
        self.sim_height = 600
        self.ui_width = width - self.sim_width
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("COVID-19 Spread Simulation")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Initialize simulation
        self.simulation = COVIDSimulation(self.sim_width, self.sim_height, population=200)
        
        # UI elements
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Buttons and sliders
        self.buttons = {}
        self.sliders = {}
        self.setup_ui()
        
        # Animation state
        self.running = True
        self.paused = False
        self.transmission_fade = []  # List of (person1, person2, alpha) for fading lines
    
    def setup_ui(self):
        """Set up UI controls."""
        ui_x = self.sim_width + 20
        y_offset = 20
        
        # Buttons
        self.buttons['reset'] = {
            'rect': pygame.Rect(ui_x, y_offset, 150, 40),
            'text': 'Reset',
            'action': self.reset_simulation
        }
        y_offset += 60
        
        self.buttons['pause'] = {
            'rect': pygame.Rect(ui_x, y_offset, 150, 40),
            'text': 'Pause',
            'action': self.toggle_pause
        }
        y_offset += 60
        
        self.buttons['lockdown'] = {
            'rect': pygame.Rect(ui_x, y_offset, 150, 40),
            'text': 'Lockdown: OFF',
            'action': self.toggle_lockdown,
            'state': False
        }
        y_offset += 80
        
        # Sliders
        slider_width = 150
        slider_height = 20
        
        self.sliders['infection_radius'] = {
            'rect': pygame.Rect(ui_x, y_offset, slider_width, slider_height),
            'label': 'Infection Radius',
            'value': 20,
            'min': 5,
            'max': 50,
            'dragging': False
        }
        y_offset += 60
        
        self.sliders['transmission_prob'] = {
            'rect': pygame.Rect(ui_x, y_offset, slider_width, slider_height),
            'label': 'Transmission Rate',
            'value': 0.5,
            'min': 0.0,
            'max': 1.0,
            'dragging': False
        }
        y_offset += 60
        
        self.sliders['movement_speed'] = {
            'rect': pygame.Rect(ui_x, y_offset, slider_width, slider_height),
            'label': 'Movement Speed',
            'value': 1.0,
            'min': 0.0,
            'max': 2.0,
            'dragging': False
        }
        y_offset += 60
        
        self.sliders['mortality_rate'] = {
            'rect': pygame.Rect(ui_x, y_offset, slider_width, slider_height),
            'label': 'Mortality Rate',
            'value': 0.02,
            'min': 0.0,
            'max': 0.1,
            'dragging': False
        }
    
    def reset_simulation(self):
        """Reset the simulation."""
        self.simulation.initialize_population()
        self.transmission_fade = []
    
    def toggle_pause(self):
        """Toggle pause state."""
        self.paused = not self.paused
        self.buttons['pause']['text'] = 'Resume' if self.paused else 'Pause'
    
    def toggle_lockdown(self):
        """Toggle lockdown state."""
        current = self.buttons['lockdown']['state']
        self.buttons['lockdown']['state'] = not current
        self.simulation.set_lockdown(not current)
        self.buttons['lockdown']['text'] = 'Lockdown: ON' if not current else 'Lockdown: OFF'
    
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check button clicks
                for button in self.buttons.values():
                    if button['rect'].collidepoint(mouse_pos):
                        button['action']()
                
                # Check slider clicks
                for slider in self.sliders.values():
                    if slider['rect'].collidepoint(mouse_pos):
                        slider['dragging'] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Release all sliders
                for slider in self.sliders.values():
                    slider['dragging'] = False
            
            elif event.type == pygame.MOUSEMOTION:
                # Update slider values if dragging
                mouse_pos = event.pos
                for name, slider in self.sliders.items():
                    if slider['dragging']:
                        # Calculate new value based on mouse position
                        rel_x = mouse_pos[0] - slider['rect'].x
                        rel_x = max(0, min(slider['rect'].width, rel_x))
                        normalized = rel_x / slider['rect'].width
                        new_value = slider['min'] + normalized * (slider['max'] - slider['min'])
                        slider['value'] = new_value
                        
                        # Update simulation parameters
                        if name == 'infection_radius':
                            self.simulation.set_infection_radius(new_value)
                        elif name == 'transmission_prob':
                            self.simulation.set_transmission_probability(new_value)
                        elif name == 'movement_speed':
                            self.simulation.set_movement_speed(new_value)
                        elif name == 'mortality_rate':
                            self.simulation.set_mortality_rate(new_value)
    
    def draw_simulation(self):
        """Draw the main simulation area."""
        # Draw background
        pygame.draw.rect(self.screen, self.COLOR_BG, (0, 0, self.sim_width, self.sim_height))
        
        # Draw transmission lines (fading)
        new_fade = []
        for person1, person2, alpha in self.transmission_fade:
            if alpha > 0:
                color = (*self.COLOR_TRANSMISSION, int(alpha))
                surf = pygame.Surface((self.sim_width, self.sim_height), pygame.SRCALPHA)
                pygame.draw.line(surf, color, 
                               (int(person1.x), int(person1.y)), 
                               (int(person2.x), int(person2.y)), 3)
                self.screen.blit(surf, (0, 0))
                new_fade.append((person1, person2, alpha - 5))
        self.transmission_fade = new_fade
        
        # Add new transmission events
        for person1, person2 in self.simulation.transmission_events:
            self.transmission_fade.append((person1, person2, 255))
        
        # Draw people
        for person in self.simulation.people:
            # Determine color based on state
            if person.state == Person.SUSCEPTIBLE:
                color = self.COLOR_SUSCEPTIBLE
            elif person.state == Person.INFECTED:
                color = self.COLOR_INFECTED
            elif person.state == Person.RECOVERED:
                color = self.COLOR_RECOVERED
            else:  # DECEASED
                color = self.COLOR_DECEASED
            
            # Draw person as circle
            pygame.draw.circle(self.screen, color, 
                             (int(person.x), int(person.y)), 5)
    
    def draw_ui(self):
        """Draw the UI panel."""
        # Draw UI background
        pygame.draw.rect(self.screen, self.COLOR_UI_BG, 
                        (self.sim_width, 0, self.ui_width, self.height))
        
        # Draw title
        title = self.font.render("Controls", True, self.COLOR_TEXT)
        self.screen.blit(title, (self.sim_width + 20, 10))
        
        # Draw buttons
        for button in self.buttons.values():
            pygame.draw.rect(self.screen, self.COLOR_BUTTON, button['rect'], border_radius=5)
            text = self.small_font.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        # Draw sliders
        for slider in self.sliders.values():
            # Label
            label = self.small_font.render(slider['label'], True, self.COLOR_TEXT)
            self.screen.blit(label, (slider['rect'].x, slider['rect'].y - 25))
            
            # Slider track
            pygame.draw.rect(self.screen, (200, 200, 200), slider['rect'], border_radius=3)
            
            # Slider fill
            normalized = (slider['value'] - slider['min']) / (slider['max'] - slider['min'])
            fill_width = int(slider['rect'].width * normalized)
            fill_rect = pygame.Rect(slider['rect'].x, slider['rect'].y, 
                                   fill_width, slider['rect'].height)
            pygame.draw.rect(self.screen, self.COLOR_BUTTON, fill_rect, border_radius=3)
            
            # Value text
            value_text = self.small_font.render(f"{slider['value']:.2f}", True, self.COLOR_TEXT)
            self.screen.blit(value_text, (slider['rect'].x + slider['rect'].width + 10, 
                                         slider['rect'].y))
        
        # Draw statistics
        stats = self.simulation.get_statistics()
        stats_y = 500
        
        stats_title = self.font.render("Statistics", True, self.COLOR_TEXT)
        self.screen.blit(stats_title, (self.sim_width + 20, stats_y))
        stats_y += 40
        
        stat_items = [
            (f"Susceptible: {stats['susceptible']}", self.COLOR_SUSCEPTIBLE),
            (f"Infected: {stats['infected']}", self.COLOR_INFECTED),
            (f"Recovered: {stats['recovered']}", self.COLOR_RECOVERED),
            (f"Deceased: {stats['deceased']}", self.COLOR_DECEASED),
        ]
        
        for text, color in stat_items:
            rendered = self.small_font.render(text, True, color)
            self.screen.blit(rendered, (self.sim_width + 30, stats_y))
            stats_y += 30
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            
            if not self.paused:
                self.simulation.update()
            
            # Clear screen
            self.screen.fill((255, 255, 255))
            
            # Draw everything
            self.draw_simulation()
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    visualizer = SimulationVisualizer()
    visualizer.run()
