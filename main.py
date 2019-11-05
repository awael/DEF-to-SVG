#import drawSvg as draw
import svgwrite as draw
from def_parser import *
from lef_parser import *
# read_path = "./libraries/DEF/c880_tri.def"
def_path = "./libraries/DEF/ispd18_test1.input.def"
def_parser = DefParser(def_path)
def_parser.parse()
a = np.array(list(def_parser.diearea))
#print(a)

b = np.array(list(def_parser.components))
print(def_parser.components.comps[612].placed)
lef_path = "./libraries/FreePDK45/ispd18_test1.input.lef"
lef_parser = LefParser(lef_path)
lef_parser.parse()

#print(def_parser.pins)
#def_parser.pins
e = np.array(list(def_parser.nets))
#print(e[0])

def_parser.components.comps[0].name
def_parser.components.comps[0].placed
#lef_parser.macro_dict[def_parser.components.comps[0].name].info['SIZE']

#d = draw.Drawing(height = def_parser.diearea[1][0]-def_parser.diearea[0][0], width = def_parser.diearea[1][1]-def_parser.diearea[0][1])
d = draw.Drawing('./try this.svg', size = (def_parser.diearea[1][1]-def_parser.diearea[0][1],def_parser.diearea[1][0]-def_parser.diearea[0][0]))

# draw a red box
d.add(d.rect((100, 100), (300, 200),fill='blue',fill_opacity=0.5))
d.saveas("./try this.svg")


