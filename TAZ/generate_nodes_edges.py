# Generate nodes.nod.xml
with open('nodes.nod.xml', 'w') as f:
    f.write('<nodes>\n')
    for y in range(0, 801, 100):  # y from 0 to 800
        for x in range(0, 901, 100):  # x from 0 to 900
            f.write(f'    <node id="N{x}_{y}" x="{x}" y="{y}"/>\n')
    f.write('</nodes>\n')

# Generate edges.edg.xml
with open('edges.edg.xml', 'w') as f:
    f.write('<edges>\n')
    # Horizontal edges
    for y in range(0, 801, 100):
        for x in range(0, 901, 100):
            if x < 900:
                from_node = f'N{x}_{y}'
                to_node = f'N{x+100}_{y}'
                edge_id = f'E{x}_{y}_to_{x+100}_{y}'
                road_type = 'minor_road'
                # Assign road types based on positions
                if y == 400:
                    road_type = 'major_arterial'
                elif y == 200 or y == 600:
                    road_type = 'secondary_road'
                f.write(f'    <edge id="{edge_id}" from="{from_node}" to="{to_node}" type="{road_type}"/>\n')
    # Vertical edges
    for x in range(0, 901, 100):
        for y in range(0, 801, 100):
            if y < 700:
                from_node = f'N{x}_{y}'
                to_node = f'N{x}_{y+100}'
                edge_id = f'E{x}_{y}_to_{x}_{y+100}'
                road_type = 'minor_road'
                # Assign road types based on positions
                if x == 500:
                    road_type = 'major_arterial'
                elif x == 200 or x == 800:
                    road_type = 'secondary_road'
                f.write(f'    <edge id="{edge_id}" from="{from_node}" to="{to_node}" type="{road_type}"/>\n')
    f.write('</edges>\n')
