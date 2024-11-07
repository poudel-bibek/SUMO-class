import os
import sys
import traci

def run_simulation():
    sumo_cmd = ["sumo-gui", "-c", "ped_sim.sumocfg"]
    
    try:
        traci.start(sumo_cmd)
        step = 0
        while step < 100:
            traci.simulationStep()
            step += 1
    finally:
        traci.close()

if __name__ == "__main__":
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
        
    run_simulation()