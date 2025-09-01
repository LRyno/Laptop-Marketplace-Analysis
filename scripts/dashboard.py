import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from pathlib import Path
import numpy as np

file_path = Path(__file__).resolve().parent.parent/'02. Cleansing'/'formatted_data.csv'
df = pd.read_csv(file_path)
app = dash.Dash(__name__)
app.title = '📊 Brand Analytics Dashboard'

app.layout = html.Div([
    html.H1("📊 Brand Analytics Dashboard", style={"textAlign": "center"}),
    html.Div(id='brand-filter-container', children=[
        html.Label("🏷️ Brand Filter:"),
        dcc.Dropdown(
            id='brand-filter',
            options=[{"label": brand, "value": brand} for brand in sorted(df["Brand"].dropna().unique())],
            multi=True,
            placeholder="Select brands..."
        )
    ], style={"width": "45%", "display": "inline-block", "padding": "10px"}),

    html.Div(id='location-filter-container', children=[
        html.Label("📍Location Filter:"),
        dcc.Dropdown(
            id='location-filter',
            options=[{"label": loc, "value": loc} for loc in sorted(df["Location"].dropna().unique())],
            multi=True,
            placeholder="Select multiple locations..."
        )
    ], style={"width": "45%", "display": "inline-block", "padding": "10px"}),

    html.Br(),

    dcc.Tabs(id='tabs', value='brand rating', children=[
        dcc.Tab(label='Average Rating by Brand', value='brand rating'),
        dcc.Tab(label='Average Price by Brand', value='brand price'),
        dcc.Tab(label='Brand Distribution Based on Seller Location', value='brand location'),
        dcc.Tab(label='Brand Popularity Map Based on Sales Volume per Location', value='brand popularity loc'),
        dcc.Tab(label='Brand Popularity by Price Volume', value='brand popularity price'),
        dcc.Tab(label='Popular Locations Based on Satisfaction Ratings', value='loc satisfaction'),
    ]),

    html.Div([
        html.Div(id='tabs-content'),
        html.Div(
            "LRyno",
            style={
                "textAlign": "center",
                "marginTop": "30px",
                "fontSize": "16px",
                "color": "gray",
                "fontStyle": "italic"
            }
        )
    ])
])

@app.callback(
    Output('brand-filter-container', 'style'),
    Output('location-filter-container', 'style'),
    Input('tabs', 'value'),
)

def toggle_filters(tab):
    show_brand = {'display': 'inline-block', 'width': '45%', 'padding': '10px'}
    show_location = {'display': 'inline-block', 'width': '45%', 'padding': '10px'}
    hide = {'display': 'none'}

    if tab in ['brand rating', 'brand price', 'brand popularity price']:
        return show_brand, hide
    elif tab in ['loc satisfaction']:
        return hide, show_location
    elif tab in ['brand location', 'brand popularity loc']:
        return show_brand, show_location
    else:
        return show_brand, show_location


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input('brand-filter', 'value'),
    Input('location-filter', 'value')
)

