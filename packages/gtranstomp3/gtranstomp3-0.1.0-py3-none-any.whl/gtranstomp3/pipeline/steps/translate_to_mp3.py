from googletrans import Translator
from gtts import gTTS

from .step import Step

class TranslateToMp3(Step):
   
    """
    word is one of the user input
    data stores the sentenses get from google translate
    The order of prounouce will be English word 3 times in slow, Chinese translate 1 time, all of example sentences 1 time, and end sentence.
    The output will store in the output directory under the same directory where execute the program.
    """

    def process(self, word, data, utils, logger):
        translator = Translator()
        i = word
        if not i:
            pass
        else:
            dest_text = translator.translate(i, dest = 'zh-TW').text
            tts_en1 = gTTS(i + '. ' + i + '. ' + i, slow = True)
            tts_zh = gTTS(dest_text, lang = 'zh-TW')
            sens = data
            if sens in ([], ''):
                tts_en2 = gTTS('No example sentence for this word.')
            else:
                tts_en2 = gTTS('. '.join(sens))
            tts_end = gTTS('This is the end of ' + i)
            with open(utils.outdir + i + '.mp3', 'wb') as f:
                tts_en1.write_to_fp(f)
                tts_zh.write_to_fp(f)
                tts_en2.write_to_fp(f)
                tts_end.write_to_fp(f)

