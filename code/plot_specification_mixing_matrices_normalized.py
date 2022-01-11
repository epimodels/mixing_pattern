import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

from bokeh.models import LinearColorMapper, ColorBar, FixedTicker
from bokeh.palettes import brewer, Viridis5, Category10
from bokeh.plotting import figure, show, output_file
from bokeh.models import Slider, HoverTool, Select, CustomJS, ColumnDataSource, FactorRange
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Panel, Tabs
from bokeh.transform import cumsum

plot_width_global = 510
plot_height_global = 510

initial_hid = 'Hospital-1'
initial_unit_name = '24-Hour Observation Area'

def plot_hm_age_matrix(df_age_matrix):

	#print(df_age_matrix.columns)
	source_all_age_matrix = ColumnDataSource(df_age_matrix)
	source_age_matrix = ColumnDataSource(
		data = dict(
			age_x = df_age_matrix['Hospital-1_24-Hour Observation Area_age_x'],
			age_y = df_age_matrix['Hospital-1_24-Hour Observation Area_age_y'],
			contact_count = df_age_matrix['Hospital-1_24-Hour Observation Area_contact_count'],
            normalized_contact_count = df_age_matrix['Hospital-1_24-Hour Observation Area_normalized_contact_count']
		)
	)

	########## Heatmap Plot Specifications Starts ############

	color_mapper = LinearColorMapper(palette="Viridis256", nan_color = '#d9d9d9')
	#color_mapper = LinearColorMapper(palette = palette, low = 0, high = max(source.data['contact_count']))
	color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=400, height=20, major_label_text_font_size="12pt",
	 location=(0,0), orientation='horizontal')
	TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
	hm_age = figure(title="Mixing Matrix by Age",
		x_range=(-5, 95),
		y_range=(-5, 95),
		plot_width=plot_width_global,
		plot_height=plot_height_global, tools=TOOLS,
		tooltips=[('Age-x', '@age_x'), ('Age-y', '@age_y'), ('value', '@normalized_contact_count')],
	)
	hm_age.rect(x='age_x', y='age_y', source=source_age_matrix, width=1, height=1,
	fill_color={'field': 'normalized_contact_count', 'transform': color_mapper}, line_color=None)

	color_bar.formatter.use_scientific = False
	color_bar.ticker.desired_num_ticks = 4
	hm_age.add_layout(color_bar, 'below')
	hm_age.xaxis.axis_label = 'Patient Age'
	hm_age.yaxis.axis_label = 'Patient Age'
	#hm_age.xaxis.major_label_orientation = pi/12

	hm_age.title.text_font_size = '12pt'
	hm_age.xaxis.axis_label_text_font_size = "15pt"
	hm_age.yaxis.axis_label_text_font_size = "15pt"
	hm_age.xaxis.major_label_text_font_size = "15pt"
	hm_age.yaxis.major_label_text_font_size = "15pt"


	axis_ticks = [-10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
	#hm.xaxis.ticker = axis_ticks
	#hm.yaxis.ticker = axis_ticks
	hm_age.xaxis.ticker = FixedTicker(ticks=axis_ticks)
	hm_age.yaxis.ticker = FixedTicker(ticks=axis_ticks)
	#print('returning from plot function..')
	########## Heatmap Plot Specifications Ends ############

	return hm_age, source_age_matrix, source_all_age_matrix


def plot_elixhauser_score_matrix_data(df_elix_score_mixing_matrix):

	source_elix_score_matrix = ColumnDataSource(
	    data = dict(
	        ElixhauserScore_x = df_elix_score_mixing_matrix['Hospital-1_24-Hour Observation Area_ElixhauserScore_x'],
	        ElixhauserScore_y = df_elix_score_mixing_matrix['Hospital-1_24-Hour Observation Area_ElixhauserScore_y'],
	        contact_count = df_elix_score_mixing_matrix['Hospital-1_24-Hour Observation Area_contact_count'],
	        normalized_contact_count = df_elix_score_mixing_matrix['Hospital-1_24-Hour Observation Area_normalized_contact_count']
	    )
	)
	source_all_elix_score_matrix = ColumnDataSource(df_elix_score_mixing_matrix)

################# ElixhauserScore Heatmap Plot Specification Starts ####################

	color_mapper = LinearColorMapper(palette="Viridis256", nan_color = '#d9d9d9')

	color_bar_normalized = ColorBar(color_mapper=color_mapper, label_standoff=8, width=400, height=20,
	                         location=(0,0), orientation='horizontal', major_label_text_font_size='10pt')
	TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
	hm_elix_score_normalized = figure(title="Mixing Matrix by Elixhauser Score",
	           x_range=(-2, 20),
	           y_range=(-2, 20),
	           plot_width=plot_width_global,
	           plot_height=plot_height_global, tools=TOOLS,
	           tooltips=[('ElixhauserScore-x', '@ElixhauserScore_x'), ('ElixhauserScore-y', '@ElixhauserScore_y'), ('value', '@normalized_contact_count')],
	           )
	hm_elix_score_normalized.rect(x='ElixhauserScore_x', y='ElixhauserScore_y', source=source_elix_score_matrix, width=1, height=1,
	        fill_color={'field': 'normalized_contact_count', 'transform': color_mapper}, line_color=None)

	hm_elix_score_normalized.add_layout(color_bar_normalized, 'below')
	hm_elix_score_normalized.xaxis.axis_label = 'Elixhauser Score'
	#hm.xaxis.axis_label_text_font_size = "15pt"
	hm_elix_score_normalized.yaxis.axis_label = 'Elixhauser Score'
	#hm_elix_score_normalized.xaxis.major_label_orientation = pi/12

	hm_elix_score_normalized.title.text_font_size = '12pt'
	hm_elix_score_normalized.xaxis.axis_label_text_font_size = "15pt"
	hm_elix_score_normalized.yaxis.axis_label_text_font_size = "15pt"
	hm_elix_score_normalized.xaxis.major_label_text_font_size = "15pt"
	hm_elix_score_normalized.yaxis.major_label_text_font_size = "15pt"

	axis_ticks = [-2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	hm_elix_score_normalized.xaxis.ticker = FixedTicker(ticks=axis_ticks)
	hm_elix_score_normalized.yaxis.ticker = FixedTicker(ticks=axis_ticks)

	###### Creating tabbed layout ######

	#elix_score_tab1 = Panel(child=hm_elix_score, title='Elixhauser Score Mixing Pattern')
	#elix_score_tab2 = Panel(child=hm_elix_score_normalized, title='Elixhauser Score Mixing Pattern')


################# ElixhauserScore Heatmap Plot Specification Ends ####################

	return hm_elix_score_normalized, source_elix_score_matrix, source_all_elix_score_matrix


def plot_antibiotic_mixing(df_antibiotic_mixing):

    df_antibiotic_mixing = df_antibiotic_mixing.replace(
                                            {'a': 'Narrow',
                                            'b': 'Broad',
                                            'c': 'Extended',
                                            'd': 'Protected'
                                            })

    source_all_antibiotic_mixing_matrix = ColumnDataSource(df_antibiotic_mixing)
    source_antibiotic_mixing_matrix = ColumnDataSource(
        data = dict(
            rank_x = df_antibiotic_mixing['Hospital-1_24-Hour Observation Area_rank_x'],
            rank_y = df_antibiotic_mixing['Hospital-1_24-Hour Observation Area_rank_y'],
			freq = df_antibiotic_mixing['Hospital-1_24-Hour Observation Area_freq'],
			normalized_freq = df_antibiotic_mixing['Hospital-1_24-Hour Observation Area_normalized_freq']
        )
    )

    ########## Antibiotic Rank Heatmap Plot Specifications Starts ############

    color_mapper = LinearColorMapper(palette="Viridis256", nan_color = 'white')
	#color_mapper = LinearColorMapper(palette="Viridis256", nan_color = '#d9d9d9')
    #color_mapper = LinearColorMapper(palette = palette, low = 0, high = max(source.data['contact_count']))
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=400, height=20, major_label_text_font_size="12pt",
                             location=(0,0), orientation='horizontal')
    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
    hm_antibiotic_rank = figure(title="Mixing Matrix by Antibiotic Ranks",
               x_range=['Narrow', 'Broad', 'Extended', 'Protected'],
               y_range=['Narrow', 'Broad', 'Extended', 'Protected'],
               plot_width=plot_width_global,
               plot_height=plot_height_global, tools=TOOLS,
               tooltips=[('value', '@normalized_freq')],
               )
    hm_antibiotic_rank.rect(x='rank_x', y='rank_y', source=source_antibiotic_mixing_matrix, width=1, height=1,
            fill_color={'field': 'normalized_freq', 'transform': color_mapper}, line_color=None)

    color_bar.formatter.use_scientific = False
    #color_bar.formatter = NumeralTickFormatter(format='0.0')
    color_bar.ticker.desired_num_ticks = 4
    hm_antibiotic_rank.add_layout(color_bar, 'below')
    hm_antibiotic_rank.xaxis.axis_label = 'Antibiotic Spectrum'
    hm_antibiotic_rank.yaxis.axis_label = 'Antibiotic Spectrum'
    #hm_antibiotic_rank.xaxis.major_label_orientation = pi/12

    hm_antibiotic_rank.title.text_font_size = '12pt'
    hm_antibiotic_rank.xaxis.axis_label_text_font_size = "15pt"
    hm_antibiotic_rank.yaxis.axis_label_text_font_size = "15pt"
    hm_antibiotic_rank.xaxis.major_label_text_font_size = "15pt"
    hm_antibiotic_rank.yaxis.major_label_text_font_size = "15pt"
	#hm_antibiotic_rank.xaxis.major_label_orientation = pi/4


    ########## Antibiotic Rank Heatmap Plot Specifications Ends ############

    return hm_antibiotic_rank, source_antibiotic_mixing_matrix, source_all_antibiotic_mixing_matrix

def plot_no_antibiotic_ratio_pie_chart(data_no_antibiotic_ratio):
	#df_pie_chart = data_no_antibiotic_ratio.copy()
	data_no_antibiotic_ratio['color'] = ['blue', 'orange', 'yellow']
	source_all_pie_chart = ColumnDataSource(data_no_antibiotic_ratio)
	source_pie_chart = ColumnDataSource(
		data = dict(
			type = data_no_antibiotic_ratio['type'],
			value = data_no_antibiotic_ratio['Hospital-1_24-Hour Observation Area_value'],
			percentage = data_no_antibiotic_ratio['Hospital-1_24-Hour Observation Area_percentage'],
			angle = data_no_antibiotic_ratio['Hospital-1_24-Hour Observation Area_percentage'] * 2 * pi,
			color = data_no_antibiotic_ratio['color']
			#color = Category10[len(data_no_antibiotic_ratio)]
		)
	)
	TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
	pie_chart = figure(title="Pie chart of antibiotic exposure", plot_width=plot_width_global,
            plot_height=plot_height_global, tools=TOOLS,
			tooltips="@type: @percentage%")

	pie_chart.wedge(x=1, y=1, radius=0.4,
		start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
		line_color="white", fill_color='color', legend_field='type', source=source_pie_chart)

	return pie_chart, source_pie_chart, source_all_pie_chart

def plot_antibiotic_exposure_proportion_barchart(data_antibiotic_exposure_proportion):

	df = data_antibiotic_exposure_proportion.copy()
	source_all_barchart = ColumnDataSource(df)
	source_colname = initial_hid + '_' + initial_unit_name + '_percentage'
	data = {
	    'labs_barchart': ['Contacts(%)'],
	    'no_antibiotic': [df.at[0, source_colname]],
	    'one_antibiotic': [df.at[1, source_colname]],
	    'both_antibiotic': [df.at[2, source_colname]]
	}
	source_barchart = ColumnDataSource(data)

	#return source_barchart

	labs_barchart = ['Contacts(%)']	
	vals_barchart = ['no_antibiotic', 'one_antibiotic', 'both_antibiotic']
	legend_label_custom = ['Not Exposed Patient with Not Exposed Patient', 'Not Exposed Patient with Exposed Patient', 'Exposed Patient with Exposed Patient']
	colors = ['blue','orange','yellow']
	tooltips = [    	
    	("Not Exposed Patient with Not Exposed Patient:", "@no_antibiotic{0.00}"),
    	("Not Exposed Patient with Exposed Patient:", "@one_antibiotic{0.00}"),
    	("Exposed Patient with Exposed Patient:", "@both_antibiotic{0.00}")
	]

	bar_chart = figure(title="Antibiotic Exposed and Not Exposed Contacts", y_range=labs_barchart, plot_width = plot_width_global, plot_height = plot_height_global, tooltips=tooltips)

	bar_chart.hbar_stack(vals_barchart, y='labs_barchart', height=0.2, source=source_barchart, color=colors,
		legend_label=legend_label_custom)
	bar_chart.legend.location = "top_left"
	bar_chart.legend.orientation = "vertical"
	bar_chart.title.text_font_size = '12pt'
	bar_chart.yaxis.axis_label_text_font_size = "15pt"
	bar_chart.yaxis.major_label_text_font_size = "15pt"

	#show(p)
	return bar_chart, source_barchart, source_all_barchart
