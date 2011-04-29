# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# this is the factory for the page containing login form
# and also introductory materials


from luban.content import load, select, alert, createCredential
import luban.content as lc


class Factory(object):


    from vnf.deployment import html_base
    js_base = '%s/javascripts' % html_base
    chem_doodle_base = '%s/other/chemdoodle' % js_base
    
    
    def createViewer(self, matter, size=500):
        """create html content that has a matter viewer
        This is implemented by using chemdoodle
        """
        chem_doodle_base = self.chem_doodle_base
        script = self._createChemDoodleJS(matter, size)
        # script = self._createChemDoodleJSUsingPDB(matter, size)
        script = '\n'.join(script)
        text = page_template % locals()
        return text


    def createRibbonViewer(self, pdbcontent, size=500):
        """create html content that has a viewer showing ribbon
        This is implemented by using chemdoodle
        """
        chem_doodle_base = self.chem_doodle_base
        script = self._createChemDoodleJS_ribbon(pdbcontent, size)
        script = '\n'.join(script)
        text = page_template % locals()
        return text        


    def _createChemDoodleJS(self, matter, size):
        code = []
        # create mol
        code.append('var mol = new ChemDoodle.structures.Molecule();')
        code.append('var x,y,z;')
        # add atoms to mol
        sg = matter.sg
        lattice = matter.lattice
        atoms = getAtomsInOneUnitCell(matter)
        for count,atom in enumerate(atoms):
            symbol = atom.symbol
            # this is to avoid a bug in chemdoodle
            if symbol in buggyelements:
                symbol = 'Cu'
            x,y,z = lattice.cartesian(atom.xyz)
            code.append('x = scalefactor*%s;' % x)
            code.append('y = scalefactor*%s;' % y)
            code.append('z = scalefactor*%s;' % z)
            code.append('var atom%s = new ChemDoodle.structures.Atom("%s", x,y,z);' % (count, symbol))
            code.append('mol.atoms[%s]=atom%s;' % (count,count))
            continue
        # add mol to canvas
        code.append('canvas.loadMolecule(mol);')
        code.append('if (!webgl) {canvas.specs.scale = 2.5; canvas.repaint();}')
        code.append("var msg = 'Note: webgl is not supported by your browser. To get a better 3d view, you may want to try a webgl enabled browser such as firefox or google chrome';")
        code.append('if (!webgl) {$("body").append("<p/>").append("<div>"+msg+"</div>");}')

        add_mol_to_canvas = '\n'.join(code)
        #
        width = height = size
        #
        text = js_create_3dscene_template % locals()
        return [text]


    def _createChemDoodleJS_ribbon(self, pdbcontent, size):
        width = height = size
        pdb = pdbcontent.replace('\n', r'\n')
        text = js_create_ribbon_3dscene_template % locals()
        return [text]


page_template = '''
<html>
<head>
<link rel="stylesheet" href="%(chem_doodle_base)s/ChemDoodleWeb.css" type="text/css">
<script type="text/javascript" src="%(chem_doodle_base)s/ChemDoodleWeb-libs.js"></script>
<script type="text/javascript" src="%(chem_doodle_base)s/ChemDoodleWeb.js"></script>
<title>Matter viewer</title>
</head>
<body>

<div>
<script>
%(script)s
</script>
</div>

</body>
</html>
'''


js_create_3dscene_template = """
  // initialize component and set visual specifications
  var canvas, scalefactor;
  var webgl = ChemDoodle.featureDetection.supports_webgl(); 
  if (webgl) {
    canvas \
      = new ChemDoodle.TransformCanvas3D('canvas', %(width)s, %(height)s);
    // canvas.specs.set3DRepresentation('Ball and Stick');
    canvas.specs.set3DRepresentation('Stick');
    canvas.specs.backgroundColor = 'black';
    // canvas.specs.ribbons_cartoonize = true;
    scalefactor = 1;
    }
  else {
    scalefactor = 15;
    canvas \
      = new ChemDoodle.TransformCanvas('canvas', %(width)s, %(height)s, true);
    // use JMol colors for atom types
    canvas.specs.atoms_useJMOLColors = true;
    // render circles instead of labels
    canvas.specs.atoms_circles_2D = true;
    // make bonds symmetrical (they will not face into rings)
    canvas.specs.bonds_symmetrical_2D = true;
    // change the background color
    // canvas.specs.backgroundColor = '#E4FFC2';
    canvas.specs.backgroundColor = 'black';
  }
  %(add_mol_to_canvas)s;
"""


js_create_ribbon_3dscene_template = """
  // initialize component and set visual specifications
  var canvas = new ChemDoodle.TransformCanvas3D('canvas', %(width)s, %(height)s);
  if (!canvas.gl) {
    canvas.emptyMessage = 'Your browser does not support WebGL';
    canvas.displayMessage();
  }
  canvas.specs.set3DRepresentation('Wireframe');
  canvas.specs.backgroundColor = 'black';
  canvas.specs.atoms_display = false;
  canvas.specs.bonds_display = false;
  canvas.specs.ribbons_cartoonize = true;
  
  var mol = ChemDoodle.readPDB('%(pdb)s');
  canvas.loadMolecule(mol);
"""



# elements for which chemdoodle is buggy
buggyelements = [
    'Fe', 'Al', 'Th', 'Rb', 'V', 'Mo', 'Cr', 'Ta', 'Ce',
    'W', 'Co', 'Nb', 'B', 
    ]


def getAtomsInOneUnitCell(matter):
    "get atoms in one unit cell, including atoms in the faces"
    from matter.Atom import Atom
    from matter.SymmetryUtilities import expandPosition

    # list of atoms to return
    ret = []
    # cache['H'] are a list of positions that are already
    # include in result atom list
    cache = {}; 
    #
    sg = matter.sg
    for atom in matter:
        symbol = atom.symbol
        # all equivalent but unique positions for this atom
        positions, pops, pmult = expandPosition(sg, atom.xyz)
        # get the cache for this type of atom
        cache1 = cache.get(symbol)
        if cache1 is None:
            cache1 = cache[symbol] = []
        # loop over all positions 
        for position in positions:
            position = tuple(position)
            if position in cache1:
                continue
            # add new position to cache, and the new atom to the result list
            # cache1.append(position)
            # ret.append(Atom(symbol, position))
            # also see if the position is at boundary, if so, add all
            # boundary atoms
            positions_at_boundary = getPositionsAtBoundary(position)
            for pos in positions_at_boundary:
                cache1.append(pos)
                ret.append(Atom(symbol, pos))
                continue
            continue
        continue
    return ret

def getPositionsAtBoundary(position):
    x, y, z = position
    for x1 in _getChoices(x):
        for y1 in _getChoices(y):
            for z1 in _getChoices(z):
                yield x1,y1,z1
    return

def _getChoices(x):
    if x in [0,1]:
        return [0,1]
    return [x]
    

# version
__id__ = "$Id$"

# End of file 
