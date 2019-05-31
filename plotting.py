import matplotlib.pyplot as plt
import skrf as rf
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter a filename to plot your favorite .s2p file!')
    parser.add_argument('name', type=str, nargs='?', default='ntwk.s2p', help='Name of the file.')
    args = parser.parse_args()
    network = rf.Network('./'+args.name)
    network.plot_s_db()
    plt.show()
