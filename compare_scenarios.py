#!/usr/bin/env python3
"""
Scenario Comparison Script

Run multiple simulation scenarios to compare the effectiveness of different
public health interventions.
"""

from simulation import COVIDSimulation
from plotter import compare_scenarios
import time

def run_scenario(name, config, steps=500):
    """
    Run a simulation scenario with specific configuration.
    
    Args:
        name: Name of the scenario
        config: Dictionary with simulation parameters
        steps: Number of time steps to simulate
    
    Returns:
        History dictionary with simulation results
    """
    print(f"\nRunning scenario: {name}")
    print(f"  Configuration: {config}")
    
    sim = COVIDSimulation(width=800, height=600, population=200)
    
    # Apply configuration
    if 'infection_radius' in config:
        sim.infection_radius = config['infection_radius']
    if 'transmission_probability' in config:
        sim.transmission_probability = config['transmission_probability']
    if 'movement_speed' in config:
        sim.movement_speed = config['movement_speed']
    if 'lockdown' in config:
        sim.lockdown = config['lockdown']
    if 'mortality_rate' in config:
        sim.mortality_rate = config['mortality_rate']
    
    # Run simulation
    for step in range(steps):
        sim.update()
        
        if step % 100 == 0:
            stats = sim.get_statistics()
            print(f"  Step {step}: {stats['infected']} infected")
    
    print(f"  Final statistics:")
    final_stats = sim.get_statistics()
    for key, value in final_stats.items():
        print(f"    {key.capitalize()}: {value}")
    
    return sim.history


def main():
    """Compare different intervention scenarios."""
    print("=" * 70)
    print("COVID-19 Simulation - Scenario Comparison")
    print("=" * 70)
    print("\nThis script will run 4 different scenarios to compare")
    print("the effectiveness of various public health interventions.")
    print("\nScenarios:")
    print("  1. No intervention (baseline)")
    print("  2. Social distancing (reduced movement)")
    print("  3. Mask wearing (reduced infection radius)")
    print("  4. Lockdown (no movement)")
    print("\n" + "=" * 70)
    
    # Define scenarios
    scenarios = [
        {
            'name': 'No Intervention (Baseline)',
            'config': {
                'infection_radius': 20,
                'transmission_probability': 0.5,
                'movement_speed': 1.0,
                'lockdown': False,
                'mortality_rate': 0.02
            }
        },
        {
            'name': 'Social Distancing',
            'config': {
                'infection_radius': 20,
                'transmission_probability': 0.5,
                'movement_speed': 0.3,  # Reduced movement
                'lockdown': False,
                'mortality_rate': 0.02
            }
        },
        {
            'name': 'Mask Wearing',
            'config': {
                'infection_radius': 10,  # Reduced infection radius
                'transmission_probability': 0.3,  # Lower transmission
                'movement_speed': 1.0,
                'lockdown': False,
                'mortality_rate': 0.02
            }
        },
        {
            'name': 'Lockdown',
            'config': {
                'infection_radius': 20,
                'transmission_probability': 0.5,
                'movement_speed': 1.0,
                'lockdown': True,  # No movement
                'mortality_rate': 0.02
            }
        }
    ]
    
    # Run all scenarios
    results = []
    names = []
    
    for scenario in scenarios:
        history = run_scenario(scenario['name'], scenario['config'], steps=500)
        results.append(history)
        names.append(scenario['name'])
        time.sleep(0.5)  # Brief pause between scenarios
    
    # Compare results
    print("\n" + "=" * 70)
    print("Generating comparison plots...")
    compare_scenarios(results, names)
    print("\nComparison complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
