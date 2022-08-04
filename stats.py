from node import Node


def main():
    node_prefix = "comp-mgc-"
    node_names = [node_prefix + str(i).zfill(4) for i in range(1, 12)]
    nodes = [Node(name) for name in node_names]

    print("----------------------------------------------------------------------------------")
    print("Node Name:  \t Used/Total \t Used/Total \t \t Used/Total \t GPU_Type")
    for node in nodes:
        node.print_stats()
    print("----------------------------------------------------------------------------------")
