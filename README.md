# *ROAR Stats*

A tool for scraping current usage information from nodes
(Note: Currently compatible with nodes with 1 or fewer types GPU)


## Installation:

First activate a conda environment, then navigate to directory you want to install the package
```
git clone https://github.com/gmwendel/ROAR_Stats
cd ROAR_Stats
pip install --editable .
```

Display stats about current SAGEMAPP utilization after install
by running sagemapp_stats. Example:
```
$ sagemapp_stats
----------------------------------------------------------------------------------
Node Name:  	 Used/Total 	 Used/Total 	 	 Used/Total 	 GPU_Type
comp-mgc-0001: 	 CPU: 0/40 	 RAM: 0G/1510.1G 	 GPU: 0/10 	 gc_v100s.
comp-mgc-0002: 	 CPU: 0/40 	 RAM: 0G/1510.1G 	 GPU: 0/10 	 gc_v100s.
comp-mgc-0003: 	 CPU: 4/40 	 RAM: 100.0G/1510.1G 	 GPU: 1/10 	 gc_v100s.
comp-mgc-0004: 	 CPU: 0/40 	 RAM: 0G/754.3G 	 GPU: 0/3 	 gc_rtx6000.
comp-mgc-0005: 	 CPU: 0/40 	 RAM: 0G/754.3G 	 GPU: 0/3 	 gc_rtx6000.
comp-mgc-0006: 	 CPU: 0/40 	 RAM: 0G/754.3G 	 GPU: 0/4 	 gc_v100nvl.
comp-mgc-0007: 	 CPU: 0/40 	 RAM: 0G/754.3G 	 GPU: 0/3 	 gc_v100nvl.
comp-mgc-0008: 	 CPU: 30/40 	 RAM: 136.0G/1510.1G 	 GPU: 16/16 	 gc_t4.
comp-mgc-0009: 	 CPU: 16/40 	 RAM: 80.0G/1510.1G 	 GPU: 7/16 	 gc_t4.
comp-mgc-0010: 	 CPU: 25/40 	 RAM: 128.0G/1510.1G 	 GPU: 4/15 	 gc_t4.
comp-mgc-0011: 	 CPU: 14/40 	 RAM: 56.0G/1510.1G 	 GPU: 7/14 	 gc_t4.
----------------------------------------------------------------------------------

```

Usage notes:
Perform updates at a rate of <1 per minute to avoid stressing the job scheduling system
