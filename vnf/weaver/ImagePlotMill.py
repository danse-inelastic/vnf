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
This implementation needs improvements.
It assumes that there is a symbolic link in html/ named "tmp" pointing
to the directory content/data/tmp
'''

class ImagePlotMill:


    def onImagePlot(self, plot):
        tmproot = self.configurations['tmproot']

        histogram = plot.data
        # first save data to a file
        histtemp = tempfile.mktemp(suffix='.h5')
        hh.dump(histogram, histtemp, '/', 'c')

        # matplotlib needs home to be writable
        os.environ['HOME'] = '/tmp'

        # find the temporary directory to write the png file
        parentdir = os.path.join('..', 'content', 'data', 'tmp')
        tmpdirectory = tempfile.mkdtemp(dir=parentdir)
        if not os.path.exists(tmpdirectory): os.makedirs(tmpdirectory)

        subdir = os.path.split(tmpdirectory)[1]

        # png filename
        filename = 'plot.png'
        filepath = os.path.join(tmpdirectory, filename)

        # the command to launch
        cmd = 'PlotHist.py %s --output=%s' % (histtemp, filepath)

        # launch
        from vnf.utils.spawn import spawn
        fail, output, error = spawn(cmd)

        if fail:
            raise RuntimeError, 'out=%s, err=%s' % (output, error)

        # delete the histogram
        os.remove(histtemp)

        # the url for the image
        pngurl = os.path.join(tmproot, subdir, filename)

        return [ '<img src="%s" />' % pngurl ]

    pass # end of DocumentMill


from vnf.components.misc import new_id
import os, tempfile, histogram.hdf as hh


# version
__id__ = "$Id$"

# End of file 
