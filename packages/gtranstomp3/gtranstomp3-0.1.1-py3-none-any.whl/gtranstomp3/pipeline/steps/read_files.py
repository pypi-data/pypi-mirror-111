class Readfile():

    def process(self, utils, logger):
        filenames = utils.check_input()
        words = []
        for filename in filenames:
            with open(utils.indir + filename, 'r') as f:
                for line in f:
                    words.append(line.strip())
        return words

