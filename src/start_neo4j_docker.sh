#!/bin/bash
set -eo pipefail
IFS=$'\n\t'


# This script starts the Neo4J docker image
# to run it as a deamon add -d when restarting
# http://neo4j.com/docs/operations-manual/current/installation/docker/
# BASE_PATH=/home/puliga/Patent/neo4j-community-3.0.6/

if [[ -d $1 ]]; then
	BASE_PATH=$1
	CONF="${BASE_PATH}/conf/:/conf"
	DATA="${BASE_PATH}/data/:/data"
	LOGS="${BASE_PATH}/logs/:/logs"

	docker run \
	    -d \
	    --publish=7474:7474 \
	    --publish=7687:7687 \
	    --volume="${CONF}" \
	    --volume="${DATA}" \
	    --volume="${LOGS}" \
	    neo4j
else 
	echo "usage CMD NEO4J_DIR"
	echo ""
	echo "the NEO4J_DIR contains the data, conf and logs dirs"
	echo "e.g. /home/puliga/Patent/neo4j-community-3.0.6/"
	echo ""
	exit # EXIT!
fi
