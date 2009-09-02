<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!                             Michael A.G. Aivazis
!                      California Institute of Technology
!                      (C) 1998-2005  All Rights Reserved
!
! {LicenseText}
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->


<!DOCTYPE inventory>

<inventory>

  <component name='journald-harness'>
    <property name='home'>../config</property>

    <component name='journal'>
        <property name='device'>file</property>

        <component name='file'>
          <property name='name'>../log/journal.log</property>
        </component>

    </component>

  </component>

</inventory>


<!-- version-->
<!-- $Id: journald-harness.pml,v 1.1.1.1 2006-11-27 00:09:15 aivazis Exp $-->

<!-- End of file -->
