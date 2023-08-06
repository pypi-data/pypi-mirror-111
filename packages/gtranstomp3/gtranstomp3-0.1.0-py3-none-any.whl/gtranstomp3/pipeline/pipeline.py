from .steps.step import StepException
from .steps.read_files import Readfile

class Pipeline:

    def __init__(self, steps):
        self.steps = steps

    def run(self, utils, logger, file_inputs):
        
        if file_inputs:
            word = Readfile.process(utils, logger)
        else:
            word = None
        data = None

        utils.check_dir()
        words = self.steps[0].process(word, data, utils, logger)
        for word in words:
            for step in self.steps[1:]:
                try:
                    data = step.process(word, data, utils, logger)
                except StepException as e:
                    print('Exception happened:', e)
                    break
