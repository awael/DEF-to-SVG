#import drawSvg as draw
import svgwrite as draw
from def_parser import *
from lef_parser import *
# read_path = "./libraries/DEF/c880_tri.def"
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
d = draw.Drawing('./try this.svg', size = (def_parser.diearea[1][1]-def_parser.diearea[0][1],def_parser.diearea[1][0]-def_parser.diearea[0][0]))


#print(def_parser.components.num_comps)
for component in def_parser.components.comps:
    #print(component.name)
    #print(component.placed)
    #print(lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'])
    #print("----------------------------------")
    d.add(d.rect((component.placed[0], component.placed[1]), (lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][0], lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'][1]), fill='#39ff14', fill_opacity=0.5))
print(def_parser.nets.nets[580])
#the above object has attributes:
# .end_via
# .layer
# .end_via_loc
# .points
# .type, we need to use these with the svg element polyLine to create wires and place vias when needed in different colors.


d.saveas("./try this.svg")


