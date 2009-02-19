# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import geometry.primitives as primitives
import geometry.operations as operations


class Renderer:


    def __init__(self, db):
        self.db = db
        return


    def render(self, instrument):
        return self._dispatch(instrument)


    def onInstrument(self, instrument):
        components = instrument.components
        components = components.dereference(self.db)

        geometer = instrument.geometer
        poreg = geometer.dereference(self.db)

        shapes = []
        for name, component in components:
            shape = self._dispatch(component)
            if not shape: continue
            po = poreg[name]
            position = po.position
            rx, ry, rz = po.orientation
            shape1 = operations.translate(
                operations.rotate(
                    operations.rotate(
                        operations.rotate(shape, (1,0,0), rx),
                        (0,1,0), ry),
                    (0,0,1), rz),
                position)
            shapes.append(shape1)
            continue

        if not shapes: return

        shape = shapes[0]
        for s in shapes[1:]:
            shape = operations.unite(shape, s)
            continue
        return shape


    def onChanneledGuide(self, cg):
        front = cg.w2, cg.h2
        back = cg.w1, cg.h1
        l = cg.l
        return primitives.rectTube(front, back, l)


    def onEMonitor(self, emonitor):
        X = emonitor.x_max-emonitor.x_min
        Y = emonitor.y_max-emonitor.y_min
        Z = (X+Y)/20. # monitor has no thickness at this moment. this is kind of random
        diagonal = X,Y,Z
        b = primitives.block(diagonal)

        C = (emonitor.x_min+emonitor.x_max)/2., \
                (emonitor.y_min+emonitor.y_max)/2., \
                0
        if C[0] == C[1] == 0.0: return b
        return primitives.translate(b, C)


    def onFermiChopper(self, fc):
        Z = fc.len
        X = fc.w
        Y = fc.ymax-fc.ymin
        diagonal = X,Y,Z
        b = primitives.block(diagonal)
        
        CY = (fc.ymax+fc.ymin)/2
        if CY == 0.0: return b

        C = 0, CY, 0
        return primitives.translate(b, C)


    def onMonochromaticSource(self, s):
        diagonal = 0.01,0.01,0.01 # should have no size.
        return primitives.block(diagonal)


    def onNeutronRecorder(self, r):
        return 


    def onQEMonitor(self, m):
        return 


    def onQMonitor(self, m):
        return


    def onSNSModerator(self, m):
        X = xwidth
        Y = height
        Z = (X+Y)/20.
        diagonal = X,Y,Z
        b = primitives.block(diagonal)
        return b


    def onSampleComponent(self, s):
        diagonal = 0.01,0.01,0.01 # should have no size.
        return primitives.block(diagonal)


    def onSphericalPSD(self, d):
        radius = d.radius
        thickness = radius/20.
        s1 = primitives.sphere(radius+thickness/2.)
        s2 = primitives.sphere(radius-thickness/2.)
        return operations.subtract(s1,s2)


    def onT0Chopper(self, tc):
        Z = tc.len
        X = tc.w2
        Y = tc.ymax-tc.ymin
        diagonal = X,Y,Z
        b = primitives.block(diagonal)
        
        CY = (tc.ymax+tc.ymin)/2
        if CY == 0.0: return b

        C = 0, CY, 0
        return primitives.translate(b, C)


    def onTofMonitor(self, tm):
        X = tm.x_max-tm.x_min
        Y = tm.y_max-tm.y_min
        Z = (X+Y)/20. # monitor has no thickness at this moment. this is kind of random
        diagonal = X,Y,Z
        b = primitives.block(diagonal)

        C = (tm.x_min+tm.x_max)/2., \
            (tm.y_min+tm.y_max)/2., \
            0
        if C[0] == C[1] == 0.0: return b
        return primitives.translate(b, C)


    def onVanadiumPlate(self, vp):
        X = vp.width
        Y = vp.height
        Z = vp.thickness
        diagonal = X,Y,Z
        return primitives.block(diagonal)
    

    def _dispatch(self, element):
        handler = 'on'+element.__class__.__name__
        handler = getattr(self, handler)
        return handler(element)
    

    pass # end of Renderer



# version
__id__ = "$Id$"

# End of file 
