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
    
    
    def createViewer(self, matter, size=200):
        """create html content that has a matter viewer
        This is implemented by using chemdoodle
        """
        chem_doodle_base = self.chem_doodle_base
        script = self._createChemDoodleJS(matter, size)
        # script = self._createChemDoodleJSUsingPDB(matter, size)
        script = '\n'.join(script)
        text = page_template % locals()
        return text


    def _createChemDoodleJS(self, matter, size):
        code = []
        # create mol
        code.append('var mol = new ChemDoodle.structures.Molecule();')
        # add atoms to mol
        sg = matter.sg
        atoms = getAtomsInOneUnitCell(matter)
        for count,atom in enumerate(atoms):
            symbol = atom.symbol
            # this is to avoid a bug in chemdoodle
            if symbol in buggyelements:
                symbol = 'Cu'
            x,y,z = atom.xyz
            code.append('var atom%s = new ChemDoodle.structures.Atom("%s", %s, %s, %s);' % (count, symbol, x*size/2,y*size/2,z*size/2))
            code.append('mol.atoms[%s]=atom%s;' % (count,count))
            continue
        # add mol to canvas
        code.append('canvas.loadMolecule(mol);')
        add_mol_to_canvas = '\n'.join(code)
        #
        width = height = size
        #
        text = js_create_3dscene_template % locals()
        return [text]


    def _createChemDoodleJSUsingPDB(self, matter, size):
        text = [
            """
	// initialize component and set visual specifications
	// var canvas = new ChemDoodle.RotatorCanvas('rotate3D', 200, 200, true);""",
            "var canvas = new ChemDoodle.TransformCanvas('canvas', %s, %s, true);" % (size, size),
            """// use JMol colors for atom types
	canvas.specs.atoms_useJMOLColors = true;
	// render circles instead of labels
	canvas.specs.atoms_circles_2D = true;
	// make bonds symmetrical (they will not face into rings)
	canvas.specs.bonds_symmetrical_2D = true;
	// change the background color
	canvas.specs.backgroundColor = '#E4FFC2';
        """]
        pdb = matter.writeStr('pdb')
        pdb = pdb.replace('\n', r'\n')
        text.append('var mol = ChemDoodle.readMOL("%s");' % pdb)
        text.append('canvas.loadMolecule(mol);')
        # text.append('canvas.startAnimation();')
        return text


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
  var canvas;
  var webgl = ChemDoodle.featureDetection.supports_webgl();
  if (webgl) {
    canvas \
      = new ChemDoodle.TransformCanvas3D('canvas', %(width)s, %(height)s, true);
    canvas.specs.set3DRepresentation('Ball and Stick');
    canvas.specs.backgroundColor = 'black';
    }
  else {
    canvas \
      = new ChemDoodle.TransformCanvas('canvas', %(width)s, %(height)s, true);
      // use JMol colors for atom types
      canvas.specs.atoms_useJMOLColors = true;
      // render circles instead of labels
      canvas.specs.atoms_circles_2D = true;
      // make bonds symmetrical (they will not face into rings)
      canvas.specs.bonds_symmetrical_2D = true;
      // change the background color
      canvas.specs.backgroundColor = '#E4FFC2';
  }
  %(add_mol_to_canvas)s;
"""

# elements for which chemdoodle is buggy
buggyelements = [
    'Fe', 'Al',
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
