import yaml

def merge_topologies(input_files, output_file):
    master_data = {}

    for input_file in input_files:
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)

        # Merge top-level sections
        for section in ('veos', 'generic', 'cvp'):
            if section in data:
                master_data[section] = data[section]  # Overwrite for these sections

        # Merge 'nodes' 
        if 'nodes' in master_data:
            for node in data['nodes']:
                node_name = list(node.keys())[0]  # Extract the first key as node_name
                if not any(node_name in n for n in master_data['nodes']):  # Corrected duplicate check
                    master_data['nodes'].append(node)
                else:
                    print(f"Duplicate node found: {node_name}. Keeping the original version.")
        else:
            master_data['nodes'] = data['nodes']


        # Merge 'links' 
        if 'links' in master_data:
            for link in data['links']:
                # Check for simple duplicate
                if link in master_data['links']:
                    print(f"Duplicate link found: {link}. Skipping.")
                    continue

                # Check for reverse duplicate
                reverse_link = {
                    'connection': [link['connection'][1], link['connection'][0]]
                }
                if reverse_link in master_data['links']:
                    print(f"Reverse duplicate link found: {link}. Skipping.")
                    continue

                # No duplicate found
                master_data['links'].append(link)
        else:
            master_data['links'] = data['links']

    with open(output_file, 'w') as f:
        yaml.dump(master_data, f, default_flow_style=False)  # Try to preserve formatting

input_files = [
    'backbone/lab_topology/FABRIC-act_topology.yml', 
    'domain-a/lab_topology/FABRIC-act_topology.yml', 
    'domain-b/lab_topology/FABRIC-act_topology.yml',
    'domain-c/lab_topology/FABRIC-act_topology.yml',
    'domain-d/lab_topology/FABRIC-act_topology.yml'
 ]
output_file = 'act/tl_combined_topology.yml'

merge_topologies(input_files, output_file)
