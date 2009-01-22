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
        <property name="actor">sample</property>
        <property name="content">html</property>
        <property name="javascriptpath">/vnf/javascripts</property>
        <property name="help-components">False</property>
        <property name="routine">default</property>
        <facility name="clerk">clerk</facility>
        <property name="typos">relaxed</property>
        <property name="cgi-home">http://trueblue.caltech.edu/cgi-bin/vnf/main.cgi</property>
        <facility name="sentry">sentry</facility>
        <property name="javapath">/vnf/java</property>
        <property name="debug">True</property>

        <component name="ssher">
            <property name="private_key">/Users/linjiao/vnfssh/id_rsa.www</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="known_hosts">/Users/linjiao/vnfssh/known_hosts.www</property>
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
            <property name="port">50004</property>

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
            <property name="db">linjiao:4Od&amp;Cm#@localhost:54321:vnf</property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
        </component>


        <component name="sentry">
            <property name="username">demo</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="passwd">demo</property>
            <property name="help-properties">False</property>
            <property name="attempts">0</property>
            <property name="session">ipa-session</property>
            <property name="help-components">False</property>
            <property name="ticket">demo0adc12afe048be299c7f7a2eafa2ce8f</property>

            <component name="ipa-session">
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="marshaller">ipa-pickler</property>
                <property name="host">131.215.30.140</property>
                <property name="help-components">False</property>
                <property name="port">50005</property>

                <component name="ipa-pickler">
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="key">kel592gjs6xztr1o</property>
                    <property name="help-components">False</property>
                </component>

            </component>

        </component>


        <component name="sample">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="page">empty</property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
            <property name="id">None</property>
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
