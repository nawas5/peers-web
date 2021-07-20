import os
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from time import perf_counter
from datetime import datetime

pd.options.mode.chained_assignment = None

def tracking_simulator(file, start, stop):

    t1_start = perf_counter()
    print("Process started at: ", datetime.now())

    file_path = "data/" + file

    df = pd.read_csv(file_path, error_bad_lines=False)

    metka_name = df["name"].unique()

    df["time"] = df["time"] - df["time"][0]
    df["time"] = df.time.round(decimals=2)

    df = df.rename(columns={"name":"Label name"})
    df["size"] = 10

    # нормировать х и у на максимальные значения
    # по х - 12, по у - 6
    df["x"] = df["x"] / 13
    df["y"] = 1 - df["y"] / 6

    df = df[(df["time"] >= start) & (df["time"] <= stop)]

    color = ["#eb6b6b", "#7ce04d", "#4de0e0", "#4d74e0", "#c34de0", "#e04d9e"]

    color_discrete_map = {str(metka_name[i]): color[i] for i in range(len(metka_name))}

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="Label name",
        hover_name="Label name",
        animation_frame="time",
        animation_group="Label name",
        range_x=[-0.05, 1.05],
        range_y=[-0.05, 1.05],
        size="size",
        size_max=10,
        opacity=0.8,
        color_discrete_map=color_discrete_map,
        text="Label name",
        hover_data={
            "x": True,
            "y": True,
            "time": False,
            "size": False,
            "Label name": False,
            "z": False,
            "number": False
        },
    )

    fig.add_scatter(
        x=[0,0,1,1],
        y=[0,1,0,1],
        mode="markers",
        marker=dict(size=1,color="white"),
        name="Flags",
    )

    fig.update_traces(
        textfont_size=7, textfont_color="white", hoverinfo="none"
    )

    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        xaxis=dict(range=[-0.05, 1.05]),
        yaxis=dict(range=[-0.05, 1.05]),
        coloraxis_showscale=False,
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    fig.update_xaxes(showticklabels=False, title_text="")
    fig.update_yaxes(showticklabels=False, title_text="")

    image_file = "assets/Rooms12x6.jpg"
    image_path = os.path.join(os.getcwd(), image_file)

    from PIL import Image

    img = Image.open(image_path)

    fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=1,
            sizey=1,
            sizing="stretch",
            opacity=0.7,
            layer="below",
        )
    )

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200

    fig["layout"]["sliders"][0]["pad"]["t"] = 0
    fig["layout"]["updatemenus"][0]["pad"]["t"] = 0

    pio.templates["custom_dark"] = go.layout.Template()
    pio.templates["custom_dark"]["layout"]["paper_bgcolor"] = "#282828"
    pio.templates["custom_dark"]["layout"]["plot_bgcolor"] = "#282828"

    # pio.templates["custom_white"] = go.layout.Template()
    # pio.templates["custom_white"]["layout"]["paper_bgcolor"] = "#f7f7f7"
    # pio.templates["custom_white"]["layout"]["plot_bgcolor"] = "#f7f7f7"

    fig.update_layout(
        template="custom_dark",
        xaxis=dict(showgrid=False, showticklabels=False),
    )

    # slider format and adjustments for aesthetic purposes
    fig["layout"]["sliders"][0]["pad"] = dict(l=0, r=0, b=0, t=0,)
    fig["layout"]["sliders"][0]["minorticklen"] = 2
    fig["layout"]["sliders"][0]["ticklen"] = 5
    fig["layout"]["sliders"][0]["tickcolor"] = "grey"
    fig["layout"]["sliders"][0]["font"]["color"] = "grey"
    fig["layout"]["sliders"][0]["bgcolor"] = "grey"
    fig["layout"]["sliders"][0]["bordercolor"] = "grey"
    fig["layout"]["template"]["data"]["scatter"][0]["marker"]["line"]["color"] = "lightgrey"
    fig["layout"]["template"]["data"]["scatter"][0]["marker"]["opacity"] = 0.9

    # fig["layout"]["sliders"][0]["pad"] = dict(l=10, r=10, b=10, t=10,)
    # fig["layout"]["sliders"][0]["minorticklen"] = 2
    # fig["layout"]["sliders"][0]["ticklen"] = 5
    # fig["layout"]["sliders"][0]["tickcolor"] = "blue"
    # fig["layout"]["sliders"][0]["font"]["color"] = "blue"
    # fig["layout"]["sliders"][0]["bgcolor"] = "blue"
    # fig["layout"]["sliders"][0]["bordercolor"] = "blue"
    # fig["layout"]["template"]["data"]["scatter"][0]["marker"]["line"]["color"] = "lightgrey"
    # fig["layout"]["template"]["data"]["scatter"][0]["marker"]["opacity"] = 0.9

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

    fig.update_layout(
        legend_orientation="v", transition={"duration": 0, "ordering": "traces first"}
    )

    # Make sure pitch background image shape doesn't get distorted
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    t1_stop = perf_counter()
    print("Process took " + str((t1_stop - t1_start) / 60) + " minutes of time")

    fig.update_layout(legend=dict(yanchor="top", y=0.95, xanchor="left", x=-0.08))
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=-0.14,
                x=-0.08,
                xanchor="left",
                yanchor="bottom",
            )
        ]
    )
    fig.update_layout(autosize=True, hovermode="closest")

    fig.update_layout(legend=dict(font=dict(family="Roboto", size=10, color="blue")))

    for trace in fig["data"]:
        if trace["name"] == "Flags":
            trace["showlegend"] = False

    export = input("Do you wish to export the graph to json (y/n)?:")
    if export == "y":
        export_file_name = input(
            "Please enter a name for the json file to be exported (ending with .json): "
        )
        export_file_name = "data/" + export_file_name
        with open(export_file_name, "w") as f:
            pio.write_json(fig, f)
            f.close()

    return fig


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# какие доки читаются

filename = "log.csv"
start = 0
stop = 300

app.layout = html.Div(
    [
        dcc.Graph(
            figure=tracking_simulator(filename,start,stop)
        )
    ]
)

start_server = input("Do you want to display the graph (y/n)?: ")
if start_server == "y":
    app.run_server(debug=True, use_reloader=False)