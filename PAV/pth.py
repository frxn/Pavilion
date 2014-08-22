#!/usr/bin/env python
"""Pavilion Cluster Test Harness (main module)"""

import sys,os

# support creating Python style command line interfaces
import argparse

# support for dynamically loading new features/commands from a "plugins" directory
sys.path.append("../special-pkgs")
#print sys.path
from yapsy.PluginManager import PluginManager

# set up logging
import logging
master_log_file = '/tmp/pth.log'
logger = logging.getLogger('pth')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(filename=master_log_file)
fh.setFormatter(formatter)
logger.addHandler(fh)

global _debug

# look for modules relative to where this program is located
sys.path.append(os.path.join(os.path.dirname(__file__), "../modules"))
os.environ['PV_SRC_DIR'] = os.getcwd()
if (os.environ.get('PV_SRC_DIR')):
    sys.path.append(os.environ.get('PV_SRC_DIR'))

# stub foo sub-command implemented in the main
def foo():
    print "running foo"
    
def usage():
    print __doc__
        
def main():
    """Main entry point for the test harness."""

    _debug = 0
    func_map = {}
    
    # construct main input arguments
    parser = argparse.ArgumentParser(prog="Pavilion")
    subparser = parser.add_subparsers(title="commands", help='sub-commands')
    parser.add_argument("-v", "--verbose", help="provide verbose output", action="store_true")
    #parser.add_argument('-g', '--hello', help='prints greeting', action="store_true")
    parser_foo = subparser.add_parser('foo', help="foo help message")
    parser_foo.set_defaults(sub_cmds='foo')

    print "Running from -> %s " % os.environ['PV_SRC_DIR']
    print "Logging to -> %s" % master_log_file

    # Dynamic support for adding commands...
    # Find and load the sub-commands (plug-ins) and their arguments

    # Build the manager
    PavPluginManager = PluginManager()
    # Inform where to find plug-ins
    # User can add more places to look by setting ENV PV_PLUGIN_DIR
    plugin_places = ['../plugins']
    if (os.environ.get('PV_PLUGIN_DIR')):
        plugin_places.append(os.environ.get('PV_PLUGIN_DIR'))
    PavPluginManager.setPluginPlaces(plugin_places)
    # Load all the plug-ins
    logger.info('Loading plugins')
    PavPluginManager.collectPlugins()
    
    # create a hash that maps all sub-commands to their respective function call
    for pluginInfo in PavPluginManager.getAllPlugins():
                    
        try: 
            # let new functions add to the help line
            func = pluginInfo.plugin_object.add_parser_info(subparser)
            # dictionary of function name to object mapping
            func_map[func] = pluginInfo.plugin_object
        except:
            print "Error using add_help_info method for %s" % pluginInfo.plugin_object
            

    # turn the input arguments into a dictionary
    args = vars(parser.parse_args())
    # record the command line selections
    logger.info('cmd line args: %s' % args)

       
    # Process sub-commands, most of which should be found
    # in the plug-ins directory.
    print "Invoke command: -> " + args['sub_cmds']
    if args['sub_cmds'] == 'foo':
        foo()
    else:
        # invoke the cmd method of the object that corresponds to
        # the command selected
        getattr(func_map[args['sub_cmds']], 'cmd')(args)
        


# this gets called if it's run as a script/program
if __name__ == '__main__':
    # pass entire command line to main except for the command name
    sys.exit(main())