import pygame, sys, tkinter, math, random, time
from tkinter import filedialog

pygame.init()
tkinter.Tk().withdraw()

WIDTH, HEIGHT = 1280, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption('PokéPaint')

background = pygame.transform.scale(
	pygame.image.load('../assets/paintproject_background.png'),(1280,960))
screen.blit(background, (0,0))

logo = pygame.transform.scale(
	pygame.image.load('../assets/pokemon.png'),(300,111))
logowidth = logo.get_width()
screen.blit(logo, (0,0))

canvasRect = pygame.Rect(416,310,854,480)
canvasRectOutline =  pygame.Rect(411,305,864,490)
pygame.draw.rect(screen,'black',canvasRectOutline)
pygame.draw.rect(screen,'white',canvasRect)
screenCap=screen.subsurface(canvasRect).copy()

colorPalette = pygame.transform.scale(
	pygame.image.load('../assets/fullrbgcolorpalette.png'),(150,150))
screen.blit(colorPalette,(10,645))
colorPaletteRect = pygame.Rect(10,645,150,150)

tools=['pencil', 'eraser','spraypaint','paintbrush','line','ellipse','rectangle',]
stamps=['pokeball','greatball','ultraball','masterball','duskball']
stamppage=0
uiItems=['save','upload','garbage']
tool='pencil'
toolRects=[]
uiRects=[]
images=[]
uiImages=[]
stampimages=[]
user_size=5
fill_status=0


for t in tools:
	image = pygame.transform.scale(
		pygame.image.load(f'../assets/{t}.png'),(60,60))
	images.append(image)

for s in stamps:
	image = pygame.transform.scale(
		pygame.image.load(f'../assets/{s}.png'),(60,60))
	stampimages.append(image)

for u in uiItems:
	image = pygame.transform.scale(
		pygame.image.load(f'../assets/{u}.png'),(60,60))
	uiImages.append(image)

pokeballstamp = pygame.transform.scale(
	pygame.image.load('../assets/pokeball.png'),(100,100))
pygame.display.set_icon(pokeballstamp)
greatballstamp = pygame.transform.scale(
	pygame.image.load('../assets/greatball.png'),(100,100))
ultraballstamp = pygame.transform.scale(
	pygame.image.load('../assets/ultraball.png'),(100,100))
masterballstamp = pygame.transform.scale(
	pygame.image.load('../assets/masterball.png'),(100,100))
duskballstamp = pygame.transform.scale(
	pygame.image.load('../assets/duskball.png'),(100,100))

stamppageleftRect = pygame.Rect(180,390,70,70)
stamppagerightRect = pygame.Rect(320,390,70,70)
stamppagerect = pygame.Rect(250,390,70,70)

rightarrow = pygame.transform.scale(
		pygame.image.load(f'../assets/rightarrow.png'),(60,60))

leftarrow = pygame.transform.scale(
		pygame.image.load(f'../assets/leftarrow.png'),(60,60))


pencilRect = pygame.Rect(10,310,70,70)
toolRects.append(pencilRect)

eraserRect = pygame.Rect(90,310,70,70)
toolRects.append(eraserRect)

spraypaintRect = pygame.Rect(170,310,70,70)
toolRects.append(spraypaintRect)

paintbrushRect = pygame.Rect(250,310,70,70)
toolRects.append(paintbrushRect)

lineRect = pygame.Rect(330,310,70,70)
toolRects.append(lineRect)

ellipseRect = pygame.Rect(10,390,70,70)
toolRects.append(ellipseRect)

rectRect = pygame.Rect(90,390,70,70)
toolRects.append(rectRect)

saveRect = pygame.Rect(1040,10,70,70)
uiRects.append(saveRect)

uploadRect = pygame.Rect(1120,10,70,70)
uiRects.append(uploadRect)

garbageRect = pygame.Rect(1200,10,70,70)
uiRects.append(garbageRect)

selected_color='black'

FPS = pygame.time.Clock()

omx, omy = 0, 0



