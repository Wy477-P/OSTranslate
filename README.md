## OSTranslate v1.0 Nov 17th 2024 ##

## HOW TO USE ##
Use a snipping tool to extract an image of some text, and it will automatically translate the text and put it into the output box.

You can change input/output languages at the bottom right. Input (left box) determines what language easyocr will look for. Output (right box) determines what language the text will be translated to.

You can also customize the translation site by using the box with the link to tell the web scraper which site to go to. Remember to include {text} so that any text you extract using easyOCR gets sent in the link.
Also, there is a box to the right of the link box which contains a few random characters. Those characters are the class in which the translated text will be stored in the html response of google translate, so if google translate ever updates, you can find that class using inspect element on the website and copying the name of the class that stores the response text.
