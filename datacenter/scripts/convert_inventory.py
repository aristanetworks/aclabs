import argparse
import yaml

def update_ansible_host_ips_with_argparse():
    # Define a custom representer for None (null values)
    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '')

    # Add the custom representer to the Dumper
    yaml.add_representer(type(None), represent_none)

    # Setup argparse for command line arguments
    parser = argparse.ArgumentParser(description='Update ansible_host IPs in inventory files.')
    parser.add_argument('directory', choices=['domain-a', 'domain-b', 'domain-c', 'backbone'], 
                        help='Directory where the inventory files are located')
    args = parser.parse_args()

    # Define the file paths based on the specified directory
    inventory_file = f'{args.directory}/inventory.yml'
    act_inventory_file = f'act-inventory.yml'
    output_file = f'{args.directory}/inventory.yml'

    # Load inventory.yml
    with open(inventory_file, 'r') as file:
        inventory_data = yaml.safe_load(file)

    # Load act-inventory.yml
    with open(act_inventory_file, 'r') as file:
        act_inventory_data = yaml.safe_load(file)

    # Function to create a map of hosts from act_inventory.yml
    def create_hosts_map(data, hosts_map):
        if 'hosts' in data:
            for host, properties in data['hosts'].items():
                hosts_map[host] = properties
        if 'children' in data:
            for child in data['children']:
                create_hosts_map(data['children'][child], hosts_map)

    # Function to update hosts in inventory.yml using the hosts map
    def update_hosts_with_map(hosts, hosts_map):
        for host, properties in hosts.items():
            if host in hosts_map:
                for key, value in hosts_map[host].items():
                    if key in ['ansible_host', 'ansible_httpapi_host']:  # Update only specific keys
                        properties[key] = value

    # Function to recursively traverse and update inventory.yml
    def traverse_and_update_with_map(data, hosts_map):
        if data is None:
            return
        if 'hosts' in data:
            update_hosts_with_map(data['hosts'], hosts_map)
        if 'children' in data:
            for child in data['children']:
                traverse_and_update_with_map(data['children'][child], hosts_map)

    # Create hosts map from act_inventory.yml
    act_hosts_map = {}
    create_hosts_map(act_inventory_data['all'], act_hosts_map)

    # Update inventory.yml using the hosts map
    traverse_and_update_with_map(inventory_data['all'], act_hosts_map)

    # Write the updated data to inventory.yml
    with open(output_file, 'w') as file:
        yaml.dump(inventory_data, file, sort_keys=False, default_flow_style=False)

    return output_file

if __name__ == '__main__':
    updated_file = update_ansible_host_ips_with_argparse()
    print(f"Updated inventory file: {updated_file}")
