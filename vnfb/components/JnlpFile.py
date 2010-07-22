
import os, tempfile

#this is a data object, not a component
 #### WARNING: THIS IS A QUICK AND DIRTY SOLUTION--NEEDS REFACTORING ####

class JnlpFile:

    
    def __init__(self,resources=[],
    mainClass='',
    programArguments=[],
    fileName = 'jnlpFile',
    title='Danse Application',
    description='A Java web start application',
    javaVersion='1.5'):
        self.resources = resources
        self.mainClass = mainClass
        self.programArguments = programArguments
        self.fileName = fileName
        self.title = title
        self.description = description
        self.javaVersion = javaVersion
        self.jnlpString=''
        self.reformJnlp()
    
    def reformJnlp(self,director=None):
        import urlparse as up
        if not director: 
            codebase = 'http://vnf.caltech.edu'
        else: 
            codebase = director.weaver.inventory.htmlbase
        self.jnlpString = '''<?xml version="1.0" encoding="UTF-8"?>
<jnlp spec="1.0+"
      codebase="'''+codebase+'''/java">
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
            self.jnlpString += '<jar href="' + resource + '" />'+os.linesep
        self.jnlpString += '''</resources>
    <application-desc main-class="''' + self.mainClass + '''" >
'''
        for argumentName, argumentValue in self.programArguments.iteritems():
            self.jnlpString += '<argument>'+argumentName+'='+argumentValue+'</argument>'+os.linesep
        self.jnlpString +='''</application-desc>
</jnlp>'''     
        
    
    def writeJnlp(self, director):
        '''write the jnlp file and return a url string pointing to it'''
        self.reformJnlp(director)
        if self.fileName[-5:] is '.jnlp': self.fileName = self.fileName[:-5]
        parentdir = os.path.join('..', 'content', 'data', 'tmp')
        tmpdirectory = tempfile.mkdtemp(dir=parentdir)
        f = file(os.path.join(tmpdirectory, self.fileName + '.jnlp'),'w')
        f.write(self.jnlpString)
        f.close()
        return os.path.join(director.weaver.inventory.htmlbase, 'tmp', os.path.split(tmpdirectory)[1], self.fileName + '.jnlp')
        
    
    