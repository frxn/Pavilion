#!python        

#  ###################################################################
#
#  Disclaimer and Notice of Copyright 
#  ==================================
#
#  Copyright (c) 2015, Los Alamos National Security, LLC
#  All rights reserved.
#
#  Copyright 2015. Los Alamos National Security, LLC. 
#  This software was produced under U.S. Government contract 
#  DE-AC52-06NA25396 for Los Alamos National Laboratory (LANL), 
#  which is operated by Los Alamos National Security, LLC for 
#  the U.S. Department of Energy. The U.S. Government has rights 
#  to use, reproduce, and distribute this software.  NEITHER 
#  THE GOVERNMENT NOR LOS ALAMOS NATIONAL SECURITY, LLC MAKES 
#  ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY 
#  FOR THE USE OF THIS SOFTWARE.  If software is modified to 
#  produce derivative works, such modified software should be 
#  clearly marked, so as not to confuse it with the version 
#  available from LANL.
#
#  Additionally, redistribution and use in source and binary 
#  forms, with or without modification, are permitted provided 
#  that the following conditions are met:
#
#  1. Redistributions of source code must retain the 
#     above copyright notice, this list of conditions 
#     and the following disclaimer. 
#  2. Redistributions in binary form must reproduce the 
#     above copyright notice, this list of conditions 
#     and the following disclaimer in the documentation 
#     and/or other materials provided with the distribution. 
#  3. Neither the name of Los Alamos National Security, LLC, 
#     Los Alamos National Laboratory, LANL, the U.S. Government, 
#     nor the names of its contributors may be used to endorse 
#     or promote products derived from this software without 
#     specific prior written permission.
#   
#  THIS SOFTWARE IS PROVIDED BY LOS ALAMOS NATIONAL SECURITY, LLC 
#  AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
#  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
#  IN NO EVENT SHALL LOS ALAMOS NATIONAL SECURITY, LLC OR CONTRIBUTORS 
#  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, 
#  OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
#  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
#  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
#  OF SUCH DAMAGE.
#
#  ###################################################################

#  sample command: pav show_tests hpl

import os,sys
import os.path
import logging
import subprocess
from fnmatch import fnmatch
from yapsy.IPlugin import IPlugin
from testConfig import YamlTestConfig

class showTests(IPlugin):

    def __init__(self):
        
        my_name = self.__class__.__name__

        self.logger = logging.getLogger('pav.' + my_name)
        self.logger.info('created instance of plugin: %s'% my_name)

    def add_parser_info(self, subparser): 
        
        parser_rts = subparser.add_parser("show_tests", help="show available tests")
        parser_rts.add_argument('testSuite')
        parser_rts.set_defaults(sub_cmds='show_tests')
        return 'show_tests'

    def cmd(self, args):
        
        test = args['testSuite'] 
        print "test of interest: " + test + "\n"
        #print "Args: " + args

        if args['verbose']:
            print "Command args -> %s" % args

        print "\n" + " ----------  Available Tests:  -------------"
        #I hard-coded this, the directory will be different elsewhere
        subprocess.Popen("ls", cwd="/users/lapid/pavilion2/Pavilion/test_suites/")

        #I also hard-coded this, the directory will be different elsewhere
        #(or is it already an environment variable somewhere?)
        root = '/users/lapid/pavilion2/Pavilion/test_suites/gzshared'
        pattern = '*' + test + '*'
        directoryList = []  
        for path, subdirs, files in os.walk(root):
            for name in files:
                if fnmatch(name, pattern):
                    print "\n"
                    print os.path.join(path, name)
        
        sys.exit()

if __name__ == "__main__":
    print ShowTests.__doc__
