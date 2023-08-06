# argparse for parsing of incoming arguments
from DataPlotter.Models import DataPlotter
import argparse

# parse input with the help of an argument parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
# input path to specimen folder
parser.add_argument('-file', help='Path to file')

# read arguments
args = parser.parse_args()

# get the file path from arguments
filePath = args.file

# create a DataPlotter
plotter = DataPlotter("exampleData.dat")

# filter our data
def filterFunction(data):
    return data + [abs(data[2]-data[1])]

plotter.filterData(filterFunction)

plotter.plot()