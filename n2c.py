#! /usr/bin/python


# TODO
# blank prompts
# replace <br> with <div> maybe
# inline notation
# integrate with anki import feature

import re, sys

class FileParser:
	
	def __init__(self): # my regex so far: r'^\s*\*\s*(.*)'
		self.subjectRe = re.compile(r'^\s*\*\s*(.*)') 
		self.predicateRe = re.compile(r'^\s*{(.*?)}(.*)')
		self.learnRe = re.compile(r'^\?(.*)')
		
		self.reset()

		
	def reset(self):
		self.dataset = []
		self.learnset = []
		self.currentSubject = None
		self.currentVerb = None
		self.currentObject = None
		
	def addLearn(self, line):
		self.learnset.append(line.strip())
		
	def flush(self):
		if (self.currentSubject != None) and (self.currentVerb != None) and (self.currentObject != None):
			self.currentObject = self.currentObject.strip()
			self.currentVerb = self.currentVerb.strip()
			self.dataset.append((self.currentSubject, self.currentVerb, self.currentObject))
		self.currentVerb = None
		self.currentObject = None
		
	def updateSubject(self, line):
		self.flush()
		self.currentSubject = line.strip()
		#print "subject updated: " + self.currentSubject
		
	def updatePredicate(self, verb, obj):
		self.flush()
		self.currentVerb = verb.strip()
		self.currentObject = obj.strip()
		
	def appendPredicate(self, line):
		if self.currentObject == None:
			self.currentObject = ''
		self.currentObject = self.currentObject + '\n' + line.strip()
		
	def removeComment(self, line):
		return line.split('//')[0]

	def interpretLine(self, line):
		line = self.removeComment(line)
		
		m = self.learnRe.match(line)
		if m:
			self.addLearn(m.group(1))
			return
		
		m = self.subjectRe.match(line)
		if m:
			self.updateSubject(m.group(1))
			return
			
		m = self.predicateRe.match(line)
		if m:
			self.updatePredicate(m.group(1),m.group(2))
		else:
			self.appendPredicate(line)

	def parseFile(self, filepath = None):
		if filepath == None:
			if len(sys.argv) < 2:
				print 'Not enough parameters!'
				return False
			self.filepath = sys.argv[1]
		else:
			self.filepath = filepath
		
		if self.filepath[-4:] != '.txt':
			print 'Filename must end in .txt'
			return False
		
		try:
			source = open(self.filepath)
		except:
			print 'exception! '+ sys.argv[1]
			return False
		
		# what happens if the file is too big?	
		lines = source.read().splitlines() 
		print self.filepath, len(lines)
		source.close()
		
		for line in lines:
			self.interpretLine(line)

		self.flush() # add the terminal value
		return True
		
	def dump(self):
		for t in self.dataset:
			print t[0] + ': ' + t[1] + '\t' + t[2]
		for i in self.learnset:
			print 'learn: ' + i + '\t(no back)'
			
	def dumpToFile(self, filepath=None):
		if self.parseFile(filepath) != True:
			return
		outpath = self.filepath[0:-4] + '-READY_FOR_ANKI.txt' # disaster!
		try:
			f = open(outpath, 'w')
		except:
			print 'problem opening outfile: '+ outpath
			return 
		for t in self.dataset:
			f.write(self.cardLineFromTuple(t))
		for i in self.learnset:
			f.write('learn: ' + i + '\t(no back)' + '\n')
		f.close()
		self.reset()
		
	def cardLine(self, front, back):
		template = front + '\t' + back
		template = template.replace('\n','<br>')
		return template + '\n'
		
	def cardLineFromTuple(self, t):
		verb = t[1]
		front = t[0].strip()
		back = t[2].strip()
		
		if verb == ':': # {:} style
			return self.cardLine(front, back)
			
		if verb.find('|') != -1: # : and | together is not possible
			# this is so confusing
			options = verb.split('|')
			forwardVerb = ': ' + options[0]
			reverseVerb = ': ' + options[1]
			forwardFront = front + forwardVerb
			reverseFront = back + reverseVerb
			firstCard = self.cardLine(forwardFront, back)
			secondCard = self.cardLine(reverseFront, front)
			return firstCard + secondCard
			
		if verb.startswith('<<'):
			if verb == '<<':
				return self.cardLine(back, front)
			else:
				return self.cardLine(back + ': ' + verb[2:], front)
		
		# normal case
		verb = ': ' + t[1]
		front = front + verb
		return self.cardLine(front, back)
		
	def runAsAnkiPlugin(self):
		action = QAction("Convert Notes...", mw)
		mw.connect(action, SIGNAL("triggered()"), self.actionConvertNotes)
		mw.form.menuTools.addAction(action)
		
	def actionConvertNotes(self):
		filepath = QFileDialog.getOpenFileName(mw, 'Choose File', 
			mw.pm.base, "Plain text files (*.txt)")
		self.dumpToFile(filepath)


p = FileParser()
# go go go!
try:
	from aqt import mw
	from aqt.utils import showInfo
	from aqt.qt import *
	p.runAsAnkiPlugin()
except ImportError:
	# not anki addon, must be run from command line
	p.dumpToFile()
