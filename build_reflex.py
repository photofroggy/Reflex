''' build.py
    Created by photofroggy (Henry Rapley)
    
    Build slave for reflex. Automatically edits
    appropriate source files, archives changes,
    generates documentation and pushes changes to
    github.
    
    NB: Doesn't do this stuff yet.
'''

import os
import sys
import time
import json
import shutil
import argparse
import traceback
import subprocess

def writeout(message=''):
    sys.stdout.write('{0}\n'.format(message))

def export_struct(data, depth=1):
    """ This method returns a JSON object from a Python object.
        The JSON object is formatted to make it easier to read.
        Example: export_struct({'lol':[1,2]})
            >>  {
            >>      'lol': [
            >>          1,
            >>          2
            >>      ]
            >>  }
    """
    if isinstance(data, dict):
        string  = '{'
    elif isinstance(data, list) or isinstance(data, tuple):
        string = '['
    else:
        return flatten_val(data)
    for i in data:
        if len(string) > 0 and string[-1] not in ('{', '(', '['):
            string+= ','
        string += '\n{0}'.format("    " * depth)
        if isinstance(data, dict):
            string += flatten_val(i)+' : '
            use = data[i]
        else:
            use = i
        if isinstance(use, str) or isinstance(use, int) or isinstance(use, float):
            string += flatten_val(use)
        else:
            string += export_struct(use, depth+1)
    if len(data) > 0: string += "\n"+("    "*(depth-1))
    if isinstance(data, list) or isinstance(data, tuple):
        string += ']'
    elif isinstance(data, dict):
        string += '}'
    return string

def flatten_val(value):
    if not isinstance(value, str):
        if value is None:
            return 'null'
        if value is True:
            return 'true'
        if value is False:
            return 'false'
        return '"{0}"'.format(str(value).replace('"', '\\"'))
    return '"{0}"'.format(str(value).replace('"', '\\"'))

def clean_files(dirs=[], debug=None):
    """ Removes .pyc files from given directories. """
    if debug is None:
        debug = lambda m: None
    
    for dir in dirs:
        # Remove all pyc files in a directory.
        debug('>> Cleaning directory {0}...'.format(dir))
        for file in os.listdir(dir):
            name, ext = os.path.splitext(file)
            if ext == '.pyc':
                if os.path.exists(os.path.join(dir, name+'.py')):
                    debug('>>> Removing {0}.pyc...'.format(
                        os.path.join(dir, name)))
                    os.remove(os.path.join(dir, file))
    
        # Remove __pycache__ if it exists.
        if os.path.exists(os.path.join(dir, '__pycache__')):
            debug('>>> Removing pycache...')
            shutil.rmtree(os.path.join(dir, '__pycache__'))

