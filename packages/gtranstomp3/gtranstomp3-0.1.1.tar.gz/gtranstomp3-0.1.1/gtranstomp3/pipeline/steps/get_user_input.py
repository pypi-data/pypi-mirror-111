import re

from googletrans import Translator

from .step import Step

class CheckInput(Step):
    
    """
    divided the input types for different treat
    """

    def process(self, word, data, utils, logger):
        trans = Translator()
        if isinstance(word, (list, tuple)):
            result = []
            for w in word:
                if w.strip() == '':     
                    continue
                else:
                    result.extend(Formatting.process(self, w, trans, utils, logger))
        elif isinstance(word, str):
            if ' ' in word:
                result = Formatting.process(self, word, trans, utils, logger)
            else:
                result = word
        else:
            print('user input mode')
            word = None
            result = GetUserInput.process(self, word, trans, utils, logger)
        return result

class GetUserInput(Step):
    
    """
    user input the word they want to translate in once, after input, the process will automaticly complete.
    """

    def process(self, word, trans, utils, logger):  
        userins = []
        while True:
            userin = input('Please enter the word(s) you want to translate (double press enter to stop enter): ')
            if utils.check_files(userin):
                logger.warning('file exists')
                continue
            elif not userin:
                logger.info('start formatting!')
                break   
            else:
                userins.extend(Formatting.process(self, userin, trans, utils, logger))
        return userins

class Formatting(Step):

    def process(self, word, trans, utils, logger):
        userins = []
        if utils.check_files(word):
            logger.warning('file exists') 
        elif trans.translate(word, dest = 'zh-TW').text.lower().strip('.') == word:  #check if the word is readable
            logger.warning(f'Translate error: {word} may not be a word.')
        else:   #delete words that are not english 
            text = ''
            for i in word.split():
                if re.search('[a-zA-Z]', i):
                    text = text + i + ' '
            if text:
                userins.append(text.strip())
        return userins
