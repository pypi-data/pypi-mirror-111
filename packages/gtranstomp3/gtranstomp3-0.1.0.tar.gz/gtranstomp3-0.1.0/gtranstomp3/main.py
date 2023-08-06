from .utils import Utils
from .logger import Logger
from .pipeline.steps.get_user_input import CheckInput
from .pipeline.steps.get_sentence import GetSentence
from .pipeline.steps.translate_to_mp3 import TranslateToMp3
from .pipeline.pipeline import Pipeline


def main():
    steps = [
        CheckInput(),
        GetSentence(),
        TranslateToMp3(),
    ]
    utils = Utils()
    logger = Logger.logger()
    p = Pipeline(steps)
    
    file_input_opt = utils.cla()
    p.run(utils, logger, file_input_opt)
    
    logger.info('Transform complete!')

if __name__ == '__main__':
    main()
