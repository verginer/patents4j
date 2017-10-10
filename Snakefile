configfile: 'config/snakeconfig.yaml'


import munch


# makes the config accessible through dot notation
config = munch.munchify(config)

RAW = config.dirs.raw
INT = config.dirs.interim
PRO = config.dirs.processed


#=========================================================================
# https://snakemake.readthedocs.io/en/stable/getting_started/examples.html
#=========================================================================
#
#rule all:
#    input: protect(interim+'/deals.csv')
#
#
#rule report:
#    input:
#        raw+'/recap_raw.csv',
#        lambda wildcards: config["samples"][wildcards.sample]
#    output: protect/temp(interim+'/deals.csv')
#    threads: 3
#    params:
#        rg = "@RG\tID:{sample}\tSM:{sample}"
#    script: 'src/rules/clean_recap.py'
