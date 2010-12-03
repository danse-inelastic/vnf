#!/usr/bin/env bash

ROOT_UID=0   # Root has $UID 0.

if [ "$UID" -eq "$ROOT_UID" ]  # Will the real "root" please stand up?
then
  su jbk #become someone with permission to move the docs
fi

svn up
make html
scp -r _build/html/* jbrkeith@login.cacr.caltech.edu:projects/danse/docs.danse.us/docroot/VNET
#rsync -a _build/html/* jbrkeith@login.cacr.caltech.edu:projects/danse/docs.danse.us/docroot/VNET


#if [[ $USER -eq jbk ]] then 
#	svn up
#	make html
#	scp -r _build/html/* jbrkeith@login.cacr.caltech.edu:projects/danse/docs.danse.us/docroot/AbInitio/qecalc
#	# hi nikolay...just do a script like the one above...
#elif [[ $USER -eq root ]] then 
#	su jbk #become someone with permission to move the docs 
#fi

#ssh jbrkeith@login.cacr.caltech.edu 'chgrp -R danse projects/danse/docs.danse.us/docroot/VNET/*'