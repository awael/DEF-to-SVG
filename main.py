import svgwrite as draw
from def_parser import *
from lef_parser import *
import numpy as np
import random
import math
from svgutils import transform
from svgutils import compose
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtGui import *
from cairosvg import svg2png

#"./libraries/DEF/spi_ctl.def"
def_path = input("Enter def file path: ")

def_parser = DefParser(def_path)
def_parser.parse() #call def parser

# ".\\libraries\\LEF\\osu035_stdcells.lef"
lef_path = input("Enter lef file path: ")
# lef_path = ".\\libraries\\LEF\\osu035_stdcells.lef"

lef_parser = LefParser(lef_path)
lef_parser.parse() #call lef parser

boolean = input("Do you want to highlight clock tree (DFF and CLK nets)? [1:yes,0:no]") #Prompt user for highlight option
boolean = int(boolean)
SCALE = int(def_parser.scale)

#construct color table
j=0
colors = dict()
x = list(lef_parser.layer_dict.keys())
while j < len(lef_parser.layer_dict):
    colors.update({x[j]:("#"+''.join([random.choice('0123456789ABCDEF') for l in range(6)]))})
    j=j+1
print(colors)

d = draw.Drawing('./output.svg', size = (int((def_parser.diearea[1][0]-def_parser.diearea[0][0])*1.15),int((def_parser.diearea[1][1]-def_parser.diearea[0][1]))*1.15))
d.add(draw.shapes.Rect((0,0), (
def_parser.diearea[1][0]-def_parser.diearea[0][0],
def_parser.diearea[1][1]-def_parser.diearea[0][1]), fill='#ffffff', fill_opacity=0.1,
                       stroke_width=8, stroke='black'))

