from node import Node
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose', default=False, type=bool,
                        help='Add flag to display job information on node; Default = False')
    args = parser.parse_args()

    node_prefix = "comp-mgc-"#Generate node names
    node_names = [node_prefix + str(i).zfill(4) for i in range(1, 12)]
    nodes = [Node(name) for name in node_names] #Add nodes to list

    print("----------------------------------------------------------------------------------")
    print("Node Name:  \t Used/Total \t Used/Total \t \t Used/Total \t GPU_Type")
    for node in nodes:
        node.print_stats()
        if args.verbose:
            cmd = subprocess.run("qstat -a1nt | grep {}".format(node.name),
                     shell=True, stdout=subprocess.PIPE)
            out = cmd.stdout.decode('utf-8')
            print(out)
    print("----------------------------------------------------------------------------------")
