from .chart import Chart
import plotly.figure_factory as ff
from IPython.display import display
import pandas as pd

class Table(Chart):
    def __init__(self, dataframe, kwargs):
        """
        Constructs all the necessary attributes for the Table object

        Parameters:
            dataframe (pandas.Dataframe): The dataframe
        """
        Chart.__init__(self, dataframe, kwargs)

    def plot(self):
        """
        Generate table visualization
        """
        if len(self.dataframe) > 1000 :
            fig = ff.create_table(self.dataframe)
            fig.show()
        else:
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                display(self.dataframe)    