import unittest
import subprocess
import os
import shutil
import matplotlib.pyplot as plt
import gsbatch


def run(cmd, verbose=False):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


def dummy_plot(filename):
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    fig.savefig(filename)
    plt.close(fig)


class Test_topng(unittest.TestCase):

    def test_basic(self):

        dummy_plot("test.pdf")
        output = run("gsbatch_topng -f -q test.pdf")
        self.assertTrue(os.path.isfile("test.png"))
        os.remove("test.pdf")
        os.remove("test.png")


if __name__ == '__main__':

    unittest.main()
