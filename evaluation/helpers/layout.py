import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns


def create_layout():
    # Define your color palettes
    # palette = sns.color_palette("Set1", 16).as_hex() # Generate a color palette
    palette = px.colors.qualitative.Dark24
    palette2 = px.colors.qualitative.Alphabet
    het_type_indices = [0, 2, 19, 10, 22]
    model_id_indices = [0, 2, 11, 24, 17, 18, 25, 23, 14]

    het_type_palette = [palette[i] for i in het_type_indices]
    model_id_palette = [palette2[i] for i in model_id_indices]

    # Define the font for your layout
    layout_font = dict(
        family="Arial",
        size=14,
        color="black",  # You can replace this color as you prefer
    )

    # Define the title properties
    title_properties = dict(y=0.9, x=0.5, xanchor="center", yanchor="top")

    xaxis = dict(
        title_font=dict(family="Arial", size=14, color="black"),
        showgrid=False,  # This controls horizontal gridlines
    )
    yaxis = dict(
        title_font=dict(family="Arial", size=14, color="black"),
    )

    legend = dict(
        x=1.01,
        y=1,
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(0,0,0,0)",
    )

    # Create your layout
    layout = go.Layout(
        template="seaborn",  # Using seaborn template
        autosize=False,
        width=1000,  # pixels
        height=400,  # pixels
        uniformtext_minsize=11,
        uniformtext_mode="hide",
        font=layout_font,
        # title=title_properties,
        xaxis=xaxis,
        yaxis=yaxis,
        legend=legend,
        # colorway=het_type_palette,  # Setting colorway for het_types
        # You can add more attributes here as needed
    )

    return layout, het_type_palette, model_id_palette