def main(tool,screenCap,selected_color,fill_status,stamppage):
	dmx, dmy = 0, 0
	while True:
		for event in pygame.event.get():
			print(event)
			if event.type ==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if saveRect.collidepoint(mx,my):
						dmx, dmy = event.pos
						save()
						#pygame.event.clear()
						pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos = event.pos, button = 1, touch = False, window = None))
						
						continue
						'''
						When calling the save function, the pygame window goes out of focus
						You must click back on the window to draw again making it look like it is broken
						'''
					if uploadRect.collidepoint(mx,my):
						dmx,dmy = event.pos
						upload()
						#pygame.event.clear()
						pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos = event.pos, button = 1, touch = False, window = None))
						continue
						'''
						When calling the upload function, the pygame window goes out of focus
						You must click back on the window to draw again making it look like it is broken
						'''
					if garbageRect.collidepoint(mx,my):
						pygame.draw.rect(screen,'white',canvasRect)
					if stamppageleftRect.collidepoint(mx,my):
						if stamppage == 0:
							stamppage = 4
						else:
							stamppage-=1
					if stamppagerightRect.collidepoint(mx,my):
						if stamppage == 4:
							stamppage = 0
						else:
							stamppage+=1
					dmx, dmy = event.pos
					if canvasRect.collidepoint(event.pos):
						if tool == 'paintbrush':
							pygame.draw.circle(screen,selected_color,(mx,my),user_size-2)
						if tool == 'eraser':
							pygame.draw.circle(screen,'white',(mx,my),user_size-2)

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
						if canvasRect.collidepoint(mx,my):

							if tool == 'paintbrush':
								pygame.draw.circle(screen,selected_color,(mx,my),user_size-2)
							if tool == 'eraser':
								pygame.draw.circle(screen,'white',(mx,my),user_size-2)
						screenCap=screen.subsurface(canvasRect).copy()
						
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					if fill_status == 0:
						fill_status = 1
					else:
						fill_status = 0

		mx,my = pygame.mouse.get_pos()
		mb = pygame.mouse.get_pressed()
		keys= pygame.key.get_pressed()

		#updating the ui
		for toolrect in toolRects:
			if tool in tools:
				if toolrect.collidepoint(mx,my):
					pygame.draw.rect(screen,'red',toolrect)
				elif tools.index(tool) == toolRects.index(toolrect):
					pygame.draw.rect(screen,'green',toolrect)
				else:
					pygame.draw.rect(screen,'white',toolrect)
			else:
				if toolrect.collidepoint(mx,my):
					pygame.draw.rect(screen,'red',toolrect)
				else:
					pygame.draw.rect(screen,'white',toolrect)
			screen.blit(
					images[toolRects.index(toolrect)],(toolrect.x+5,toolrect.y+5))
				
			if mb[0] and toolrect.collidepoint(mx,my):
				tool = tools[toolRects.index(toolrect)]

		for uiRect in uiRects:
			if uiRect.collidepoint(mx,my):
				pygame.draw.rect(screen,'red',uiRect)
			else:
				pygame.draw.rect(screen,'white',uiRect)
			screen.blit(
					uiImages[uiRects.index(uiRect)],(uiRect.x+5,uiRect.y+5))
		
		if tool in stamps:
			if stamppagerect.collidepoint(mx,my):
				pygame.draw.rect(screen,'red',stamppagerect)
			elif stamps.index(tool) == stamppage:
				pygame.draw.rect(screen,'green',stamppagerect)
			else:
				pygame.draw.rect(screen,'white',stamppagerect)
		else:
			if stamppagerect.collidepoint(mx,my):
				pygame.draw.rect(screen,'red',stamppagerect)
			else:
				pygame.draw.rect(screen,'white',stamppagerect)

		if stamppageleftRect.collidepoint(mx,my):
			pygame.draw.rect(screen,"red",stamppageleftRect)
		else:
			pygame.draw.rect(screen,"light gray",stamppageleftRect)
		
		if stamppagerightRect.collidepoint(mx,my):
			pygame.draw.rect(screen,"red",stamppagerightRect)
		else:
			pygame.draw.rect(screen,"light gray",stamppagerightRect)

		screen.blit(
				leftarrow,(stamppageleftRect.x+5,stamppageleftRect.y+5))
		
		screen.blit(
				rightarrow,(stamppagerightRect.x+5,stamppagerightRect.y+5))
		
		screen.blit(
				stampimages[stamppage],(stamppagerect.x+5,stamppagerect.y+5))
		#updating the ui - end

		if mb[0] and canvasRect.collidepoint(mx,my) and canvasRect.collidepoint(dmx,dmy):
			draw(tool,screenCap,user_size,selected_color,keys,omx,omy,mx,my,dmx,dmy,fill_status)

		if mb[0] and colorPaletteRect.collidepoint(mx,my):
			distance = math.sqrt((colorPaletteRect.center[0]-mx)**2 + (colorPaletteRect.center[1]-my)**2)
			if distance<=75:
				selected_color=screen.get_at((mx,my))

		if mb[0] and stamppagerect.collidepoint(mx,my):
			tool = stamps[stamppage]
		
		omx,omy = mx,my
		FPS.tick(60)
		pygame.display.flip()



