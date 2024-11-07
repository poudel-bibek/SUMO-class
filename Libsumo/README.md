## Structure

```
project/
├── basic.sumocfg          # SUMO configuration file
├── intersection.net.xml   # Network definition file
├── routes.rou.xml         # Traffic routes and flows
└── traffic_control.py     # Simulation control script
```

## File Descriptions

### 1. SUMO Configuration (`basic.sumocfg`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
    <input>
        <net-file value="intersection.net.xml"/>
        <route-files value="routes.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="1000"/>
    </time>
</configuration>
```

### 2. Network Definition (`intersection.net.xml`)
This file defines a simple intersection with:
- North-South and South-North traffic lanes
- Traffic light controlled junction
- Static traffic light program with phases:
  - 31 seconds green
  - 4 seconds yellow
  - 31 seconds green (opposite direction)
  - 4 seconds yellow

### 3. Routes Configuration (`routes.rou.xml`)
Defines:
- Vehicle type (car)
- Two routes (northbound and southbound)
- Traffic flows with 0.3 probability for each direction

### 4. Simulation Control (`traffic_control.py`)
Python script that:
- Initializes the SUMO simulation
- Monitors traffic conditions
- Collects statistics about:
  - Traffic light phases
  - Queue lengths
  - Total vehicles in simulation

## Running the Simulation

1. Ensure all files are in the same directory
2. Run the simulation using Python:

```bash
python traffic_control.py
```

The script will output statistics every 10 simulation steps, including:
- Current simulation step
- Traffic light phase
- Queue lengths for north and south approaches
- Total number of vehicles in the simulation

## Understanding the Output

The simulation provides the following metrics:
- **Traffic Light Phase**: Current phase of the traffic signal (0-3)
- **North Queue**: Number of vehicles waiting in the northern approach
- **South Queue**: Number of vehicles waiting in the southern approach
- **Total Vehicles**: Total number of vehicles currently in the simulation

## Traffic Light Phases

The traffic light operates on a fixed-time cycle:
1. Phase 0: North-South green (31s)
2. Phase 1: North-South yellow (4s)
3. Phase 2: South-North green (31s)
4. Phase 4: South-North yellow (4s)

## Notes

- The simulation runs for 100 steps by default
- Vehicle flows are generated with 0.3 probability for each direction
- The network uses a simple two-way layout with one lane per direction
- Traffic light timing is static and not adaptive
