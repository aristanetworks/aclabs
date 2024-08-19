#!/usr/bin/env python3

import sys
import csv
import yaml
import os
import shutil
from cookiecutter.main import cookiecutter
from cookiecutter import config as cc_config
import argparse


def read_csv_file(filename):
    with open(filename, mode='r') as csv_file:
        csv_row_dict_list = list()  # list of key-value pairs produced from every CSV row except header
        # if header contains __CCvar and __CCvalue CSV will be processed vertically
        # each row will be treated as separate variable with a name of __CCvar
        vars_from_csv = dict()
        for row in csv.DictReader(csv_file):
            updated_row_dict = dict()
            for k, v in row.items():
                # remove potential spaces left and right
                k = k.strip()
                if v:
                    v = v.strip()
                updated_row_dict.update({k: v})
            if '__CCkey' in updated_row_dict.keys():
                if not '__CCvalue' in updated_row_dict.keys():
                    sys.exit(
                        f'ERROR: __CCkey is defined without __CCvalue in {csv_file}')
                vars_from_csv.update({updated_row_dict['__CCkey']: updated_row_dict['__CCvalue']})
            else:
                csv_row_dict_list.append(updated_row_dict)

    if len(csv_row_dict_list):
        return csv_row_dict_list
    else:
        return vars_from_csv

def read_yaml_file(filename, load_all=False):
    with open(filename, mode='r') as f:
        if not load_all:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            # convert generator to list before returning
            yaml_data = list(yaml.load_all(f, Loader=yaml.FullLoader))
    return yaml_data

def smart_update(target_dict: dict, target_value_path: str, source_dict: dict, source_key: str, convert_to='str', mandatory=False) -> dict:
    """This function is doing some basic verification of values from CSV files.
    Feel free to add additional logic if required.

    Args:
        target_dict (dict): dictionary to update
        target_value_path (str): path to the value to be set, separated with '.'. For ex.: key1.key2
        source_dict (dict): An origin dictionary
        source_key (str): The value to be verified
        convert_to (str, optional): Convert original text value to the specified type. Possible types: ['int', 'str']. Defaults to 'str'.
        mandatory (bool, optional): True is value is mandatory. Defaults to False.

    Returns:
        dict: Returns target dictionary
    """

    # check if header is defined in the CSV
    if source_key not in source_dict.keys():
        if mandatory:
            sys.exit(
                f'ERROR: {source_key} field is mandatory and must be defined in the CSV file'
            )
    # check if the value is defined in the CSV
    elif not source_dict[source_key]:
        if mandatory:
            sys.exit(
                f'ERROR: {source_key} has an empty value. It is mandatory and must be defined in the CSV file'
            )
    else:
        if convert_to == 'int':
            source_value = int(source_dict[source_key])
        elif convert_to == 'str':
            source_value = source_dict[source_key]
        else:
            source_value = ''

        if source_value:

            path_keys = target_value_path.split('.')
            target_dict_stack = [target_dict]
            for k in path_keys:
                last_dict_in_stack = target_dict_stack[-1]
                if k in last_dict_in_stack.keys():
                    target_dict_stack.append({k: last_dict_in_stack[k]})
                else:
                    target_dict_stack.append({k: dict()})
            while path_keys:
                k = path_keys.pop()
                last_dict_in_stack = target_dict_stack.pop()
                if isinstance(source_value, dict):
                    last_dict_in_stack[k].update(source_value)
                else:
                    last_dict_in_stack.update({k: source_value})
                source_value = last_dict_in_stack
            
            target_dict.update(source_value)

        return target_dict

def cookiecutter_load(data_input_directory):

    cookiecutter_vars = dict()
    # load all data from input directory and assign to corresponding dict keys
    data_input_directory_full_path = os.path.join(
        os.getcwd(), data_input_directory)
    if not os.path.isdir(data_input_directory_full_path):
        sys.exit(
            f'ERROR: Can not find data input directory {data_input_directory_full_path}')
    
    # read files from the data input directory and add data to cookiecutter json
    # every file will be added as dictionary with a filename without extension as the parent key
    for a_name in os.listdir(data_input_directory_full_path):
        a_full_path = os.path.join(data_input_directory_full_path, a_name)
        if os.path.isfile(a_full_path):
            if '.csv' in a_name.lower():
                csv_data = read_csv_file(a_full_path)
                
                cookiecutter_vars.update({
                    # [:-4] removes .csv
                    a_name.lower()[:-4]: csv_data
                })
            elif '.yml' in a_name.lower():
                data_from_yaml = read_yaml_file(a_full_path)
                cookiecutter_vars['in'].update({
                    # [:-4] removes .yml
                    a_name.lower()[:-4]: data_from_yaml
                })
            elif '.yaml' in a_name.lower():
                data_from_yaml = read_yaml_file(a_full_path)
                cookiecutter_vars['in'].update({
                    # [:-5] removes .yaml
                    a_name.lower()[:-5]: data_from_yaml
                })

    return cookiecutter_vars

if __name__ == "__main__":

    # get directory to load extra context
    parser = argparse.ArgumentParser(
        prog="cc",
        description="Init new lab from template.")
    parser.add_argument(
        '-in', '--input_directory', default='.cc',
        help='Directory with CSV or YAML files to load as extra context for Cookiecutter'
    )
    args = parser.parse_args()

    cookiecutter_dict = cc_config.get_config(".cc/cookiecutter.json")
    cc_extras = cookiecutter_load(args.input_directory)
    cookiecutter_dict.update({
        '__lab': cc_extras
    })

    files_to_copy = list()
    file_index_list = list()
    for root, _, files in os.walk(".cc"):
        for filename in files:
            full_src_path = os.path.join(root, filename)
            f, extension = os.path.splitext(filename)
            if extension == ".jinja":
                if r'{% for' in f:
                    for_loop, true_ext = os.path.splitext(f)
                    cc_loop_key_list = [ lk for lk in for_loop.split() if "cookiecutter" in lk ][0].split(".")[1:]
                    loop_over = cookiecutter_dict
                    for k in cc_loop_key_list:
                        loop_over = loop_over[k]
                    loop_key = for_loop.split()[2]
                    for i, d in enumerate(loop_over):
                        file_index_list.append((os.path.join(root, d[loop_key]+true_ext).replace(".cc/", ".cc-temp/"), i))
                        files_to_copy.append((full_src_path, os.path.join(root, d[loop_key]+true_ext).replace(".cc/", ".cc-temp/")))
                else:
                    files_to_copy.append((full_src_path, os.path.join(root, f).replace(".cc/", ".cc-temp/")))
            else:
                files_to_copy.append((full_src_path, full_src_path.replace(".cc/", ".cc-temp/")))

    for src_file, dst_file in files_to_copy:
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy(src=src_file, dst=dst_file)

    for indexed_file, index in file_index_list:
        with open(indexed_file) as f:
            data = f.read()
        with open(indexed_file, 'w') as f:
            f.write("{%- set cookiecutter_file_index = "+f"{index}"+" -%}\n"+data)

    cookiecutter(template='.cc-temp', overwrite_if_exists=True, extra_context={'__lab': cc_extras})

    shutil.rmtree(".cc-temp")