#draw components and their inner OBS and layers, highlight if selected
for component in def_parser.components.comps:
    if (boolean == 0):
        d.add(draw.shapes.Rect((component.placed[0], component.placed[1]), (
            lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][0] * SCALE,
            lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][1] * SCALE), fill='#ffb330',
                               fill_opacity=0.5,
                               stroke_width=8, stroke='black'))
        z = 0
        # print(component.name.split("_")[0])
        while z < len(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict.keys()):
            pin_name = list(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict.keys())
            y=0
            while y < len(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info['LAYER'][0].shapes):
                zz=lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info['LAYER'][0].shapes[y].points[0][0]*SCALE
                zo=lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info['LAYER'][0].shapes[y].points[0][1]*SCALE
                oz=lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info['LAYER'][0].shapes[y].points[1][0]*SCALE
                oo=lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info['LAYER'][0].shapes[y].points[1][1]*SCALE
                d.add(draw.shapes.Rect((component.placed[0]+(zz), component.placed[1]+zo), (
                        (oz-zz),
                        (oo-zo)), fill=colors[lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info['LAYER'][0].name],
                                           fill_opacity=0.3,
                                           stroke_width=2, stroke='black'))
                y=y+1
            y=0
            if 'OBS' in (list(lef_parser.macro_dict[component.name.split("_")[0]].info.keys())):
            # print(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[1].points)
            # if ()
            #     print(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].name)
                while y < len(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes):
                    zz=lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[y].points[0][0]*SCALE
                    zo=lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[y].points[0][1]*SCALE
                    oz=lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[y].points[1][0]*SCALE
                    oo=lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[y].points[1][1]*SCALE
                    d.add(draw.shapes.Rect((component.placed[0] + (zz), component.placed[1] + zo), (
                        (oz - zz),
                        (oo - zo)), fill=colors[lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].name],
                                           fill_opacity=0.3,
                                           stroke_width=2, stroke='black'))
                    y=y+1
            z=z+1
    else:
        if 'DFF' in component.name:

            d.add(draw.shapes.Rect((component.placed[0], component.placed[1]), (
                lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][0] * SCALE,
                lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][1] * SCALE), fill='#e1ff00',
                                   fill_opacity=0.5,
                                   stroke_width=8, stroke='black'))
            z = 0
            # print(component.name.split("_")[0])
            while z < len(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict.keys()):
                pin_name = list(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict.keys())
                y = 0
                while y < len(
                        lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                            'LAYER'][0].shapes):
                    zz = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[0][0] * SCALE
                    zo = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[0][1] * SCALE
                    oz = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[1][0] * SCALE
                    oo = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[1][1] * SCALE
                    d.add(draw.shapes.Rect((component.placed[0] + (zz), component.placed[1] + zo), (
                        (oz - zz),
                        (oo - zo)), fill=colors[
                        lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                            'LAYER'][0].name],
                                           fill_opacity=0.3,
                                           stroke_width=2, stroke='black'))
                    y = y + 1
                y = 0
                if 'OBS' in (list(lef_parser.macro_dict[component.name.split("_")[0]].info.keys())):
                    # print(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[1].points)
                    # if ()
                    #     print(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].name)
                    while y < len(
                            lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes):
                        zz = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[0][0] * SCALE
                        zo = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[0][1] * SCALE
                        oz = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[1][0] * SCALE
                        oo = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[1][1] * SCALE
                        d.add(draw.shapes.Rect((component.placed[0] + (zz), component.placed[1] + zo), (
                            (oz - zz),
                            (oo - zo)), fill=colors[
                            lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].name],
                                               fill_opacity=0.3,
                                               stroke_width=2, stroke='black'))
                        y = y + 1
                z = z + 1

        else:
            d.add(draw.shapes.Rect((component.placed[0], component.placed[1]), (
                lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][0] * SCALE,
                lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][1] * SCALE), fill='#ffb330',
                                   fill_opacity=0.5,
                                   stroke_width=8, stroke='black'))
            z = 0
            # print(component.name.split("_")[0])
            while z < len(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict.keys()):
                pin_name = list(lef_parser.macro_dict[component.name.split("_")[0]].pin_dict.keys())
                y = 0
                while y < len(
                        lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                            'LAYER'][0].shapes):
                    zz = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[0][0] * SCALE
                    zo = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[0][1] * SCALE
                    oz = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[1][0] * SCALE
                    oo = lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                             'LAYER'][0].shapes[y].points[1][1] * SCALE
                    d.add(draw.shapes.Rect((component.placed[0] + (zz), component.placed[1] + zo), (
                        (oz - zz),
                        (oo - zo)), fill=colors[
                        lef_parser.macro_dict[component.name.split("_")[0]].pin_dict[pin_name[z]].info['PORT'].info[
                            'LAYER'][0].name],
                                           fill_opacity=0.3,
                                           stroke_width=2, stroke='black'))
                    y = y + 1
                y = 0
                if 'OBS' in (list(lef_parser.macro_dict[component.name.split("_")[0]].info.keys())):
                    # print(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[1].points)
                    # if ()
                    #     print(lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].name)
                    while y < len(
                            lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes):
                        zz = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[0][0] * SCALE
                        zo = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[0][1] * SCALE
                        oz = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[1][0] * SCALE
                        oo = lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].shapes[
                                 y].points[1][1] * SCALE
                        d.add(draw.shapes.Rect((component.placed[0] + (zz), component.placed[1] + zo), (
                            (oz - zz),
                            (oo - zo)), fill=colors[
                            lef_parser.macro_dict[component.name.split("_")[0]].info['OBS'].info['LAYER'][0].name],
                                               fill_opacity=0.3,
                                               stroke_width=2, stroke='black'))
                        y = y + 1
                z = z + 1

j = 0