def draw(tool,screenCap,user_size,selected_color,keys,omx,omy,mx,my,dmx,dmy,fill_status):
	screen.set_clip(canvasRect)
	if tool == 'pencil':
		pygame.draw.line(screen,selected_color,(omx,omy),(mx,my))
	elif tool == 'eraser':
		pygame.draw.line(screen,"white",(omx,omy),(mx,my),user_size)
	elif tool == 'spraypaint':
		pixelstopaint=[]
		while True:
			point = (random.randint(mx-20,mx+20),random.randint(my-20,my+20))
			distance = math.sqrt((point[0]-mx)**2 + (point[1]-my)**2)
			if distance<=user_size*3:
				pixelstopaint.append(point)
				break
		for p in pixelstopaint:
			pygame.draw.circle(screen,selected_color,p,1)
	elif tool == 'paintbrush':
		pygame.draw.line(screen,selected_color,(omx,omy),(mx,my),user_size)
	elif tool == 'line':
		screen.blit(screenCap,canvasRect)
		pygame.draw.line(screen,selected_color,(dmx,dmy),(mx,my))
	elif tool == 'ellipse':
		if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
			screen.blit(screenCap,canvasRect)
			distance = math.sqrt((dmx-mx)**2 + (dmy-my)**2)
			pygame.draw.circle(screen,selected_color,(dmx,dmy),distance,fill_status)
		else:
			screen.blit(screenCap,canvasRect)
			if dmx>mx:
				if dmy>my:
					ellipseDrawRect = pygame.Rect(mx,my,dmx-mx,dmy-my)
				else:
					ellipseDrawRect = pygame.Rect(mx,dmy,dmx-mx,my-dmy)
			else:
				if dmy>my:
					ellipseDrawRect = pygame.Rect(dmx,my,mx-dmx,dmy-my)
				else:
					ellipseDrawRect = pygame.Rect(dmx,dmy,mx-dmx,my-dmy)
			pygame.draw.ellipse(screen,selected_color,ellipseDrawRect,fill_status)
	elif tool == 'rectangle':
		screen.blit(screenCap,canvasRect)
		if dmx>mx:
			if dmy>my:
				pygame.draw.rect(screen,selected_color,(mx,my,dmx-mx,dmy-my),fill_status)
			else:
				pygame.draw.rect(screen,selected_color,(mx,dmy,dmx-mx,my-dmy),fill_status)
		else:
			if dmy>my:
				pygame.draw.rect(screen,selected_color,(dmx,my,mx-dmx,dmy-my),fill_status)
			else:
				pygame.draw.rect(screen,selected_color,(dmx,dmy,mx-dmx,my-dmy),fill_status)
	elif tool == 'pokeball':
		screen.blit(screenCap,canvasRect)
		screen.blit(pokeballstamp,(mx-50,my-50))
	elif tool == 'greatball':
		screen.blit(screenCap,canvasRect)
		screen.blit(greatballstamp,(mx-50,my-50))
	elif tool == 'ultraball':
		screen.blit(screenCap,canvasRect)
		screen.blit(ultraballstamp,(mx-50,my-50))
	elif tool == 'masterball':
		screen.blit(screenCap,canvasRect)
		screen.blit(masterballstamp,(mx-50,my-50))
	elif tool == 'duskball':
		screen.blit(screenCap,canvasRect)
		screen.blit(duskballstamp,(mx-50,my-50))
	screen.set_clip(None)

def save():
	try:
		fname=tkinter.filedialog.asksaveasfilename(defaultextension=".png")
		pygame.image.save(screen.subsurface(canvasRect),fname)
		
	except:
		print('No file selected')

def upload():
	try:
		fname=filedialog.askopenfilename()
		dot = fname.rfind('.')
		ext = fname[dot+1:]
		imagewidth = image.get_width()
		imageheight = image.get_height()
		if ext == 'png':
			image = pygame.image.load(fname)
			if imagewidth>canvasRect.width:
				if imageheight>canvasRect.height:
					pygame.transform.scale(image,(canvasRect.width,canvasRect.height))
				else:
					pygame.transform.scale(image,(canvasRect.width,imageheight))
			else:
				if imageheight>canvasRect.height:
					pygame.transform.scale(image,(imagewidth,canvasRect.height))
			pygame.draw.rect(screen,'white',canvasRect)
			screen.blit(image,(250,250))
			
	except:
		print('No file selected')
	
main(tool,screenCap,selected_color,fill_status,stamppage)