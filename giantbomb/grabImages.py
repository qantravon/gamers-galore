import xml.etree.ElementTree as ET
import requests
import os

giantBombWAPI = 'http://www.giantbomb.com/api/'
#giantBombKEY = ''
#giantBombKEY = ''
giantBombKEY = ''

def grabImage(id):
	_gameImages = requests.get(giantBombWAPI+'game/%s/?api_key=%s&field_list=image&format=xml' % (id, giantBombKEY))
	images = (ET.fromstring(_gameImages.text.encode('utf-8')).find('results')).find('image')
	if len(images) > 0:
		if len(images) < 5:
			return images[0].text
		else:
			return images[5].text
	else:
		return 'NONE'

def main():
	for i in range(16408,41803):
		if os.path.isfile('games/g'+str(i+1)+'.xml'):
			root = ET.parse('games/g'+str(i+1)+'.xml').getroot()
			with open("IDs.txt",'a') as file:
				file.write(str(i+1)+ ' ' + root[1].text.encode('utf-8')+'\n')
			_image = ET.SubElement(root, 'image')
			image = grabImage(i+1)
			_image.text = image
			tree = ET.ElementTree(root)
			f=open('Games/'+str(i+1)+'.xml', 'w')
			tree.write(f, encoding='utf-8', xml_declaration=True)
			f.close()
			#print image

if __name__ == '__main__':
	main()