class Build:
    
    args = None
    stamp = ()
    major = 1
    version = '1.n'
    series = 'Charged'
    
    class conf:
        name = None
        
        class version:
            major = None
            build = None
            full = None
            series = None
        
        pypi = None
        
        class doc:
            source = None
            dest = None
            cf = None
        
        clean = None
            
    def __init__(self):
        self.load_config()
        
        self.handle_args()
        
        self.version = '{0}.{1}'.format(self.conf.version.major, self.args.build)
        
        self.get_stamp()
        
        writeout('>> Preparing to release Reflex {0} ({1})...'.format(
            self.version, self.stamp[1]))
        
        writeout('>> Stamping build list...')
        self.stamp_build_list()
        
        self.modify_docs()
        
        self.generate_docs()
        
        self.modify_setup()
        
        self.push_changes()
        
        writeout('>> Cleaning folders and files...')
        
        clean_files(self.conf.clean, writeout if self.args.verbose else None)
        
        self.distribute()
    
        writeout('>> Build {0} packaged and released'.format(self.args.build))
        
        self.save_config()
    
    def load_config(self):
        conf = open('build.conf', 'r')
        data = json.loads(conf.read())
        conf.close()
        
        self.conf.name = data['name']
        
        self.conf.version.major = data['version']['major']
        self.conf.version.build = data['version']['build']
        self.conf.version.full = data['version']['full']
        self.conf.version.series = data['version']['series']
        
        self.conf.pypi = data['pypi']
        
        self.conf.doc.source = data['doc']['source']
        self.conf.doc.dest = data['doc']['dest']
        self.conf.doc.cf = data['doc']['cf']
        
        self.conf.clean = data['clean']
    
    def save_config(self):
        data = {
            'name': self.conf.name,
            'version': {
                'major': self.conf.version.major,
                'build': self.args.build,
                'full': '{0}.{1}'.format(self.conf.version.major, self.args.build),
                'series': self.conf.version.series
            },
            'pypi': self.conf.pypi,
            'doc': {
                'source': self.conf.doc.source,
                'dest': self.conf.doc.dest,
                'cf': self.conf.doc.cf
            },
            'clean': self.conf.clean
        }
        
        conf = open('build.conf', 'w')
        conf.write(export_struct(data))
        conf.close()


    def handle_args(self):
        parser = argparse.ArgumentParser(
            description='Performs build tasks for Reflex-events.')
            
        parser.add_argument('-b', '--build', dest='build',
            action='store', type=int, default=-1, metavar='N',
            help='Define the build number for the release')
        
        parser.add_argument('-S', '--nosetup', dest='setup',
            action='store_false', default=True,
            help='Do not modify setup.py during build process')
        
        parser.add_argument('-ds', '--docsource', dest='docsource',
            action='store', default=self.conf.doc.source, metavar='source_dir',
            help='Define the source folder for the documentation')
        
        parser.add_argument('-dd', '--docdest', dest='docdest',
            action='store', default=self.conf.doc.dest, metavar='destination',
            help='Define the destination folder for the documentation')
        
        parser.add_argument('-D', '-nodocs', dest='doc',
            action='store_false', default=True,
            help='Use this option to prevent documentation being generated')
        
        parser.add_argument('-P', '--nopush', dest='push',
            action='store_false', default=True,
            help='Use this to prevent pushing updates to github')
        
        parser.add_argument('-U', '--noupload', dest='upload',
            action='store_false', default=True,
            help='Use this to prevent uploading the distribution to pypi')
        
        parser.add_argument('-v', '--verbose', dest='verbose',
            default=False, action='store_true',
            help='Show debug messages for everything done')
        
        parser.add_argument('-q', '--quiet', dest='verbose',
            action='store_false',
            help='Show minimal output messages [Default]')
            
        
        self.args = parser.parse_args()
        
        if self.args.build < 1:
            parser.error('A build number must be provided!')
    
    def get_stamp(self):
        raw = time.time()
        self.stamp = (raw, time.strftime("%d%m%Y-%H%M%S", time.gmtime(raw)))
    
    def stamp_build_list(self):
        if self.version == self.conf.version.full:
            return
        
        blist = open('./Builds.txt', 'r')
        data = blist.read()
        blist.close()
        
        newd = data.replace('Build {0} ()'.format(self.args.build),
            'Build {0} ({1})'.format(self.args.build, self.stamp[1]))
        
        if newd == data:
            
            if 'Build {0} ('.format(self.args.build) in newd:
                return
            
            writeout('>> Build {0} is not documented in the build list!'.format(
                self.args.build))
            writeout('>> Make sure the changes in this build are listed.')
            writeout('>> Exiting...')
            sys.exit(3)
        
        blist = open('./Builds.txt', 'w')
        blist.write(newd)
        blist.close()
    
    def modify_setup(self):
        
        if not self.args.setup:
            if self.args.verbose:
                writeout('>> Skipping setup.py modification...')
            return
        
        writeout('>> Attempting to modify setup.py...')
        
        previous = self.conf.version.full
        
        writeout('>> Assuming previous version is {0}...'.format(previous))
        
        sfile = open('./setup.py', 'r')
        data = sfile.read()
        sfile.close()
        
        newd = data.replace('version=\'{0}\''.format(previous),
            'version=\'{0}\''.format(self.version))
        
        if newd == data:
            writeout('>> Previous version is not {0}...'.format(previous))
            writeout('>> Correct this or use -S to leave setup.py unmodified.')
            writeout('>> Exiting...')
            sys.exit(3)
        
        sfile = open('./setup.py', 'w')
        sfile.write(newd)
        sfile.close()
    
    def modify_docs(self):
        
        if not self.args.doc:
            if self.args.verbose:
                writeout('>> Skipping documentation...')
            return
        
        writeout('>> Editing documentation links...')
        
        indexd = os.path.join(self.args.docsource, 'index.rst')
        dld = os.path.join(self.args.docsource, 'reflex_downloads.rst')
        
        self.modify_docs_index(indexd, dld)
        
    def modify_docs_index(self, indexd, dld):
        
        if self.args.verbose:
            writeout('>>> Editing index link...')
        
        indexf = open(indexd, 'r')
        idata = indexf.read()
        indexf.close()
        
        newid = idata.replace('Build {0}'.format(self.conf.version.build),
            'Build {0}'.format(self.args.build))
        
        if newid == idata:
            writeout('>>> Editing index did not work.')
            writeout('>>> Previous build was not {0}.'.format(self.args.build))
            return
        
        newid = newid.replace('Reflex_{0}'.format(self.conf.version.full),
            'Reflex_{0}'.format(self.version))
        
        indexf = open(indexd, 'w')
        indexf.write(newid)
        indexf.close()
        
        self.modify_docs_downloads(dld)
    
    def modify_docs_downloads(self, dld):
        
        if self.args.verbose:
            writeout('>>> Editing downloads page...')
        
        downloads = open(dld, 'r')
        data = downloads.read()
        downloads.close()
        
        newd = data.replace('**Downloads:**\n\n',
            '**Downloads:**\n\n{0}\n'.format('* `Reflex {0} RC - Build {1} ({2}) {3}\n  <https://github.com/downloads/photofroggy/Reflex/Reflex_{4}.zip>`_'.format(
                self.major, self.args.build, self.stamp[1], self.series, self.version
            )))
        
        if newd == data:
            writeout('>>> Editing downloads page did not work.')
            writeout('>>> Not sure why...')
            return
        
        downloads = open(dld, 'w')
        downloads.write(newd)
        downloads.close()
        
    def generate_docs(self):
        
        if not self.args.doc:
            return
        
        writeout('>> Generating documentation using sphinx-build...')
        
        ret = subprocess.call(['sphinx-build', '-q', self.args.docsource, self.args.docdest])
        
        if ret != 0:
            writeout('>> Something went wrong...')
            writeout('>> Exiting.')
            sys.exit(4)
        
        try:
            for cf in self.conf.doc.cf:
                subprocess.call(['cp', os.path.join(self.args.docdest, cf), './{0}'.format(cf)])
        except Exception as e:
            return
        
        self.conf.doc.source = self.args.docsource
        self.conf.doc.dest = self.args.docdest
    
    def push_changes(self):
        
        if not self.args.push:
            if self.args.verbose:
                writeout('>> Skipping git push...')
            return
        
        writeout('>> Pushing updates to github...')
        
        if self.args.verbose:
            writeout('>>> Pushing to master...')
        
        if not self.commit():
            return
        
        if not self.args.doc:
            return
        
        if self.args.verbose:
            writeout('>>> Pushing to gh-pages...')
        
        origd = os.getcwd()
        os.chdir(self.args.docdest)
        
        self.commit('gh-pages')
        
        os.chdir(origd)
        
    def commit(self, branch='master'):
            
        ret = subprocess.call(['git', 'commit', '-a', '-m', '"Pushing build {0}"'.format(self.args.build)])
        
        if ret != 0:
            writeout('>>> Failed to commit changes...')
            writeout('>>> Cancelling pushes...')
            return False
        
        ret = subprocess.call(['git', 'push', 'origin', branch])
        
        if ret != 0:
            writeout('>>> Failed to push changes...')
            writeout('>>> Cancelling pushes...')
            return False
        
        return True
    
    def distribute(self):
        
        writeout('>> Building distribution...')
        
        cmd = [sys.executable, 'setup.py', '-q', 'sdist', '--formats=gztar,zip',
            '--dist-dir', '../dist']
        if self.args.upload:
            cmd.append('upload')
        
        ret = subprocess.call(cmd)
        
        if ret != 0:
            writeout('>> Something went wrong...')
            writeout('>> Exiting.')
            sys.exit(5)


if __name__ == '__main__':
    Build()
        

# EOF