#draw nets highlighting clock if selected
j = 0
while j < def_parser.nets.num_nets:
    i = 0
    if (boolean == 0):
        while i < len(def_parser.nets.nets[j].routed):
            if def_parser.nets.nets[j].routed[i].points[0][0] == def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][0]:
                # x coordinates match --> vertical layer
                XC = def_parser.nets.nets[j].routed[i].points[0][0] - (lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width*SCALE) /2
                if(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][1]-def_parser.nets.nets[j].routed[i].points[0][1] > 0):
                    d.add(draw.shapes.Rect((XC,def_parser.nets.nets[j].routed[i].points[0][1]), (lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width*SCALE, (def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][1]-def_parser.nets.nets[j].routed[i].points[0][1])),fill_opacity = 0.5,fill = colors[def_parser.nets.nets[j].routed[i].layer]))
                else:
                    d.add(draw.shapes.Rect((XC,def_parser.nets.nets[j].routed[i].points[0][1]-abs(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][1]-def_parser.nets.nets[j].routed[i].points[0][1])), (lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width*SCALE, abs(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][1]-def_parser.nets.nets[j].routed[i].points[0][1])),fill_opacity = 0.5,fill = colors[def_parser.nets.nets[j].routed[i].layer]))

            else:
                #horizontal layer
                YC = def_parser.nets.nets[j].routed[i].points[0][1] - (lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width*SCALE) /2
                if ((def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][0]-def_parser.nets.nets[j].routed[i].points[0][0]) > 0):
                    d.add(draw.shapes.Rect((def_parser.nets.nets[j].routed[i].points[0][0], YC), ((def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][0]-def_parser.nets.nets[j].routed[i].points[0][0]),lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width*SCALE),fill_opacity = 0.5,fill = colors[def_parser.nets.nets[j].routed[i].layer] ))
                else:
                    d.add(draw.shapes.Rect((def_parser.nets.nets[j].routed[i].points[0][0]-abs(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][0]-def_parser.nets.nets[j].routed[i].points[0][0]), YC), (abs(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][0]-def_parser.nets.nets[j].routed[i].points[0][0]),lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width*SCALE),fill_opacity = 0.5,fill = colors[def_parser.nets.nets[j].routed[i].layer] ))
            k = 0
            if def_parser.nets.nets[j].routed[i].end_via != None and def_parser.nets.nets[j].routed[i].end_via != ';':
                while k < 3:
                    via_w = (lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[0].points[1][0] - lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[0].points[0][0])*SCALE
                    via_h = (lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[0].points[1][1] - lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[0].points[0][1])*SCALE
                    XC = def_parser.nets.nets[j].routed[i].end_via_loc[0] - via_w/2
                    YC = def_parser.nets.nets[j].routed[i].end_via_loc[1] - via_h/2
                    d.add(draw.shapes.Rect((XC,YC), (via_w, via_h),fill_opacity = 0.5, fill = colors[lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[1].name]))
                    k=k+1
            i=i+1
        j=j+1
    else:
        if 'clk' in def_parser.nets.nets[j].name:
            while i < len(def_parser.nets.nets[j].routed):
                if def_parser.nets.nets[j].routed[i].points[0][0] == \
                        def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][0]:
                    # x coordinates match --> vertical layer
                    XC = def_parser.nets.nets[j].routed[i].points[0][0] - (
                                lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width * SCALE) / 2
                    if (def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][1] -
                            def_parser.nets.nets[j].routed[i].points[0][1] > 0):
                        d.add(draw.shapes.Rect((XC, def_parser.nets.nets[j].routed[i].points[0][1]), (
                        lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width * SCALE, (
                                    def_parser.nets.nets[j].routed[i].points[
                                        len(def_parser.nets.nets[j].routed[i].points) - 1][1] -
                                    def_parser.nets.nets[j].routed[i].points[0][1])), fill_opacity=0.5,
                                               fill='#e1ff00'))
                    else:
                        d.add(draw.shapes.Rect((XC, def_parser.nets.nets[j].routed[i].points[0][1] - abs(
                            def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                                1] - def_parser.nets.nets[j].routed[i].points[0][1])), (lef_parser.layer_dict[
                                                                                            def_parser.nets.nets[
                                                                                                j].routed[
                                                                                                i].layer].width * SCALE,
                                                                                        abs(def_parser.nets.nets[
                                                                                                j].routed[i].points[len(
                                                                                            def_parser.nets.nets[
                                                                                                j].routed[
                                                                                                i].points) - 1][1] -
                                                                                            def_parser.nets.nets[
                                                                                                j].routed[i].points[0][
                                                                                                1])), fill_opacity=0.5,
                                               fill='#e1ff00'))

                else:
                    # horizontal layer
                    YC = def_parser.nets.nets[j].routed[i].points[0][1] - (
                                lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width * SCALE) / 2
                    if ((def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                             0] - def_parser.nets.nets[j].routed[i].points[0][0]) > 0):
                        d.add(draw.shapes.Rect((def_parser.nets.nets[j].routed[i].points[0][0], YC), ((
                                                                                                                  def_parser.nets.nets[
                                                                                                                      j].routed[
                                                                                                                      i].points[
                                                                                                                      len(
                                                                                                                          def_parser.nets.nets[
                                                                                                                              j].routed[
                                                                                                                              i].points) - 1][
                                                                                                                      0] -
                                                                                                                  def_parser.nets.nets[
                                                                                                                      j].routed[
                                                                                                                      i].points[
                                                                                                                      0][
                                                                                                                      0]),
                                                                                                      lef_parser.layer_dict[
                                                                                                          def_parser.nets.nets[
                                                                                                              j].routed[
                                                                                                              i].layer].width * SCALE),
                                               fill_opacity=0.5, fill='#e1ff00'))
                    else:
                        d.add(draw.shapes.Rect((def_parser.nets.nets[j].routed[i].points[0][0] - abs(
                            def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                                0] - def_parser.nets.nets[j].routed[i].points[0][0]), YC), (abs(
                            def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                                0] - def_parser.nets.nets[j].routed[i].points[0][0]), lef_parser.layer_dict[
                                                                                                def_parser.nets.nets[
                                                                                                    j].routed[
                                                                                                    i].layer].width * SCALE),
                                               fill_opacity=0.5, fill='#e1ff00'))
                k = 0
                if def_parser.nets.nets[j].routed[i].end_via != None and def_parser.nets.nets[j].routed[
                    i].end_via != ';':
                    while k < 3:
                        via_w = (lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[1][0] -
                                 lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[0][0]) * SCALE
                        via_h = (lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[1][1] -
                                 lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[0][1]) * SCALE
                        XC = def_parser.nets.nets[j].routed[i].end_via_loc[0] - via_w / 2
                        YC = def_parser.nets.nets[j].routed[i].end_via_loc[1] - via_h / 2
                        d.add(draw.shapes.Rect((XC, YC), (via_w, via_h), fill_opacity=0.5, fill=colors[
                            lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[1].name]))
                        k = k + 1
                i = i + 1
            j = j + 1
        else:
            while i < len(def_parser.nets.nets[j].routed):
                if def_parser.nets.nets[j].routed[i].points[0][0] == \
                        def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][0]:
                    # x coordinates match --> vertical layer
                    XC = def_parser.nets.nets[j].routed[i].points[0][0] - (
                                lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width * SCALE) / 2
                    if (def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][1] -
                            def_parser.nets.nets[j].routed[i].points[0][1] > 0):
                        d.add(draw.shapes.Rect((XC, def_parser.nets.nets[j].routed[i].points[0][1]), (
                        lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width * SCALE, (
                                    def_parser.nets.nets[j].routed[i].points[
                                        len(def_parser.nets.nets[j].routed[i].points) - 1][1] -
                                    def_parser.nets.nets[j].routed[i].points[0][1])), fill_opacity=0.5,
                                               fill=colors[def_parser.nets.nets[j].routed[i].layer]))
                    else:
                        d.add(draw.shapes.Rect((XC, def_parser.nets.nets[j].routed[i].points[0][1] - abs(
                            def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                                1] - def_parser.nets.nets[j].routed[i].points[0][1])), (lef_parser.layer_dict[
                                                                                            def_parser.nets.nets[
                                                                                                j].routed[
                                                                                                i].layer].width * SCALE,
                                                                                        abs(def_parser.nets.nets[
                                                                                                j].routed[i].points[len(
                                                                                            def_parser.nets.nets[
                                                                                                j].routed[
                                                                                                i].points) - 1][1] -
                                                                                            def_parser.nets.nets[
                                                                                                j].routed[i].points[0][
                                                                                                1])), fill_opacity=0.5,
                                               fill=colors[def_parser.nets.nets[j].routed[i].layer]))

                else:
                    # horizontal layer
                    YC = def_parser.nets.nets[j].routed[i].points[0][1] - (
                                lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width * SCALE) / 2
                    if ((def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                             0] - def_parser.nets.nets[j].routed[i].points[0][0]) > 0):
                        d.add(draw.shapes.Rect((def_parser.nets.nets[j].routed[i].points[0][0], YC), ((
                                                                                                                  def_parser.nets.nets[
                                                                                                                      j].routed[
                                                                                                                      i].points[
                                                                                                                      len(
                                                                                                                          def_parser.nets.nets[
                                                                                                                              j].routed[
                                                                                                                              i].points) - 1][
                                                                                                                      0] -
                                                                                                                  def_parser.nets.nets[
                                                                                                                      j].routed[
                                                                                                                      i].points[
                                                                                                                      0][
                                                                                                                      0]),
                                                                                                      lef_parser.layer_dict[
                                                                                                          def_parser.nets.nets[
                                                                                                              j].routed[
                                                                                                              i].layer].width * SCALE),
                                               fill_opacity=0.5, fill=colors[def_parser.nets.nets[j].routed[i].layer]))
                    else:
                        d.add(draw.shapes.Rect((def_parser.nets.nets[j].routed[i].points[0][0] - abs(
                            def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                                0] - def_parser.nets.nets[j].routed[i].points[0][0]), YC), (abs(
                            def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][
                                0] - def_parser.nets.nets[j].routed[i].points[0][0]), lef_parser.layer_dict[
                                                                                                def_parser.nets.nets[
                                                                                                    j].routed[
                                                                                                    i].layer].width * SCALE),
                                               fill_opacity=0.5, fill=colors[def_parser.nets.nets[j].routed[i].layer]))
                k = 0
                if def_parser.nets.nets[j].routed[i].end_via != None and def_parser.nets.nets[j].routed[
                    i].end_via != ';':
                    while k < 3:
                        via_w = (lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[1][0] -
                                 lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[0][0]) * SCALE
                        via_h = (lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[1][1] -
                                 lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[k].shapes[
                                     0].points[0][1]) * SCALE
                        XC = def_parser.nets.nets[j].routed[i].end_via_loc[0] - via_w / 2
                        YC = def_parser.nets.nets[j].routed[i].end_via_loc[1] - via_h / 2
                        d.add(draw.shapes.Rect((XC, YC), (via_w, via_h), fill_opacity=0.5, fill=colors[
                            lef_parser.via_dict[def_parser.nets.nets[j].routed[i].end_via].layers[1].name]))
                        k = k + 1
                i = i + 1
            j = j + 1

