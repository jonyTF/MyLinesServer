import cv2
import pytesseract
import pprint

config = ('-l eng --oem 1 --psm 3')

im = cv2.imread('photos/9.png', cv2.IMREAD_GRAYSCALE)
text = pytesseract.image_to_string(im, config=config)

print(text)

def isName(text, i):
    if i+1 < len(text):
        return text[i].isupper() and text[i+1].isupper()
    else:
        return False

lines = {}
cur_line = ''
cur_character = ''
character_finished = False
within_parenthesis = False
i = 0
line_num = 0
while i < len(text):
    if text[i] == '(':
        within_parenthesis = True
    elif text[i] == ')':
        within_parenthesis = False
        i += 1
        continue

    if not within_parenthesis:
        if not character_finished:
            if isName(text, i):
                while text[i].isupper() or text[i] == ' ':
                    cur_character += text[i]
                    i += 1
                    if i >= len(text):
                        break
                character_finished = True
        else:
            if not isName(text, i):        
                cur_line += text[i]
            else: 
                cur_line = cur_line.replace('\n', ' ').strip()
                if cur_character in lines:
                    lines[cur_character].append((line_num, cur_line))
                else:
                    lines[cur_character] = [(line_num, cur_line)]   
                line_num += 1
                character_finished = False
                cur_line = ''
                cur_character = ''
                i -= 1
    i += 1
cur_line = cur_line.replace('\n', ' ').strip()
if cur_character in lines:
    lines[cur_character].append((line_num, cur_line))
else:
    lines[cur_character] = [(line_num, cur_line)]  

print(lines)
#pprint.pprint(lines)