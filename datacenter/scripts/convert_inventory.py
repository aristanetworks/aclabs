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

    # Function to recursively search and update ansible_host IPs
    def update_hosts(hosts, act_hosts):
        for host, properties in hosts.items():
            if 'ansible_host' in properties:
                act_host_ip = act_hosts.get(host, {}).get('ansible_host')
                if act_host_ip:
                    properties['ansible_host'] = act_host_ip
            if 'ansible_httpapi_host' in properties:
                act_httpapi_host_ip = act_hosts.get(host,{}).get('ansible_httpapi_host')
                if act_httpapi_host_ip:
                    properties['ansible_httpapi_host'] = act_httpapi_host_ip

    # Function to recursively traverse the inventory data
    def traverse_and_update(data, act_data):
        if 'hosts' in data:
            update_hosts(data['hosts'], act_data.get('hosts', {}))
        if 'children' in data:
            for child in data['children']:
                # Check if the child exists in act_data before traversing
                if 'children' in act_data and child in act_data['children']:
                    traverse_and_update(data['children'][child], act_data['children'][child])

    # Start the updating process
    traverse_and_update(inventory_data['all'], act_inventory_data['all'])

    # Write the updated data to a new file, ensuring null values are not written
    with open(output_file, 'w') as file:
        yaml.dump(inventory_data, file, sort_keys=False, default_flow_style=False)

    return output_file

if __name__ == '__main__':
    update_ansible_host_ips_with_argparse()
