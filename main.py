#import drawSvg as draw
import svgwrite as draw
from def_parser import *
from lef_parser import *
import random

def_path = "./libraries/DEF/spi_ctl.def"
def_parser = DefParser(def_path)
def_parser.parse()
a = np.array(list(def_parser.diearea))
#print(a)

b = np.array(list(def_parser.components))
#print(def_parser.components.comps[612].placed)
lef_path = ".\\libraries\\LEF\\osu035_stdcells.lef"
lef_parser = LefParser(lef_path)
lef_parser.parse()

#print(def_parser.pins)
#def_parser.pins
e = np.array(list(def_parser.nets))
#print(e[0])

#d = draw.Drawing(height = def_parser.diearea[1][0]-def_parser.diearea[0][0], width = def_parser.diearea[1][1]-def_parser.diearea[0][1])
d = draw.Drawing('./new2.svg', size = (def_parser.diearea[1][1]-def_parser.diearea[0][1],def_parser.diearea[1][0]-def_parser.diearea[0][0]))


#print(def_parser.components.num_comps)
for component in def_parser.components.comps:
    # print(component.name)
    # print(component.placed)
    # print(lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'])
    # print("----------------------------------")
    d.add(draw.shapes.Rect((component.placed[0], component.placed[1]), (lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][0], lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][1]), fill='#39ff14', fill_opacity=0.5))
# print(def_parser.nets.nets[0].routed[0].points)
# print(def_parser.nets.nets[0].routed[0].end_via_loc)
# print(def_parser.nets.nets[0].routed[0].end_via)
# print(def_parser.nets.nets[0].routed[0].layer)
# print(def_parser.nets.nets[0].routed[0].type)
# print(def_parser.nets.nets[0].routed[0])
# print(len(def_parser.nets.nets[0].routed))

j = 0
colors = dict()
x = list(lef_parser.layer_dict.keys())
while j < len(lef_parser.layer_dict):
    colors.update({x[j]:("#"+''.join([random.choice('0123456789ABCDEF') for l in range(6)]))})
    j=j+1
print(colors)
j = 0
while j < def_parser.nets.num_nets:
    i = 0
    while i < len(def_parser.nets.nets[j].routed):
        # d.add(draw.shapes.Rect(def_parser.nets.nets[j].routed[i].points[0], def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1], stroke=colors[def_parser.nets.nets[j].routed[i].layer]))
        if def_parser.nets.nets[j].routed[i].points[0][0] == def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points) - 1][0]:
            # x coordinates match --> vertical layer
            d.add(draw.shapes.Rect(def_parser.nets.nets[j].routed[i].points[0], (lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width,(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][1]-def_parser.nets.nets[j].routed[i].points[0][1])),fill_opacity = 0.5,fill = colors[def_parser.nets.nets[j].routed[i].layer]))
        else:
            #horizontal layer
            d.add(draw.shapes.Rect(def_parser.nets.nets[j].routed[i].points[0], ((def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1][0]-def_parser.nets.nets[j].routed[i].points[0][0]),lef_parser.layer_dict[def_parser.nets.nets[j].routed[i].layer].width),fill_opacity = 0.5,fill = colors[def_parser.nets.nets[j].routed[i].layer] ))


        # print(def_parser.nets.nets[j].routed[i].points[0])
        # print(def_parser.nets.nets[j].routed[i].points[len(def_parser.nets.nets[j].routed[i].points)-1])
        # print(def_parser.nets.nets[j].routed[i].layer)
        # print(def_parser.nets.nets[j].routed[i].end_via)
        i=i+1
    j=j+1

# def_parser.nets.nets[j-1].routed[i-1].end_via
# print(lef_parser.layer_dict['metal1'].width)
# print(def_parser.nets.nets[0].routed[0].layer)

#print(def_parser.nets.nets[1].routed[1].end_via) 
#print(def_parser.nets.nets[1].routed[1].end_via_loc) // to get vias coordinates

#print(def_parser.nets.nets[0])

# print(def_parser.pins.pins)
# print(colors)
d.saveas("./new2.svg")


