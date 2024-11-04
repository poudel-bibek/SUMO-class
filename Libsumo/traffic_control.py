import libsumo as ls
import os

# Make sure all required files exist
required_files = ["intersection.net.xml", "basic.sumocfg", "routes.rou.xml"]
for file in required_files:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Missing required file: {file}")

# Initialize simulation
ls.start(["sumo", "-c", "basic.sumocfg"])

# Main simulation loop
try:
    for step in range(100):
        # Get traffic light status
        tl_phase = ls.trafficlight.getPhase("C")
        
        # Get queue lengths
        queue_north = ls.lane.getLastStepVehicleNumber("N2C_0")
        queue_south = ls.lane.getLastStepVehicleNumber("S2C_0")
        
        # Print status every 10 steps
        if step % 10 == 0:
            print(f"Step {step}:")
            print(f"  Traffic Light Phase: {tl_phase}")
            print(f"  North Queue: {queue_north}")
            print(f"  South Queue: {queue_south}")
            print(f"  Total Vehicles: {len(ls.vehicle.getIDList())}")
        
        # Simulate step
        ls.simulationStep()

except Exception as e:
    print(f"Error during simulation: {e}")
finally:
    ls.close()