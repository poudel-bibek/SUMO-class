import os
import sys
import time
import traci

def run_simulation():
    try:
        traci.start(["sumo-gui", "-c", "ped_sim.sumocfg"])
        step = 0
        
        while step < 1000:
            traci.simulationStep()
            
            # Get all pedestrians in simulation
            pedestrians = traci.person.getIDList()
            
            # Print statistics every 50 steps
            if step % 50 == 0:
                print(f"\nStep {step}")
                print(f"Number of pedestrians: {len(pedestrians)}")
                if pedestrians:
                    # Print positions of first 5 pedestrians
                    for ped in list(pedestrians)[:5]:
                        pos = traci.person.getPosition(ped)
                        edge = traci.person.getRoadID(ped)
                        print(f"Pedestrian {ped}: pos={pos}, edge={edge}")
            
            step += 1
            time.sleep(0.1)  # Slow down simulation for visualization
            
    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        traci.close()

if __name__ == "__main__":
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    
    run_simulation()