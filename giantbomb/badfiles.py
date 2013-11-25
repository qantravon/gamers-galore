import xml.etree.ElementTree as ET
import os

def removeBadFiles():
	for i in range(41802):
		if os.path.isfile('games/g'+str(i+1)+'.xml'):
			root = ET.parse('games/g'+str(i+1)+'.xml').getroot()
			if root[2].text == None:
				if root[4].text == None:
					os.remove('games/g'+str(i+1)+'.xml')
					#print i+1
	
def main():
	removeBadFiles()

if __name__ == '__main__':
	main()