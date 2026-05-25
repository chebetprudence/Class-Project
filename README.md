# COVID-19 Spread Simulation

An agent-based SIR model that simulates airborne disease spread across a population, built as a Scientific Computing class project. The simulation runs in real-time with interactive controls and supports scenario comparison across different public health interventions.

---

## Features

- Real-time visual simulation using Pygame
- Interactive controls: adjust infection radius, transmission rate, movement speed, and mortality rate on the fly
- Lockdown, social distancing, and mask-wearing intervention modes
- SIR curve plotting (Susceptible, Infected, Recovered, Deceased)
- Scenario comparison tool to evaluate the effectiveness of different interventions

---

## Project Structure

```
├── main.py              # Entry point for the interactive simulation
├── simulation.py        # Core SIR model and agent logic
├── visualizer.py        # Pygame-based real-time visualization
├── plotter.py           # Matplotlib SIR curve and scenario plots
├── compare_scenarios.py # Runs and compares multiple intervention scenarios
```

---

## Getting Started

### Prerequisites

```bash
pip install pygame matplotlib numpy
```

### Run the interactive simulation

```bash
python main.py
```

### Run scenario comparison

```bash
python compare_scenarios.py
```

---

## Controls (Interactive Mode)

| Control | Description |
|---|---|
| Reset | Restart the simulation |
| Pause / Resume | Pause or resume the simulation |
| Lockdown | Toggle movement on/off |
| Infection Radius slider | Simulates mask wearing |
| Movement Speed slider | Simulates social distancing |
| Transmission Rate slider | Adjust how easily the disease spreads |
| Mortality Rate slider | Adjust the death rate |

## Color Coding

| Color | Meaning |
|---|---|
| 🔵 Blue | Susceptible (healthy) |
| 🔴 Red | Infected |
| 🟢 Green | Recovered |
| ⚫ Black | Deceased |
| 🟠 Orange lines | Transmission events |

---

## Scenarios Compared

The `compare_scenarios.py` script runs four scenarios:

1. **No Intervention** — baseline with default parameters
2. **Social Distancing** — reduced movement speed
3. **Mask Wearing** — reduced infection radius and transmission probability
4. **Lockdown** — all movement stopped

---

## Built With

- Python 3
- Pygame — real-time simulation rendering
- Matplotlib — statistical plots
- NumPy — numerical computations

---

## Course

Scientific Computing — Class Project