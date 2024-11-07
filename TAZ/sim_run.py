import os
import sys
import traci
import time
import xml.etree.ElementTree as ET

# Ensure SUMO_HOME is set and add tools to the system path
if 'SUMO_HOME' in os.environ:
    sumo_tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(sumo_tools)
else:
    sys.exit("Please declare the 'SUMO_HOME' environment variable.")

def parse_taz_definitions(taz_file):
    # Parse the TAZ definitions to create a mapping of edges to TAZ IDs
    edge_to_taz = {}
    tree = ET.parse(taz_file)
    root = tree.getroot()
    for taz in root.findall('taz'):
        taz_id = taz.get('id')
        # Get edges directly associated with the TAZ
        edges_attr = taz.get('edges')
        if edges_attr:
            edges = edges_attr.strip().split()
            for edge_id in edges:
                edge_to_taz[edge_id] = taz_id
        # Get edges from tazSource elements
        for taz_source in taz.findall('tazSource'):
            edges_attr = taz_source.get('edges')
            if edges_attr:
                edges = edges_attr.strip().split()
                for edge_id in edges:
                    edge_to_taz[edge_id] = taz_id
        # Get edges from tazSink elements
        for taz_sink in taz.findall('tazSink'):
            edges_attr = taz_sink.get('edges')
            if edges_attr:
                edges = edges_attr.strip().split()
                for edge_id in edges:
                    edge_to_taz[edge_id] = taz_id
    return edge_to_taz

def run_simulation():
    # Parse the TAZ definitions
    taz_file = 'taz.add.xml'
    edge_to_taz = parse_taz_definitions(taz_file)

    # Get the list of TAZ IDs
    taz_list = list(set(edge_to_taz.values()))

    # Dictionary to store vehicle counts between TAZ pairs
    taz_vehicle_counts = {}  # Key: (from_taz, to_taz), Value: vehicle count
    vehicle_taz = {}  # Key: veh_id, Value: (from_taz, to_taz)

    # Initialize counts for TAZ pairs
    for from_taz in taz_list:
        for to_taz in taz_list:
            if from_taz != to_taz:
                taz_vehicle_counts[(from_taz, to_taz)] = 0

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # Get the list of departed vehicles
        departed_vehicles = traci.simulation.getDepartedIDList()
        for veh_id in departed_vehicles:
            # Retrieve vehicle's route
            route_edges = traci.vehicle.getRoute(veh_id)
            # Get from and to edges
            from_edge = route_edges[0]
            to_edge = route_edges[-1]

            # Determine the TAZs associated with the edges
            from_taz = edge_to_taz.get(from_edge)
            to_taz = edge_to_taz.get(to_edge)

            if from_taz and to_taz:
                vehicle_taz[veh_id] = (from_taz, to_taz)
                # Increment count if it's a valid TAZ pair
                if from_taz != to_taz:
                    taz_vehicle_counts[(from_taz, to_taz)] += 1
        time.sleep(1)
        step += 1

    traci.close()

    # Print the results
    print("\nVehicle counts between TAZs:")
    for taz_pair, count in taz_vehicle_counts.items():
        print(f"From {taz_pair[0]} to {taz_pair[1]}: {count} vehicles")

def main():
    # Define the SUMO command
    sumo_cmd = ["sumo-gui", "-c", "simulation.sumocfg", "--start"]

    # Start TraCI
    traci.start(sumo_cmd)

    # Run the simulation and analysis
    run_simulation()

if __name__ == "__main__":
    main()
