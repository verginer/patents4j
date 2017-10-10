#!/usr/bin/env python3

import re
import pandas as pd
import os
import click

# Regular expression to extract the section, class, subclass, group
# and subgroup parts
ipc_code_re = re.compile(r'^([A-Z])(\d{1,2})([A-Z])(\d{1,5})?(/\d+)?')


def extract_ipc_code_dict(ipc_string: str)->dict:
    """
    Returns for given IPC code of the form "A01B33/05" a dictionary with the
    individual levels broken out

    Parameters
    ----------
    ipc_string

    Returns
    -------
    dict

    Example
    -------
    >>> extract_ipc_code_dict('H05K234/03'))
    {'cl': 'H05', 'gr': 'H05K234', 'maingr': 'H05K234/00', 'sec': 'H',
    'subcl': 'H05K', 'subgr': 'H05K234/035'}

    """
    parts = ipc_code_re.match(ipc_string).groups()

    # how many parts have been returned?
    num_el = sum(1 for x in parts if x)

    sec, cls, subcl, group, subgroup = parts

    if num_el <= 3:
        return dict(sec=sec,
                    cl=sec + cls,
                    subcl=sec + cls + subcl,
                    gr=None,
                    maingr=None,
                    subgr=None)

    else:
        if subgroup.endswith("/00"):
            return dict(sec=sec,
                        cl=sec + cls,
                        subcl=sec + cls + subcl,
                        gr=sec + cls + subcl + group,
                        maingr=sec + cls + subcl + group + subgroup,
                        subgr=None)
        else:
            return dict(sec=sec,
                        cl=sec + cls,
                        subcl=sec + cls + subcl,
                        gr=sec + cls + subcl + group,
                        maingr=sec + cls + subcl + group + '/00',
                        subgr=sec + cls + subcl + group + subgroup)


@click.command()
@click.option('-f', '--infile', help='file with unique class ids, one per line'
                                     ' (see bash script)')
@click.option('-o', '--out-dir', help='directory where to write the neo4j '
                                      'csvs to, note there are 5')
def main(infile, out_dir):
    code_df = pd.read_csv(infile, names=['class'])

    def ipc_record(code):
        return pd.Series(extract_ipc_code_dict(code))

    class_hierarchy = code_df['class'].apply(ipc_record)

    code_levels = ('sec', 'cl', 'subcl', 'gr', 'maingr', 'subgr')
    edge_column_pairs = list(zip(code_levels[:-1], code_levels[1:]))

    edge_df_list = []
    for edge in edge_column_pairs:
        edge_column_pairs = class_hierarchy[list(edge)].drop_duplicates().copy()
        # filter out any edge which has a None
        filter_none = (
            edge_column_pairs[edge[0]].apply(lambda x: x is not None) &
            edge_column_pairs[edge[1]].apply(lambda x: x is not None)
        )
        edge_column_pairs = edge_column_pairs[filter_none]

        new_names = {edge[0]: ":END_ID", edge[1]: ":START_ID"}
        edge_df_list.append(edge_column_pairs.rename(columns=new_names))

    file_out = os.path.join(out_dir, "rel_subcategory.csv")
    pd.concat(edge_df_list).to_csv(file_out, index=False)

    for node_type in code_levels:
        file_name = "node_ipc_{}.csv".format(node_type)
        file_out = os.path.join(out_dir, file_name)
        node_df = class_hierarchy[node_type].drop_duplicates().copy()
        node_df.rename("ipc_id:ID").to_csv(file_out, index=False, header=True)

    return 0

if __name__ == "__main__":
    main()
