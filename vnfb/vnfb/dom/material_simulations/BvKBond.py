# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# deactivate the warning from importing bvk
import journal
journal.warning('UserWarning').deactivate()
import bvk
#
journal.warning('UserWarning').activate()


from bvk.orm.BvKBond import BvKBond


# view
def customizeLubanObjectDrawer(self, drawer):
    import luban.content as lc
    from luban.content import select, alert, load
    
    # override editable view to add an alert section for violated constraints
    # this is modified from luban.orm.views.ObjectPropertiesMold
    # we need a special field for force constant matrix
    def _createfields(obj):
        # a new field for force_constant_matrix
        doc = lc.document(title='force constant matrix', Class='force-constant-matrix-input-container')
        from luban.content.FormTextField import FormTextField

        # left and right
        sp = doc.splitter()
        left = sp.section(Class='force-constant-matrix')
        right = sp.section(Class='force-constant-matrix-constraints-section')

        # left is grid for the matrix
        grid = lc.grid(); left.add(grid)
        fcm = obj.force_constant_matrix
        for i in range(3):
            gr = grid.row()
            for j in range(3):
                gc = gr.cell()
                v = fcm[i,j]
                w = FormTextField(value=v, name='%s_%s_%s' % ('force_constant_matrix', i, j))
                gc.add(w)
            continue

        # right is the container for constraints
        cdoc = right.document(name='force-constant-matrix-constraints', title='constraints')

        # replace the force constant matrix field
        fields = drawer.mold.o2f(obj)
        fields['force_constant_matrix'] = doc

        return fields
    

    def _form(obj):
        self = drawer.mold
        
        # a form for the attributes
        form = lc.form(Class='bvkbond-form')
        #
        self._addfieldstoform(form, obj)
        #
        # make sure when A, or B, or Boffset changes, reload constraints
        updateconstraints = select(element=form)\
                            .find(name='force-constant-matrix-constraints')\
                            .replaceContent(
            select(element=form).submit(actor='orm/bvkbonds', routine='getConstraints',
                                        id = self.orm(obj).id)
            )
        for fname in ['A', 'B', 'Boffset_0', 'Boffset_1', 'Boffset_2', 'Boffset_is_fractional']:
            field = form.getDescendentByName(fname)
            field.onchange = updateconstraints
        # when constraints document load, update constraints too
        form.getDescendentByName('force-constant-matrix-constraints').oncreate = updateconstraints
        
        return form
        
    drawer.mold._form = _form
    drawer.mold._createfields = _createfields
    
    # uses_primitive_unitcell should be hidden because it should always be synced with
    # model.uses_primitive_unitcell
    drawer.mold.sequence = ['A', 'B', 'Boffset', 'Boffset_is_fractional', 'force_constant_matrix']
    drawer.sequence = ['properties']
    return
    
BvKBond.customizeLubanObjectDrawer = customizeLubanObjectDrawer



# version
__id__ = "$Id$"

# End of file 
