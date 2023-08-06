import os
import getopt
import sys


class Utils:

    def __init__(self):
        self.outdir = 'output/'
        self.indir = 'input/'

    def check_dir(self):
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def check_files(self, word):
        filename = word + '.mp3'
        return os.path.isfile(self.outdir + filename)

    def check_input(self):
        if os.path.exists(self.indir):
            return os.listdir(self.indir)
        else:
            return None
    
    #Comment Line Arguments
    def cla(self):
        short_opts = 'i'
        long_opts = 'input'
        try:
            opts, args = getopt.getopt(sys.argv[1], short_opts, long_opts)
        except getopt.GetoptError:
            print('python main.py i')
        if opts:
            return True
        else:
            return False
