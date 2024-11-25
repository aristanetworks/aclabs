#!/usr/bin/env python3

import copier
import sys
import csv
import yaml
import os
import shutil
import argparse
import re

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

def load_extra_vars(data_input_directory):

    extra_vars = dict()
    # load all data from input directory and assign to corresponding dict keys
    data_input_directory_full_path = os.path.join(
        os.getcwd(), data_input_directory)
    if not os.path.isdir(data_input_directory_full_path):
        sys.exit(
            f'ERROR: Can not find data input directory {data_input_directory_full_path}')
    
    # read files from the data input directory and add to extra_vars
    # every file will be added as dictionary with a filename without extension as the parent key
    for a_name in os.listdir(data_input_directory_full_path):
        a_full_path = os.path.join(data_input_directory_full_path, a_name)
        if os.path.isfile(a_full_path):
            if '.csv' in a_name.lower():
                csv_data = read_csv_file(a_full_path)
                
                extra_vars.update({
                    # [:-4] removes .csv
                    a_name.lower()[:-4]: csv_data
                })
            elif '.yml' in a_name.lower():
                data_from_yaml = read_yaml_file(a_full_path)
                extra_vars.update({
                    # [:-4] removes .yml
                    a_name.lower()[:-4]: data_from_yaml
                })
            elif '.yaml' in a_name.lower():
                data_from_yaml = read_yaml_file(a_full_path)
                extra_vars.update({
                    # [:-5] removes .yaml
                    a_name.lower()[:-5]: data_from_yaml
                })

    return extra_vars

if __name__ == "__main__":

    default_template_dir = '.cp'
    default_input_dir = '.cp/extra-vars/default'
    temp_template_dir = '.cp-temp'

    # get directory to load extra context
    parser = argparse.ArgumentParser(
        prog="copy",
        description="Init new lab from template.")
    parser.add_argument(
        '-in', '--input_directory', default=default_input_dir,
        help='Directory with CSV or YAML files to load as extra context'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='Debug the templating tool. This will save all files in a dedicated directory.'
    )
    args = parser.parse_args()

    if args.debug:
        copier_dst_directory = 'temp'
    else:
        copier_dst_directory = '.'

    extra_vars = load_extra_vars(args.input_directory)

    files_to_copy = list()
    file_index_list = list()
    for root, _, files in os.walk(default_template_dir):
        for filename in files:
            full_src_path = os.path.join(root, filename)
            f, extension = os.path.splitext(filename)
            if extension == ".jinja" and re.match(r"^\{%.*for", f):
                re_pattern = r"(?:^\{%\s* for\s*)(\w+)(?:\s*in\s*)(\w+)(?:\s*%\}).(\w+)$"
                loop_key = re.sub(re_pattern, r"\1", f)
                loop_over = extra_vars[re.sub(re_pattern, r"\2", f)]
                true_ext = re.sub(re_pattern, r".\3.jinja", f)
                for i, d in enumerate(loop_over):
                    file_index_list.append((os.path.join(root, d[loop_key]+true_ext).replace(default_template_dir, temp_template_dir), i))
                    files_to_copy.append((full_src_path, os.path.join(root, d[loop_key]+true_ext).replace(default_template_dir, temp_template_dir)))
            else:
                files_to_copy.append((full_src_path, full_src_path.replace(default_template_dir, temp_template_dir)))

    for src_file, dst_file in files_to_copy:
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy(src=src_file, dst=dst_file)

    for indexed_file, index in file_index_list:
        with open(indexed_file) as f:
            data = f.read()
        with open(indexed_file, 'w') as f:
            f.write("{%- set copier_file_index = "+f"{index}"+" -%}\n"+data)

    # run copier
    cp = copier
    cpWorker = cp.Worker(src_path=temp_template_dir, dst_path=copier_dst_directory, data=extra_vars, unsafe='True')
    cpWorker.run_copy()

    shutil.rmtree(temp_template_dir)
