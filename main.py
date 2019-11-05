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
lef_path = "C:\\Users\\ahmed\\OneDrive\\Documents\\FALL 19\\Digital 2\\MiniProject\\lef-parser-master\\DEF-to-SVG\\libraries\\LEF\\osu035_stdcells.lef"
lef_parser = LefParser(lef_path)
lef_parser.parse()

#print(def_parser.pins)
#def_parser.pins
e = np.array(list(def_parser.nets))
#print(e[0])


print(def_parser.components.num_comps)
for component in def_parser.components.comps:
    print(component.name)
    print(component.placed)
    print(lef_parser.macro_dict[component.name.split("_")[0]].info['SIZE'])
    print("----------------------------------")

#d = draw.Drawing(height = def_parser.diearea[1][0]-def_parser.diearea[0][0], width = def_parser.diearea[1][1]-def_parser.diearea[0][1])
d = draw.Drawing('./try this.svg', size = (def_parser.diearea[1][1]-def_parser.diearea[0][1],def_parser.diearea[1][0]-def_parser.diearea[0][0]))

# draw a red box
d.add(d.rect((100, 100), (300, 200),fill='blue',fill_opacity=0.5))
d.saveas("./try this.svg")


