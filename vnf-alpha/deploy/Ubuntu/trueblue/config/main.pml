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

    <component name="main">
        <property name="help-persistence">False</property>
        <property name="dumpconfiguration">False</property>
        <facility name="idd-session">idd-session</facility>
        <property name="help-properties">False</property>
        <property name="home">http://trueblue.caltech.edu/vnf/</property>
        <facility name="scribe">scribe</facility>
        <property name="csaccessor">ssher</property>
        <property name="help">False</property>
        <property name="imagepath">/vnf/images</property>
        <facility name="dds">dds</facility>
        <property name="upload-path">upload</property>
        <property name="actor">chainwizard</property>
        <property name="content">html</property>
        <property name="javascriptpath">/vnf/javascripts</property>
        <property name="help-components">False</property>
        <property name="routine">None</property>
        <facility name="clerk">clerk</facility>
        <property name="tmproot">/vnf/tmp</property>
        <property name="typos">relaxed</property>
        <property name="cgi-home">http://trueblue.caltech.edu/cgi-bin/vnf/main.cgi</property>
        <facility name="sentry">sentry</facility>
        <property name="javapath">/vnf/java</property>
        <property name="debug">True</property>

        <component name="ssher">
            <property name="private_key">/home/jbk/.vnfssh/id_rsa.www</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="known_hosts">/home/jbk/.vnfssh/known_hosts.www</property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
        </component>


        <component name="dds">
            <property name="dataroot">../content/data</property>
            <property name="help-properties">False</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="help-components">False</property>
        </component>


        <component name="idd-session">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="help-properties">False</property>
            <property name="marshaller">idd-pickler</property>
            <property name="host">131.215.30.140</property>
            <property name="help-components">False</property>
            <property name="port">50002</property>

            <component name="idd-pickler">
                <property name="help-properties">False</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="key">loe125sf9jniaqvm</property>
                <property name="help-components">False</property>
            </component>

        </component>


        <component name="clerk">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="dbwrapper">psycopg</property>
            <property name="db">vnf:A4*gl8D@vnf.caltech.edu:5432:vnf</property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
        </component>


        <component name="sentry">
            <property name="username">jbrkeith</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="passwd"></property>
            <property name="help-properties">False</property>
            <property name="attempts">0</property>
            <property name="session">ipa-session</property>
            <property name="help-components">False</property>
            <property name="ticket">jbrkeith0441ddf938917508de3a9bd0b5c54e79</property>

            <component name="ipa-session">
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="marshaller">ipa-pickler</property>
                <property name="host">131.215.30.140</property>
                <property name="help-components">False</property>
                <property name="port">50001</property>

                <component name="ipa-pickler">
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="key">q9mpfhgl2a8ixr16</property>
                    <property name="help-components">False</property>
                </component>

            </component>

        </component>


        <component name="chainwizard">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="previousSimulationId"></property>
            <property name="form-received">empty</property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
            <property name="analysisType">vacfcomputations</property>
            <property name="id"></property>

            <component name="empty">
                <property name="help-properties">False</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="submit"></property>
                <property name="help-components">False</property>
            </component>

        </component>


        <component name="weaver">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="copyright">1998-2005</property>
            <property name="creator">opal</property>
            <property name="timestamp">False</property>
            <property name="author">Michael A.G. Aivazis</property>
            <property name="bannerCharacter">~</property>
            <property name="help-properties">False</property>
            <property name="versionId"> $Id$</property>
            <property name="timestampLine"> Generated automatically by %s on %s</property>
            <property name="help-components">False</property>
            <property name="lastLine"> End of file </property>
            <property name="licenseText">[u'{LicenseText}']</property>
            <property name="copyrightLine">(C) %s  All Rights Reserved</property>
            <property name="organization">California Institute of Technology</property>
            <property name="bannerWidth">78</property>
        </component>


        <component name="scribe">
            <property name="help-properties">False</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="help-components">False</property>
        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- End of file -->
