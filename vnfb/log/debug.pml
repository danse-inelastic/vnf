<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! {LicenseText}
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->

<!DOCTYPE inventory>

<inventory>

    <component name="main">
        <property name="typos">relaxed</property>
        <property name="help-persistence">False</property>
        <property name="dumpconfiguration">False</property>
        <property name="stream"><open file '<stdout>', mode 'w' at 0xb7810070></property>
        <property name="log-dir">../log</property>
        <facility name="clerk">clerk</facility>
        <facility name="sentry">sentry</facility>
        <property name="dumpconfiguration-output"></property>
        <property name="actor">gulpsimulation</property>
        <property name="content">html</property>
        <property name="extension">luban-uiapp-extension</property>
        <property name="help-properties">False</property>
        <facility name="activity-logger">activity-logger</facility>
        <property name="help-components">False</property>
        <property name="routine">start</property>
        <property name="debug">True</property>
        <facility name="guid">guid</facility>
        <facility name="painter">painter</facility>
        <property name="help">False</property>

        <component name="activity-logger">
            <property name="help-properties">False</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="help-components">False</property>
        </component>


        <component name="gulpsimulation">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="structure_id"></property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
            <property name="id"></property>
        </component>


        <component name="web-weaver">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="copyright"></property>
            <property name="creator"></property>
            <property name="timestamp">True</property>
            <property name="author"></property>
            <property name="bannerCharacter">~</property>
            <property name="versionId"> $Id$</property>
            <property name="help-properties">False</property>
            <property name="html-base">http://localhost:8600</property>
            <property name="use-cookie">False</property>
            <property name="timestampLine"> Generated automatically by %s on %s</property>
            <property name="organization"></property>
            <property name="cookie-path">/cgi-bin/</property>
            <property name="lastLine"> End of file </property>
            <property name="licenseText">['{LicenseText}']</property>
            <property name="copyrightLine">(C) %s  All Rights Reserved</property>
            <facility name="librarian">librarian</facility>
            <property name="controller-url">/cgi-bin/main.py</property>
            <property name="bannerWidth">78</property>
            <property name="help-components">False</property>

            <component name="librarian">
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="jsbase">javascripts</property>
                <property name="library">../config/widget.lib</property>
                <property name="help-properties">False</property>
                <property name="help-components">False</property>
                <property name="cssbase">css</property>
            </component>

        </component>


        <component name="clerk">
            <property name="engine">sqlite</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="db">postgres://linjiao:4OdACm#@localhost/vnfa2b</property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
        </component>


        <component name="sentry">
            <property name="username">demo</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="passwd"></property>
            <property name="help-properties">False</property>
            <property name="attempts">0</property>
            <property name="session">ipa-session</property>
            <property name="help-components">False</property>
            <property name="ticket">demo22ffc9e8c78e12f9afdaceb40aa7a0e2</property>

            <component name="ipa-session">
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="marshaller">ipa-pickler</property>
                <property name="host">127.0.1.1</property>
                <property name="help-components">False</property>
                <property name="port">50001</property>

                <component name="ipa-pickler">
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="key">cdwoxq4801k9sp6e</property>
                    <property name="help-components">False</property>
                </component>

            </component>

        </component>


        <component name="luban-uiapp-extension">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <facility name="dds">dds</facility>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
            <property name="itaskmanager">itask-manager</property>
            <property name="csaccessor">ssher</property>

            <component name="dds">
                <property name="dataroot">../content/data</property>
                <property name="help-properties">False</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-components">False</property>
            </component>


            <component name="itask-manager">
                <property name="debug">False</property>
                <property name="help-properties">False</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-components">False</property>
            </component>


            <component name="ssher">
                <property name="private_key"></property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="known_hosts"></property>
                <property name="help-properties">False</property>
                <property name="user">www-data</property>
                <property name="help-components">False</property>
            </component>

        </component>


        <component name="guid">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="help-properties">False</property>
            <property name="recordLocator">locator</property>
            <property name="help-components">False</property>
            <property name="datastore-path">../config/guid.dat</property>

            <component name="locator">
                <property name="alphabet">23456789ABCDEFGHIJKLMNPQRSTUVWXYZ</property>
                <property name="help-properties">False</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-components">False</property>
            </component>

        </component>


        <component name="painter">
            <property name="help-components">False</property>
            <property name="help-properties">False</property>
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="object_painter">object-painter</property>

            <component name="object-painter">
                <property name="help-properties">False</property>
                <property name="actor_formatter">orm/%s</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-components">False</property>
            </component>

        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Tue Dec 22 05:22:41 2009-->

<!-- End of file -->
