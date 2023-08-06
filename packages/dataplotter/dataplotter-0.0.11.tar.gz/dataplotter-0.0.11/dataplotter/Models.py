# type hinting
from typing import Any
# plotly plotting library
import plotly.graph_objs as go

###
### Class definitions
###

###
### PART 1: Implement DataSet class without filter function
###
class DataSet:
    """ Contains data from columns. """
    # Contains all data from columns in row
    Data: list[float]
    # Contains the current row of data
    Row: int

    def __init__(self, rowIndex: int, rowStr: str) -> None:
        """Construct a standard DataSet based on a string containg data delimited by ws.

        Args:
            rowIndex (int): The row the dataset comes from.
            rowStr (str): The complete row as string.
        """
        self.Data = []
        self.Row = rowIndex
        self.ReadData(rowStr)

    def ReadData(self, rowStr: str):
        """ Converts string data to data list. """
        # rowStr:   ["0","1","1.2","3.5"]
        for data in rowStr.split():
            self.Data.append(float(data))

    ###
    ### PART 3: Implement filter function on DataSet
    ###   
    def filter(self,filter):
        """Filter data with the help of a filter function

        Args:
            filter (function): Accepts a list, returns a list.
        """
        self.Data = filter(self.Data)    

class DataPlotter:
    """
    Contains a set of DataSets and is able to plot them.

    Before plotting, apply a filter function.
    """

    DataSets: list[DataSet]
    Filter: Any
    Columns: int

    def __init__(self, path):
        """A DataPlotter can plot data.

        Args:
            path (str): The file path containing the data.
        """
        ###
        ### PART 2: Implement reading of data
        ###
        self.DataSets = []
        self.Columns = 0
        # default Filter: return the argument
        self.Filter = lambda d: d

        with open(path, 'r') as dataFile:
            lines = dataFile.readlines()

            for row,line in enumerate(lines):
                self.DataSets.append(DataSet(row,line))

                self.Columns = max(self.Columns, self.DataSets[-1].Data.__len__()-1)


    def plot(self):
        """ Plot the data. """
        # get the x values of the datasets
        x = [xi.Data[0] for xi in self.DataSets]
        # extract all y values from the datasets
        y = [yi.Data[1:] for yi in self.DataSets]
      
        lines = []

        for col in range(self.Columns):
            # extract current y value from y list
            cury = [yi[col-1] for yi in y]

            lines.append(go.Scatter(x=x, y=cury, name=f'Column {col+1}'))
      
        fig = go.Figure(data=lines)
        fig.show()


    def filterData(self, function = None ):
        """ Filter all data. """
        # if there is a filter, pass that filter to every dataset
        if function != None:
            for data in self.DataSets:
                data.filter(function)                
        else:
            # call with default filter
            for data in self.DataSets:
                data.filter(self.Filter)        
        
        # update column length
        self.Columns = max(self.Columns, self.DataSets[-1].Data.__len__()-1)