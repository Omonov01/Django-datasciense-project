import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64
def get_image():
    buffer = BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode("utf-8","ignore")
    # print("a")
    # print(type(graph))
    buffer.close()
    # print(type(image_png))
    return graph


def get_simple_plot(chart_type,*args, **kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(5,5))  
    x = kwargs.get("x")
    y = kwargs.get("y")
    data = kwargs.get("data")
    if chart_type == "bar plot":
        title = "Kunlik sotuvlar miqdori (bar) title"
        plt.title(title)
        plt.bar(x,y)
    elif chart_type == "Kunlik sotuvlar miqdori (line) plot":
        title = "title"
        plt.title(title)
        plt.plot(x,y)
    elif chart_type == "count plot":
        title = "Mahsulot soni"
        plt.title(title)
        sns.countplot(x="name",data=data)
    plt.xticks(rotation=45)
    plt.tight_layout()

    graph = get_image()
    return graph
