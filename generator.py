import os
import sys
from bs4 import BeautifulSoup
import re
import shutil

#Static field
scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
normalizeMap = {"Cb":"B", "Db":"C#", "Eb":"D#", "Fb":"E", "Gb":"F#", "Ab":"G#", "Bb":"A#",  "E#":"F", "B#":"C"}
reverseMap = {"B": "Cb", "C#": "Db", "D#":"Eb", "E":"Fb", "F#":"Gb", "G#":"Ab", "A#":"Bb"}
mode = 1 #using "#"
basePath = os.getcwd()

#Get what need to be replaced
def getChord(string):
	chord = re.search('[CDEFGAB](b|#)?', string)
	return chord.group()

#Transposing function, amount counted by half-step, get what to replace
def transposeChord(chord, amount):
	#match regex
	chord = getChord(chord)
	#normalize chord
	if normalizeMap.get(chord) != None:
		chord = normalizeMap[chord]
	else:
		pass
	i = (scale.index(chord) + amount) % len(scale)
	#normalize i
	if i < 0:
		i = i + len(scale)
	else:
		pass
	return scale[i]


def generateFiles(ori, new): #filename after changing
	shutil.copy(basePath + "\\" + ori, basePath + "\\" + new)
	return

def getAmount(src, dst):
	return scale.index(dst) - scale.index(src)

def editHTML(filename, amount):
	with open(filename, "r") as fp:
		txt = fp.read()
		soup = BeautifulSoup(txt, 'html.parser')
		chords = soup.find_all('b')
		for c in range(0, len(chords)):
			transChord = transposeChord(chords[c].string, amount)
			if mode == 1:
				pass
			else:
				if reverseMap.get(transChord) != None:
					transChord = reverseMap[transChord]
				else:
					pass
			newChord = re.sub('[CDEFGAB](b|#)?', transChord, chords[c].string)
			chords[c].string.replace_with(newChord)
	with open(filename, "wb") as file:
		file.write(soup.prettify("latin-1"))

def main():
	usage = """
Place this script in the same folder as your .html.
Usage: generator.py [filename.html] [base tone]
Replace filename.html and base tone with yours (without bracket [])
Example: generator.py "A- De gloria en gloria.html"
"""
	if len(sys.argv) != 2:
		print("Invalid parameters.")
		print(usage)
		return

	name = sys.argv[1]
	baseTone = name[:name.index("-")]

	#normalize tone
	if normalizeMap.get(baseTone) != None:
		baseTone = normalizeMap[baseTone]

	for j in range(0, 12):
		if scale[j] == baseTone:
			continue
		#generate new html file here
		newTone = scale[j]
		amount = getAmount(baseTone, newTone)
		temp = name.index("-")

		#change name in mode 2
		if mode == 1:
			pass
		else:
			if reverseMap.get(newTone) != None:
				newTone = reverseMap[newTone]
			else:
				pass
		newName = newTone + name[temp:]
		generateFiles(name, newName)
		editHTML(newName, amount)


if __name__ == '__main__':
	mode = int(input("Type 1 for \"#\" mode or 2 for \"b\" mode:  "))
	if mode != 1 and mode != 2:
		print("Wrong! Automatically set to default mode = 1")
		mode = 1
	main()



