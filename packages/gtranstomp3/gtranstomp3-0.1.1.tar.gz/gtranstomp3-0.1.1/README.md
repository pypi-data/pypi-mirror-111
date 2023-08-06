""IMPORTANT""
Browser driver is essential to work, please go to pypi.org/project/selenium/ find suitable driver under "Drivers" and put in the same directory you execute this program or in your $PATH 
Default browser is Chrome, to change, please add -d firefox/edge/safari after command, or --driver <drivername>

Input can be any type of text file, as long as it can be read.
gtranstomp3 is a tool that can translate English word or sentence into Traditional Chinese and get the example sentences if existed.
Then combine the text by the order of 3 English word, 1 Chinese word and all example sentences.
After combination, the result will be pronounced by 'Miss Google' and store into mp3 file.

All the input files must be store in 'input' directory where is the same directory you execute the file.
To use this function, add -i or --input

Batch of copy and paste is available, for example, you can copy the following words or phrases:

old
new
milk
apple
umbrella
momentum
Newton
make up
look into

But the word should be in the next line, otherwise it would be seen as a sentence.

To finish entering, just press enter for none input to start translating and formatting.
The mp3 file will be store in the 'output' directorry, where is the same directory you execute the file.


HOW TO USE
python main.py -option
-i --input  use file as input word
-d --driver change browser 
