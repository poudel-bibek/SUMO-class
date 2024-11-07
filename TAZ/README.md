# SUMO Traffic Simulation Setup Guide

This guide outlines the step-by-step process to set up and run a traffic simulation using SUMO (Simulation of Urban MObility).

## Prerequisites

- SUMO (1.20.0)
- Python 3.12

## Setup Process

### 1. Network Generation

First, start with the network generation scripts:

```bash
# Generate initial nodes and edges
python generate_nodes_edges.py
```

This will create:
- `nodes.nod.xml`
- `edges.edg.xml`

Make sure you have the `road_types.typ.xml` file in your working directory.

### 2. TAZ (Traffic Assignment Zones) Configuration

#### 2.1. Add TAZ Nodes

Add the following nodes to your `nodes.nod.xml` file:

```xml
<!-- TAZ Connector Nodes -->
<!-- TAZ1: Southwest Corner -->
<node id="source_TAZ1_node" x="-100" y="100" type="priority"/>
<node id="sink_TAZ1_node" x="100" y="-100" type="priority"/>

<!-- TAZ2: Southeast Corner -->
<node id="source_TAZ2_node" x="1000" y="100" type="priority"/>
<node id="sink_TAZ2_node" x="800" y="-100" type="priority"/>

<!-- TAZ3: Northwest Corner -->
<node id="source_TAZ3_node" x="-100" y="600" type="priority"/>
<node id="sink_TAZ3_node" x="100" y="800" type="priority"/>

<!-- TAZ4: Northeast Corner -->
<node id="source_TAZ4_node" x="1000" y="600" type="priority"/>
<node id="sink_TAZ4_node" x="800" y="800" type="priority"/>
```

#### 2.2. Add TAZ Edges

Add the following edges to your `edges.edg.xml` file:

```xml
<!-- TAZ Connector Edges -->
<!-- TAZ1: Southwest Corner -->
<edge id="source_TAZ1" from="source_TAZ1_node" to="N0_100" type="minor_road"/>
<edge id="sink_TAZ1" from="N100_0" to="sink_TAZ1_node" type="minor_road"/>

<!-- TAZ2: Southeast Corner -->
<edge id="source_TAZ2" from="source_TAZ2_node" to="N900_100" type="minor_road"/>
<edge id="sink_TAZ2" from="N800_0" to="sink_TAZ2_node" type="minor_road"/>

<!-- TAZ3: Northwest Corner -->
<edge id="source_TAZ3" from="source_TAZ3_node" to="N0_600" type="minor_road"/>
<edge id="sink_TAZ3" from="N100_700" to="sink_TAZ3_node" type="minor_road"/>

<!-- TAZ4: Northeast Corner -->
<edge id="source_TAZ4" from="source_TAZ4_node" to="N900_600" type="minor_road"/>
<edge id="sink_TAZ4" from="N800_700" to="sink_TAZ4_node" type="minor_road"/>
```

### 3. Network Conversion

Generate the network file using netconvert:

```bash
netconvert --node-files=nodes.nod.xml \
           --edge-files=edges.edg.xml \
           --type-files=road_types.typ.xml \
           --output-file=simple.net.xml
```

### 4. Vehicle Types Configuration

Add the `vtypes.add.xml` file and regenerate the network:

```bash
netconvert --node-files=nodes.nod.xml \
           --edge-files=edges.edg.xml \
           --type-files=road_types.typ.xml \
           --output-file=simple.net.xml
```

### 5. Network Editing (Optional)

You can use SUMO's netedit tool to make minor adjustments to `simple.net.xml` if needed.

### 6. Traffic Demand Generation

#### 6.1. Create OD Matrix
Create the `od_matrix.odm.xml` file based on the provided example.

#### 6.2. Generate Trips
Convert the OD matrix to trips:

```bash
od2trips --xml-validation never \
         --taz-files taz.add.xml \
         --tazrelation-files od_matrix.odm.xml \
         -o trips.trips.xml
```

#### 6.3. Generate Routes
Convert trips to routes using duarouter:

```bash
duarouter --trip-files trips.trips.xml \
          --net-file simple.net.xml \
          --additional-files vtypes.add.xml \
          -o routes.rou.xml
```

### 7. Run Simulation

Execute the simulation using:

```bash
python sim_run.py
```

## File Structure

```
project/
├── generate_nodes_edges.py
├── road_types.typ.xml
├── nodes.nod.xml
├── edges.edg.xml
├── taz.add.xml
├── vtypes.add.xml
├── od_matrix.odm.xml
├── simple.net.xml
├── trips.trips.xml
├── routes.rou.xml
└── sim_run.py
```

## Notes

- Make sure all XML files are properly formatted and validated
- Keep backups of your configuration files
- Check SUMO logs for any errors during the process
