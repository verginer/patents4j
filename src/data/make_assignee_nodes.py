# ==> node_assignees.csv <==
# assignee_id:ID,name
# HA22476,ABT Holding Company
# HA634666,Haas Maschinenbau GmbH
# LA604727,"Youds, Mark"
# LA672879,Verdi Visual Intelligence Ltd.
# LA793589,KENT STATE UNIVERSITY
# UA1190590,Clearwater Specialties- LLC
# UA1231050,"Dabczynski, Zdzislaw"
# UA918957,"Weiler, Dieter"
# UA928847,ZTE Corporation
import string
from collections import Counter
import pandas as pd
from tqdm import tqdm
import click


def normalize_name(name: str) -> str:
    punctuation = string.punctuation
    n_name = name.lower()
    n_name = ''.join(c for c in n_name if c not in punctuation)
    return n_name


def most_common_name(name_df: pd.DataFrame) -> str:
    if isinstance(name_df, str):
        return name_df
    else:
        counts = Counter(name_df.apply(normalize_name))
        return counts.most_common()[0][0]


@click.command()
@click.argument('linked_assignee_names',
                type=click.Path(exists=True, dir_okay=False))
@click.argument('edgelist_dir',
                type=click.Path(exists=True, file_okay=False))
def make_assignee_nodes_rels(linked_assignee_names, edgelist_dir):
    col_names = [
        'assignee_id',
        'patent_id',
        'name',
        'georef',
        'quality',
        'type'
    ]

    assignee_df = pd.read_csv(
        linked_assignee_names,
        index_col='assignee_id',
        sep='|',
        header=None,
        names=col_names
    )

    assignee_ids = assignee_df.index.unique()
    nodes_df = pd.DataFrame(index=assignee_ids, columns=['name'])

    for assignee_id in tqdm(assignee_ids):
        name = most_common_name(assignee_df.loc[assignee_id, 'name'])
        nodes_df.loc[assignee_id, 'name'] = name

    nodes_df['assignee_id:ID'] = nodes_df.index
    nodes_df.to_csv(edgelist_dir, index=False)


if __name__ == "__main__":
    make_assignee_nodes_rels()
