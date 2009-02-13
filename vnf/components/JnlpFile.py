

#this is a data object, not a component
 #### WARNING: THIS IS A QUICK AND DIRTY SOLUTION--NEEDS REFACTORING ####

class JnlpFile:

    
    def __init__(self,resources=[],
    mainClass='',
    programArguments=[],
    title=' ',
    description=' ',
    javaVersion='1.5'):
        self.resources = resources
        self.mainClass = mainClass
        self.programArguments = programArguments
        self.title = title
        self.description = description
        self.javaVersion = javaVersion
    
    def returnFileAsString(self, director):
        '''write the jnlp file which will load gulp with the correct structure'''
        import os
        jnlpFile = '''<?xml version="1.0" encoding="UTF-8"?>
<jnlp spec="1.0+"
      codebase="'''+director.home+'''/java">
    <information>
        <title>'''+self.title+'''</title>
        <vendor>DANSE</vendor>
        <homepage href="http://danse.us" />
        <description>'''+self.description+'''</description>
    </information>
    <offline-allowed/>
    <security>
        <all-permissions/>
    </security>
    <resources>
        <j2se version="''' + self.javaVersion + '''+" java-vm-args="-Xmx512m -splash:splash.png"/>
'''
        for resource in self.resources:
            jnlpFile += '<jar href="' + resource + '" />'+os.linesep
        jnlpFile += '''
    </resources>
    <application-desc main-class="''' + self.mainClass + '''" />
</jnlp>'''
        return jnlpFile
    
    