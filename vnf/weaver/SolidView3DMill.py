#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


'''
This renderer takes a solid (represented by a hierarchy of geometry operations
and primitives) and use java 3d and jython to create a jar file displaying
a 3d view of the solid. Then a piece of html code is generated to show
this java applet.

Tricky things:
  * We need to run jythonc to create the jar file, which actually needs a
    display (this is weird though, because we do not need to see the 3d view
    in the compiling process). The current solution is to use virtual frame
    buffer. In a linux machine, run
    
      $ Xvfb :2 -screen 0 1024x768x16

    The virtual display may not be accessible due to athorization limit.
    Here is one way to deal with it:

      1. set env var XAUTHORITY. The "user" that runs apache2 server
      (www-data for ubuntu, _www for Mac) is not a normal user, and
      we need to manually set the file path for xauth:
      
        $ export XAUTHORITY=/tmp/xauth-www-data

      2. now add authorization key. We can use the authorization key of a
      real user. As a real user, run

        $ xauth list

      you will see a list of authorization keys. Look for the line that looks
      like

        <your host name>/unix:0 MIT-MAGIC-COOKIE-1 xxxxxxxxxx

      Copy the key at the end of that line, and as the apache2 user, run

        $ xauth add <your host name>/unix:2 MIT-MAGIC-COOKIE-1 xxxxxxxxxx
'''


APACHE2_USER_XAUTHORITY = '/tmp/xauth-www-data'
VIRTUAL_DISPLAY = ':2'
APACHE2_USER_HOME = '/tmp'


class SolidView3DMill:


    def onSolidView3D(self, view):
        tmproot = self.configurations['tmproot']

        solid = view.solid
        
        # find a temporary working directory
        parentdir = os.path.join('..', 'content', 'data', 'tmp')
        tmpdirectory = tempfile.mkdtemp(dir=parentdir)
        if not os.path.exists(tmpdirectory): os.makedirs(tmpdirectory)
        subdir = os.path.split(tmpdirectory)[1]

        # first render jython sources
        generator = JythonCodeGenerator()
        jyclassname = JythonCodeGenerator.classname
        jyfilepath = generator.generate(tmpdirectory, solid)
        jyfilename = os.path.basename(jyfilepath)
        
        # jar filename
        jarfilename = '%s.jar' % jyclassname
        jarfilepath = os.path.join(tmpdirectory, jarfilename)

        # bash script
        # the commands
        # j3d env vars
        path = os.path.abspath( 'j3d-env.sh' )
        if not os.path.exists(path):
            raise RuntimeError, "j3d-env.sh is not in the right place: %s" % path
        cmd0 = '. %s' % path
        envs = {
            'HOME': APACHE2_USER_HOME,
            'DISPLAY': VIRTUAL_DISPLAY,
            'XAUTHORITY': APACHE2_USER_XAUTHORITY,
            }
        envstr = ' '.join(['%s=%s' % (k,v) for k,v in envs.iteritems()])
        cmd2 = '%(envstr)s jythonc --core --deep -A unbboolean --jar %(jarfilename)s %(jyfilename)s' \
               % locals()
        cmds = [cmd0, cmd2]

        bashscript = 'run.sh'
        bashscriptpath = os.path.join(tmpdirectory, bashscript)
        open(bashscriptpath, 'w').write('\n'.join(cmds))

        # launch
        from vnf.utils.spawn import spawn
        cmd1 = 'cd %s' % tmpdirectory
        cmd2 = 'bash %s' % bashscript
        cmds = [cmd1, cmd2]
        fail, output, error = spawn('&&'.join(cmds))

        if fail:
            raise RuntimeError, 'out=%s, err=%s' % (output, error)

        # the url for the jar
        jarurl = os.path.join(tmproot, subdir, jarfilename)

        # the html code
        width = view.width; height = view.height
        htmlcode = '''
        <APPLET CODE="%(jyclassname)s" WIDTH="%(width)s" HEIGHT="%(height)s"
	ARCHIVE="%(jarurl)s" 
	NAME="%(jyclassname)s"
	ALIGN="BOTTOM" 
	alt="This browser doesn\'t support JDK 1.1 applets.">
        ''' % locals()
        return htmlcode.splitlines()

    pass # end of DocumentMill



