import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

class DataVisualizer:
    def __init__(self, df):
        self.df = df

    def create_bar_chart(self, x_col, y_col):
        return px.bar(self.df, x=x_col, y=y_col, title=f"Bar Chart: {y_col} by {x_col}")

    def create_line_chart(self, x_col, y_col):
        return px.line(self.df, x=x_col, y=y_col, title=f"Line Chart: {y_col} over {x_col}")

    def create_scatter_plot(self, x_col, y_col, color_col=None):
        return px.scatter(self.df, x=x_col, y=y_col, color=color_col,
                         title=f"Scatter Plot: {y_col} vs {x_col}")

    def create_pie_chart(self, names_col, values_col):
        return px.pie(self.df, names=names_col, values=values_col,
                     title=f"Pie Chart: {values_col} by {names_col}")

    def create_histogram(self, col):
        return px.histogram(self.df, x=col, title=f"Histogram of {col}")

    def create_box_plot(self, col):
        return px.box(self.df, y=col, title=f"Box Plot of {col}")

    def create_heatmap(self, corr_matrix):
        return px.imshow(corr_matrix, title="Correlation Heatmap")

    def create_3d_scatter(self, x_col, y_col, z_col, color_col=None):
        return px.scatter_3d(self.df, x=x_col, y=y_col, z=z_col, color=color_col,
                            title=f"3D Scatter Plot") 