#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, actionRequireAuthentication, AuthenticationError


class PolycrystalScatteringIntensity(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'polycrystalScatteringIntensity' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        username = director.sentry.username
        userrecord = director.clerk.getUser( username )
        fullname = userrecord.fullname
        document = main.document(title='Compute polycrystal scattering intensity')
        
        p = document.paragraph()
        p.text = ['''<p>&nbsp;</p>
<form action="" method="post" enctype="multipart/form-data" name="form1" id="form1">
  <label>Type of material
  <select name="select" id="select">
    <option>Polycrystal</option>
    <option>Disordered</option>
    <option>Single crystal</option>
  </select>
  </label>
  <label>Type of Scattering
  <select name="select" id="select">
    <option>Incoherent</option>
    <option>Coherent</option>
  </select>
  </label>
  <p>
    <label>Dynamics Run
    <input type="file" name="fileField" id="fileField" />
    </label>
  </p>
  <p>Q Values
    <label>
    <input name="textfield" type="text" id="textfield" value="-3.0" />
    </label>
    to 
    <label>
    <input name="textfield2" type="text" id="textfield2" value="10" />
    </label>
    incremented by 
    <label>
    <input name="textfield3" type="text" id="textfield3" value="0.1" />
    </label>
  </p>
  <p>Q Shell Width 
    <label>
    <input name="textfield4" type="text" id="textfield4" value="1.0" />
    </label>
  </p>
  <p><span id="sprytextfield1">
    <label>Vectors per shell
    <input name="text1" type="text" id="text1" value="50" />
    </label>
  </span></p>
  <p><span id="sprytextfield2">
  <label></label>
  </span> <span id="sprytextfield3"></span>
    <label>Units of Q
    <select name="select2" id="select2">
      <option>1/Ang</option>
      <option>1/nm</option>
    </select>
    </label>
  </p>
  <p><span id="sprytextfield4">
    <label>Fourier Transform Window (% Trajectory Length)
    <input name="text3" type="text" id="text3" value="10" />
    </label>
 </span></p>
  <p>
    <label>Number of Frequency Points
    <input name="text2" type="text" id="text2" value="1000" />
    </label>
    </p>
<p>&nbsp;</p>
  <p>&nbsp;</p>
</form>
<p>&nbsp;</p>''']

        return page


    def __init__(self, name=None):
        if name is None:
            name = "greet"
        super(PolycrystalScatteringIntensity, self).__init__(name)
        return


    pass # end of Greeter


# version
__id__ = "$Id$"

# End of file 
