#!/usr/bin/env python3
"""
COVID-19 Spread Simulation
A visual, interactive model showing how diseases propagate in a population.

This simulation uses a modified SIR (Susceptible-Infected-Recovered) model
adapted for visual representation with agent-based modeling.
"""

from visualizer import SimulationVisualizer

def main():
    """Run the COVID-19 simulation."""
    print("=" * 60)
    print("COVID-19 Spread Simulation")
    print("=" * 60)
    print("\nStarting interactive simulation...")
    print("\nControls:")
    print("  - Reset: Restart the simulation")
    print("  - Pause/Resume: Pause or resume the simulation")
    print("  - Lockdown: Stop all movement (simulates lockdown)")
    print("  - Sliders: Adjust parameters in real-time")
    print("\nColor coding:")
    print("  - Blue dots: Susceptible (healthy)")
    print("  - Red dots: Infected")
    print("  - Green dots: Recovered")
    print("  - Black dots: Deceased")
    print("  - Orange lines: Transmission events")
    print("\n" + "=" * 60)
    
    visualizer = SimulationVisualizer()
    visualizer.run()

if __name__ == "__main__":
    main()
