import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class StatisticsPlotter:
    """Plots SIR curves and statistics from the simulation."""
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig, self.axes = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.suptitle('COVID-19 Simulation Statistics', fontsize=16)
    
    def plot_sir_curves(self):
        """Plot the SIR curves over time."""
        ax = self.axes[0]
        ax.clear()
        
        time_steps = range(len(self.simulation.history['susceptible']))
        
        ax.plot(time_steps, self.simulation.history['susceptible'], 
                label='Susceptible', color='blue', linewidth=2)
        ax.plot(time_steps, self.simulation.history['infected'], 
                label='Infected', color='red', linewidth=2)
        ax.plot(time_steps, self.simulation.history['recovered'], 
                label='Recovered', color='green', linewidth=2)
        ax.plot(time_steps, self.simulation.history['deceased'], 
                label='Deceased', color='black', linewidth=2)
        
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Number of People')
        ax.set_title('SIR Model - Population Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_infection_rate(self):
        """Plot the infection rate over time."""
        ax = self.axes[1]
        ax.clear()
        
        if len(self.simulation.history['infected']) > 1:
            time_steps = range(len(self.simulation.history['infected']))
            infection_rate = self.simulation.history['infected']
            
            ax.plot(time_steps, infection_rate, color='red', linewidth=2)
            ax.fill_between(time_steps, infection_rate, alpha=0.3, color='red')
            
            ax.set_xlabel('Time Steps')
            ax.set_ylabel('Number of Infected')
            ax.set_title('Active Infections Over Time')
            ax.grid(True, alpha=0.3)
    
    def update_plots(self):
        """Update all plots with current data."""
        self.plot_sir_curves()
        self.plot_infection_rate()
        plt.tight_layout()
    
    def show_live(self):
        """Show live updating plots."""
        def update(frame):
            self.update_plots()
        
        ani = FuncAnimation(self.fig, update, interval=100, cache_frame_data=False)
        plt.show()
    
    def save_final_plot(self, filename='simulation_results.png'):
        """Save the final plot to a file."""
        self.update_plots()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {filename}")


def compare_scenarios(scenarios_data, scenario_names):
    """
    Compare multiple simulation scenarios side by side.
    
    Args:
        scenarios_data: List of history dictionaries from different simulations
        scenario_names: List of names for each scenario
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Comparison of Different Intervention Scenarios', fontsize=16)
    
    colors = ['blue', 'red', 'green', 'black']
    labels = ['Susceptible', 'Infected', 'Recovered', 'Deceased']
    states = ['susceptible', 'infected', 'recovered', 'deceased']
    
    # Plot each scenario
    for idx, (data, name) in enumerate(zip(scenarios_data, scenario_names)):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        
        time_steps = range(len(data['susceptible']))
        
        for state, color, label in zip(states, colors, labels):
            ax.plot(time_steps, data[state], label=label, color=color, linewidth=2)
        
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Number of People')
        ax.set_title(name)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('scenario_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Comparison plot saved to scenario_comparison.png")
