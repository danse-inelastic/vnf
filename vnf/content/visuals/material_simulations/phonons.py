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


#
import luban.content as lc
from luban.content import select, load, alert
import os, tempfile
import numpy as np


#
from vnf.dom.material_simulations.Phonons import Phonons


class Factory(object):
    
    
    def __init__(self, actorname = 'orm/phonons'):
        import journal
        self._debug = journal.debug("phonons")
        self.actorname = actorname
        return
    
    
    def createFile(self, id, director):
        phonons = self._load(id, director)
        content = self._createDownloadContent(id, phonons, director)
        filename = 'phonon-dispersions-%s.plot' % id
        return lc.file(filename=filename, content=content)
        

    def createGraphicalView(self, ids=[], id=None, director=None):
        if ids and id:
            raise ValueError
        if ids: return self._createGraphicalViewM(ids, director)
        return self._createGraphicalView1(id, director)
    
    
    def _createGraphicalViewM(self, ids, director):
        nids = len(ids)
        nrows = (nids+1)/2
        doc = lc.document(Class='container')
        grid = lc.grid(); doc.add(grid)
        for i in range(nrows):
            row = grid.row()

            cell1 = row.cell();
            id = ids[2*i];
            cell1.add(self._createGraphicalView1(id, director))

            if 2*i+1 < nids:
                cell2 = row.cell();
                id = ids[2*i+1];
                cell2.add(self._createGraphicalView1(id, director))

            continue
        
        return doc


    def _createGraphicalView1(self, id, director):
        domaccess = self._domaccess(director)
        obj = self._load(id, director)
        if not obj: return
        orm = domaccess.orm
        db = orm.db
        record = orm(obj)
        # the document to build
        title='phonons %s' % record.id
        short_description = record.short_description
        if short_description:
            title += ': %s' % short_description
        doc = lc.document(title=title)
        # link to the computation
        try:
            origin = record.getOrigin(db)
        except:
            import traceback
            msg = traceback.format_exc()
            self._debug.log(msg)
            origin = None
        if origin:
            origin_link = lc.link(
                label='computed from %s %s' % (origin.getTableName(), origin.id),
                onclick = load(actor='computation', routine='view',
                               type = origin.getTableName(), id = origin.id)
                )
            doc.add(origin_link)
        # plot
        p, link = self._createPlotAndDataLink(id, obj, director)
        doc.add(p)
        doc.add(link)
        return doc
    
    
    def _createPlotAndDataLink(self, id, phonons, director):
        try:
            plot = self._getDefaultDispersionPlot(id, phonons, director)
        except RuntimeError, e:
            p = lc.paragraph() # fake plot
            p.text = [str(e)]
            l = lc.htmldocument() # fake link
            return p,l
        x, ys, xticks = plot
        
        # plot
        caption = (
            'Horizontal axis: high-symmetry points in the reciprocal space. '
            'Vertical axis: energy in meV'
            )
        p = lc.plot2d(xticks=xticks, caption=caption)
        for i,y in enumerate(ys):
            p.curve(x=list(x), y=list(y), label=str(i))

        # download link
        label = 'Download dispersions'
        ondownload = load(
            actor=self.actorname, routine='createFile', id=id)
        downloadLink = lc.downloader(label=label, ondownload=ondownload)
        return p, downloadLink
    
    
    def _getDefaultDispersionPlot(self, id, phonons, director):
        import pickle
        
        # try load it from cache
        domaccess = self._domaccess(director)
        record = domaccess.orm(phonons)
        dds = director.dds
        path = dds.abspath(record, "default-dispersion-plot")
        if os.path.exists(path):
            try:
                return pickle.load(open(path))
            except:
                # fail to load from cache. treat it like there is no cache
                pass
        # no cache.
        # create plot
        plot = self._createDefaultDispersionPlot(id, phonons, director)
        # save
        pickle.dump(plot, open(path, 'w'))
        return plot
    
    
    def _createDefaultDispersionPlot(self, id, phonons, director):
        "create default dispersion plot. return x, ys, and xticks"
        domaccess = self._domaccess(director)
        record = domaccess.orm(phonons)
        try:
            domaccess.standardizeDataInIDFFormat(record.id)
        except NotImplementedError:
            msg = 'Plotting for phonons#%s failed: data missing or in wrong format' % (record.id,)
            raise RuntimeError, msg
        
        try:
            phonons = domaccess.getDataForPhonons(phonons)
        except NotImplementedError:
            msg = 'Parser for this data format is not yet implemented'
            raise RuntimeError, msg

        if not phonons: 
            raise RuntimeError, 'Data missing'
        
        x, ys, xticks = phonons.getDefaultDispersionPlot()
        return x, ys, xticks
    
    
    def _createDownloadContent(self, id, disp, director):
        domaccess = self._domaccess(director)
        record = domaccess.orm(disp)
        domaccess.standardizeDataInIDFFormat(record.id)
        disp = domaccess.getDataForPhonons(disp)
        if not disp: 
            raise RuntimeError, "Dispersion data missing"
        x, ys, xticks = disp.getDefaultDispersionPlot()
        #
        content = []
        for point,label in xticks:
            content.append('# '+str(point)+' is '+label)
        for xval,yvals in zip(x, np.array(ys).transpose()):
            line = str(xval)+' '
            for yval in yvals:
                line+=str(yval)+' '
            content.append(line)
        return '\n'.join(content)


    def _load(self, id, director):
        doma = self._domaccess(director)
        return doma.getPhonons(id)
    
    
    def _initComputationOrm(self, director):
        domaccess = director.retrieveDOMAccessor('computation')
        return domaccess.orm
    
    
    def _domaccess(self, director):
        self._initComputationOrm(director)
        return director.retrieveDOMAccessor('material_simulations/phonons')
            

# version
__id__ = "$Id$"

# End of file 
