#!/bin/bash

# path where to find neo4j (i.e. ~/test/neo4j-community-3.0.6/)
# NOTE one level above the /bin/neo4j-import levels
NEO_PATH=$1

# path where to find the cleaned csvs
CLEAN_PATH=$2


"$NEO_PATH/bin/neo4j-import" \
        --into "${NEO_PATH}/data/databases/patents.db" \
        --nodes:Patent "${CLEAN_PATH}/node_patents.csv" \
        --nodes:Inventor "${CLEAN_PATH}/node_inventors_mobile.csv" \
        --nodes:Assignee "${CLEAN_PATH}/node_assignees.csv" \
        --nodes:Section:IPC "${CLEAN_PATH}/node_ipc_sec.csv" \
        --nodes:Class:IPC "${CLEAN_PATH}/node_ipc_cl.csv" \
        --nodes:Subclass:IPC "${CLEAN_PATH}/node_ipc_subcl.csv" \
        --nodes:Group:IPC "${CLEAN_PATH}/node_ipc_gr.csv" \
        --nodes:Maingroup:IPC "${CLEAN_PATH}/node_ipc_maingr.csv" \
        --nodes:Subgroup:IPC "${CLEAN_PATH}/node_ipc_subgr.csv" \
        --relationships:ASSIGNEE_OF "${CLEAN_PATH}/rel_assignee_of.csv" \
        --relationships:INVENTOR_OF "${CLEAN_PATH}/rel_inventor_of_mobile.csv" \
        --relationships:CITING "${CLEAN_PATH}/rel_citing.csv" \
        --relationships:SUBCATEGORY_OF "${CLEAN_PATH}/rel_subcategory.csv" \
        --relationships:CLASSED_AS "${CLEAN_PATH}/rel_classed_as.csv" \

echo ""
echo ""
echo "Remember to create the indices on the IDs!"
echo ""
echo "CREATE INDEX ON :IPC(ipc_id)"
echo "CREATE INDEX ON :Inventor(inventor_id)"
echo "CREATE INDEX ON :Assignee(assignee_id)"
echo "CREATE INDEX ON :Patent(patent_id)"
echo "CREATE INDEX ON :Patent(year)"
echo ""

