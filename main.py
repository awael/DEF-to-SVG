#import drawSvg as draw
import svgwrite as draw
from def_parser import *

# read_path = "./libraries/DEF/c880_tri.def"
read_path = "./libraries/DEF/spi_ctl.def"
def_parser = DefParser(read_path)
def_parser.parse()
a = np.array(list(def_parser.diearea))
#print(a)
b = np.array(list(def_parser.components))
#print(b[0])

#print(def_parser.pins)
#def_parser.pins
e = np.array(list(def_parser.nets))
#print(e[0])

#d = draw.Drawing(height = def_parser.diearea[1][0]-def_parser.diearea[0][0], width = def_parser.diearea[1][1]-def_parser.diearea[0][1])
d = draw.Drawing('svgwrite-example.svg', profile='tiny')

# draw a red box
d.add(d.rect((10, 10), (300, 200),fill='blue',fill_opacity=0.5))
d.saveas("./try this.svg")
