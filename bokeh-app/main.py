import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource,
                          HoverTool, Label, SingleIntervalTicker, Slider)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure

import os
DIRECTORY_PATH = "./renta"
files = [ file_path  for _, _, file_path in os.walk(DIRECTORY_PATH)]
#for file_name in files[0]: #note that it has list of lists
#    print(file_name)

numberList = [item.replace('renta', '') for item in files[0]]
numberList = [item.replace('.txt', '') for item in numberList]
numberList = [int(item) for item in numberList]

numberList = np.array(numberList)
#print("Min date = {:d}".format(numberList.min()))
#print("Max date = {:d}".format(numberList.max()))

print("Min date = {min}, Max date = {max}.".format(min = numberList.min(), max = numberList.max()))

all_df_dict = {}
kk = 0 
for file in files[0]:
    filePath = 'C:/Users/cvale/Dropbox/BCCH/Proyecto_Renta/renta/' + file
    df = pd.read_table(filePath, sep = ',')
    all_df_dict.update({str(kk): df})
    kk += 1



data = {}


source = ColumnDataSource(data=all_df_dict['0']) 
TOOLS = 'save,pan,box_zoom,reset,wheel_zoom'
p = figure(title="Kernel de distribución de renta", y_axis_type="linear", plot_height = 400,
           tools = TOOLS, plot_width = 800)

p.vbar(x = 'x', top = 'y', color = 'grey', width = np.min(np.abs(np.array(source.data['x'])[0:-2] - np.array(source.data['x'])[1:-1]))          , visible  = True, source = source)

p.add_tools(HoverTool(tooltips=[("Renta", "@x"), ("Densidad", "@top")]))

p.xaxis.axis_label = 'Renta'
p.yaxis.axis_label = 'Densidad'





def slider_update(attrname, old, new):
    year = slider.value
    # label.text = str(year)
    source.data = all_df_dict[str(year)]

slider = Slider(start=0, end=len(all_df_dict) - 1, value=0, step=1, title="Year")
slider.on_change('value', slider_update)

callback_id = None


def animate_update():
    year = slider.value + 1
    if year > len(all_df_dict):
        year = years[0]
    slider.value = year

def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=60)
button.on_click(animate)

layout = layout([
    [p],
    [slider, button],
], sizing_mode='scale_width')


curdoc().add_root(layout)
curdoc().title = "Gapminder"

"""
in terminal use: bokeh serve --show myapp.py

"""