def update_chart(tab, selected_brands, selected_locations):
    filtered_df = df.copy()
    if tab in ['brand rating', 'brand price', 'brand popularity price']:
        if selected_brands:
            filtered_df = filtered_df[filtered_df["Brand"].isin(selected_brands)]
    if tab in ['loc satisfaction']:
        if selected_locations:
            filtered_df = filtered_df[filtered_df["Location"].isin(selected_locations)]
    if tab in ['brand location', 'brand popularity loc']:
        if selected_brands:
            filtered_df = filtered_df[filtered_df["Brand"].isin(selected_brands)]
        if selected_locations:
            filtered_df = filtered_df[filtered_df["Location"].isin(selected_locations)]
        
    if tab == 'brand rating':
        brand_rating = filtered_df.groupby(['Brand'])['Rating'].mean().round(1).sort_values().reset_index()
        fig = px.bar(
            brand_rating,
            x='Brand',
            y='Rating',
            hover_data=['Rating'],
            orientation='v',
            color='Rating',
            color_continuous_scale='Plasma',
            title='<b>Average Rating by Brand<b>',
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=500,
            paper_bgcolor='lightgray',
            plot_bgcolor='white',
            title_x=0.5,
            title_y=0.96,
            font_color='black',
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Rating: %{y}<extra></extra>",
            texttemplate='%{y}',
            textposition='inside',
            marker=dict(line=dict(color="#000000", width=1))
        )

        fig.update_coloraxes(colorbar=dict(
            title=dict(
                text="Rating<br>Scale", 
                font=dict(size=14),
            ),         
            tickvals=[1, 2, 3, 4],  
            ticktext=['1', '2', '3', '4'],
            ticks='inside',
            thickness=30,
            tickfont=dict(color='black')
        ))

    elif tab == 'brand price':
        brand_price = filtered_df.groupby(['Brand'])['Price (Rp)'].mean().round().sort_values().reset_index()
        fig = px.bar(
            brand_price, x='Brand', y='Price (Rp)',
            hover_data=['Price (Rp)'],
            orientation='v',
            color='Price (Rp)',
            title='<b>Average Price by Brand<b>'
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=500,
            paper_bgcolor='lightgray',
            plot_bgcolor='white',
            title_x=0.5,
            title_y=0.96,
            font_color='black',
        )

        fig.update_traces(
            customdata=brand_price['Price (Rp)'] / 1000000,
            hovertemplate="<b>%{x}</b><br>Price (Rp): %{customdata:.1f}M<extra></extra>",
            texttemplate='%{customdata:.1f}M',
            textposition='outside',
            marker=dict(line=dict(color='#ffffff', width=0.5))
        )

    elif tab == 'brand location':
        brand_location = filtered_df.groupby(['Brand'])['Location'].value_counts().reset_index().rename(columns={'count':'Count'})
        fig = px.density_heatmap(
            brand_location,
            x='Brand', 
            y='Location',
            z='Count',
            height=600,
            title='<b>Brand Distribution Based on Seller Location<b>',
            hover_data={
            'Brand': True,
            'Location': True,
            }
        )

        fig.update_traces(
            hovertemplate="<br>".join([
                "<b>%{x}",
                "<b>Location</b>: %{y}",
                "<b>Count</b>: %{z}",
                "<extra></extra>"
            ])
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='lightgray',
            plot_bgcolor='white',
            title_x=0.5,
            title_y=0.97,
            font_color='black',
            xaxis=dict(
                tickangle=45
            )
        )

        fig.update_coloraxes(colorbar=dict(
            title='Count',
        ))

    elif tab == 'brand popularity loc':
        brand_popularity_loc = filtered_df.groupby(['Brand', 'Location'])['Sold'].sum().reset_index()
        fig = px.treemap(
            brand_popularity_loc,
            path=['Brand','Location'],
            values='Sold',
            title='<b>Brand Popularity Map Based on Sales Volume per Location<b>',
            height=600,
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='lightgray',
            title_y=0.97,
            title_x=0.02,
            font_color='black',
            font_size=13
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Sold: %{value}<br>Brand: %{parent}<extra></extra>",
            marker=dict(line=dict(color='#ffffff', width=0.5)),
            textposition="middle center",
            texttemplate="<b>%{label}</b><br>Sold: %{value}",
        )

    elif tab == 'brand popularity price':
        brand_popularity_price = filtered_df.groupby(['Brand', 'Price (Rp)'])['Sold'].sum().reset_index()
        def format_rupiah(x):
            return f"Rp{x:,.0f}".replace(",", ".")
        brand_popularity_price['Price Format'] = brand_popularity_price['Price (Rp)'].apply(format_rupiah)
        fig = px.treemap(
            brand_popularity_price,
            path=['Brand','Price Format'],
            values='Sold',
            title='<b>Brand Popularity by Price Volume<b>',
            height=600,
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='lightgray',
            title_y=0.97,
            font_color='black',
            font_size=15
        )

        fig.update_traces(
            hovertemplate="<b>Price: %{label}</b><br>Sold: %{value}<br>Brand: %{parent}<extra></extra>",
            marker=dict(line=dict(color='#ffffff', width=0.5)),
            textposition="middle center",
            texttemplate="<b>%{label}</b><br>Sold: %{value}",
        )

    elif tab == 'loc satisfaction':
        loc_sold = filtered_df.groupby(['Location'])['Sold'].sum().reset_index()
        loc_rate = filtered_df.groupby(['Location'])['Rating'].mean().round(1)
        loc_satisfaction = pd.merge(loc_sold, loc_rate, on='Location').rename(columns={'Sold':'Popularity', 'Rating':'Satisfaction'})
        loc_satisfaction = loc_satisfaction.sort_values(by='Popularity', ascending=False).reset_index().drop(columns='index')
        loc_satisfaction['Size'] = 1
        fig = px.bar(
            loc_satisfaction,
            x="Popularity",
            y="Location",
            orientation='h',
            color="Satisfaction",
            color_continuous_scale="RdYlGn",
            title="<b>Popular Locations Based on Satisfaction Ratings<b>",
            custom_data=['Satisfaction']
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=800,
            paper_bgcolor='lightgray',
            plot_bgcolor='white',
            title_x=0.5,
            title_y=0.98,
            font_size=13,
            font_color='black',
        )

        fig.update_traces(
            customdata = np.column_stack((
            loc_satisfaction['Popularity'],
            loc_satisfaction['Satisfaction']
        )),
            hovertemplate="<b>%{y}</b><br>Satisfaction: %{customdata[1]}<br>Popularity: %{customdata[0]:.1f}K<extra></extra>",
            texttemplate='%{customdata[0]}',
            textposition='outside',
            marker=dict(line=dict(color="#000000", width=0.5)),
            textfont=dict(size=30, color='black')
        )

        fig.update_coloraxes(colorbar=dict(
            title=dict(
                text="Satisfaction", 
                font=dict(size=14),
            ),         
            tickvals=[1, 2, 3, 4],  
            ticktext=['1', '2', '3', '4'],
            ticks='inside',
            thickness=30,
            tickfont=dict(color='black')
        ))

    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run(debug=True)