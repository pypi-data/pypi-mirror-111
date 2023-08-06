from gtranstomp3.utils import Utils
from gtranstomp3.logger import Logger
from gtranstomp3.pipeline.steps.get_user_input import CheckInput
from gtranstomp3.pipeline.steps.get_sentence import GetSentence
from gtranstomp3.pipeline.steps.translate_to_mp3 import TranslateToMp3
from gtranstomp3.pipeline.pipeline import Pipeline


def main():
    steps = [
        CheckInput(),
        GetSentence(),
        TranslateToMp3(),
    ]
    utils = Utils()
    logger = Logger.logger()
    p = Pipeline(steps)
    
    utils.cla()
    p.run(utils, logger)
    
    logger.info('Transform complete!')

if __name__ == '__main__':
    main()