for p in def_parser.pins.pins:
    if math.copysign(1, p.layer.points[1][0]) == math.copysign(1, p.layer.points[0][0]) and math.copysign(1, p.layer.points[1][1]) == math.copysign(1, p.layer.points[0][1]):
        d.add(draw.shapes.Rect((p.placed[0], p.placed[1]), (p.layer.points[1][0]-p.layer.points[0][0],p.layer.points[1][1]-p.layer.points[0][1]), fill_opacity = 0.5,fill = colors[p.layer.name]))
    else:
        d.add(draw.shapes.Rect((p.placed[0], p.placed[1]), (p.layer.points[1][0]-p.layer.points[0][0],p.layer.points[1][1]-p.layer.points[0][1]+def_parser.diearea[1][1]-def_parser.diearea[0][1]), fill_opacity = 0.5,fill = colors[p.layer.name]))





#save SVG in directory
d.saveas("./output.svg")

###############################################################################3
#Qt gui

#main class
class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(250, 241, 210)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
    #mousepress
    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)

#display window class
class Window(QtWidgets.QWidget):
    #initialization
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)
        # Button to change from drag/pan to getting pixel info
        self.btnPixInfo = QtWidgets.QToolButton(self)
        self.btnPixInfo.setText('Enter pixel info mode')
        self.btnPixInfo.clicked.connect(self.pixInfo)
        self.editPixInfo = QtWidgets.QLineEdit(self)
        self.editPixInfo.setReadOnly(True)
        self.viewer.photoClicked.connect(self.photoClicked)
        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnPixInfo)
        HBlayout.addWidget(self.editPixInfo)
        VBlayout.addLayout(HBlayout)
    #load saved image
    def loadImage(self):
        self.viewer.setPhoto(QtGui.QPixmap('./output.svg'))
        self.viewer.scale(1,-1)
    #toggles drag
    def pixInfo(self):
        self.viewer.toggleDragMode()
    #checks for click while dragging
    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(0, 0, 1920, 1080)
    window.show()
    sys.exit(app.exec_())

print('DONE')