class JythonCodeGenerator:


    classname = 'MySolidViewApplet'
    

    def generate(self, path, solid):
        import os

        shapePy = os.path.join(path, 'shape.py')
        open(shapePy, 'w').write( '\n'.join(self.shapeFactory(solid)) )

        appletBase = os.path.join(path, 'ViewerApplet.py')
        open(appletBase, 'w').write( '\n'.join(self.appletBaseClass()) )

        mainPy = os.path.join(path, self.classname + '.py')
        open(mainPy, 'w').write( '\n'.join(self.mainModule()) )

        return mainPy
    

    def mainModule(self):
        d = {'classname': self.classname}
        codes = """
from ViewerApplet import ViewerApplet
from shape import create

class %(classname)s(ViewerApplet):

    def __init__(self):
        ViewerApplet.__init__(self)
        solid = create()
        self.setTarget(solid)
        return
    

if __name__ == '__main__':
    applet = %(classname)s()
    from com.sun.j3d.utils.applet import MainFrame
    frame = MainFrame(applet, 640, 640)
""" % d
        codes = codes.splitlines()
        return codes
        

    def appletBaseClass(self):
        return """
from java.applet import Applet
from java.awt import BorderLayout
from com.sun.j3d.utils.applet import MainFrame
from com.sun.j3d.utils.universe import SimpleUniverse
from javax.media.j3d import AmbientLight, DirectionalLight, \
     BranchGroup, BoundingSphere, \
     Transform3D, TransformGroup, \
     Canvas3D
from javax.vecmath import Vector3f
from com.sun.j3d.utils.behaviors.mouse import \
     MouseRotate, MouseZoom, MouseTranslate

import math

class ViewerApplet(Applet):

    def __init__(self):
        self.u = None
        #import init_unbboolean
        #init_unbboolean.init(self.getDocumentBase()+'/coordinates')
        #init_unbboolean.init('coordinates')

    def setTarget(self, solid):
        self.target = solid
        return
    

    def createSceneGraph(self):
        objRoot = BranchGroup()
        
        vobj = self.createVisualObject()
        mouseControllable = self.createMouseControllable(vobj)
        objRoot.addChild(mouseControllable)

        lights = self.createLights()
        for light in lights:
            objRoot.addChild(light)
        
        mouseInteractors = self.createMouseBehavior(mouseControllable)
        for mi in mouseInteractors:
            objRoot.addChild(mi)

        objRoot.compile()
        return objRoot


    def createMouseControllable(self, target):
        objTrans = TransformGroup()
        objTrans.addChild(target)
        objTrans.setCapability(TransformGroup.ALLOW_TRANSFORM_WRITE)
        objTrans.setCapability(TransformGroup.ALLOW_TRANSFORM_READ)
        return objTrans


    def createMouseBehavior(self, target):
        mouseBounds = BoundingSphere()
        
        mouseRotate = MouseRotate()
        mouseRotate.setTransformGroup(target)
        mouseRotate.setSchedulingBounds(mouseBounds)

        mouseZoom = MouseZoom()
        mouseZoom.setTransformGroup(target)
        mouseZoom.setSchedulingBounds(mouseBounds)

        mouseTranslate = MouseTranslate()
        mouseTranslate.setTransformGroup(target)
        mouseTranslate.setSchedulingBounds(mouseBounds)
        
        return [mouseRotate, mouseZoom, mouseTranslate]
    
        
    def createLights(self):
        bs = BoundingSphere()
        
        alight = AmbientLight()
        alight.setInfluencingBounds(bs)

        dlight = DirectionalLight()
        dlight.setInfluencingBounds(bs)
        dlight.setDirection(-0.2, 0, -1)

        translation = Transform3D()
        translation.set(Vector3f(.6, .6, 0))
        objTrans = TransformGroup(translation)
        objTrans.addChild(dlight)
        
        return [alight, objTrans]


    def createVisualObject(self):
        return self.target
    

    def init(self):
        self.setLayout(BorderLayout())
        config = SimpleUniverse.getPreferredConfiguration()

        c = Canvas3D(config)
        self.add("Center", c)

        scene = self.createSceneGraph()
        self.u = SimpleUniverse(c)

        self.u.viewingPlatform.setNominalViewingTransform()

        self.u.addBranchGraph(scene)

    def destroy(self):
        self.u.removeAllLocales()
""".splitlines()


    def shapeFactory(self, shape):
        from geometry.visitors.viewers.java3d.JythonCodeRenderer import Renderer
        renderer = Renderer(indent=1)
        symbol = renderer.render(shape)
        lines = renderer.lines
        lines = ['def create():'] + lines
        return lines



class JSMill:

    def onSolidView3D(self, solid):
        return



import os, tempfile


# version
__id__ = "$Id$"

# End of file 
