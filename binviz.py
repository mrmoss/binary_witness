#!/usr/bin/env python2
import pygame

def init_screen(size):
	return pygame.display.set_mode(size,pygame.RESIZABLE|pygame.DOUBLEBUF)

def pyscale(size,scale):
	return (max(1,int(size[0]*scale)),max(1,int(size[1]*scale)))

def quit(status):
	pygame.quit()
	exit(status)

if __name__=='__main__':
	screen=init_screen((600,600))
	surface_size=(100,100)
	surface=pygame.Surface(surface_size)
	surface.fill((0,0,0))

	keys={}
	for ii in range(0,300):
		keys[ii]=False

	offset=[(screen.get_size()[0]-surface_size[0])/2,(screen.get_size()[1]-surface_size[1])/2]
	scale=1
	pos_change=-5
	scale_change=0.3
	old_cursor_pos=None

	while True:
		pygame.display.update()

		cursor=pygame.mouse.get_pos()
		cursor=[cursor[0]-screen.get_size()[0]/2,cursor[1]-screen.get_size()[1]/2]

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				quit(0)
			elif event.type==pygame.KEYDOWN:
				keys[event.key]=True
			elif event.type==pygame.KEYUP:
				keys[event.key]=False
			elif event.type==pygame.VIDEORESIZE:
				screen=init_screen((event.w,event.h))
			elif event.type==pygame.MOUSEBUTTONDOWN:
				if event.button==1 and not old_cursor_pos:
					old_cursor_pos=cursor
				elif event.button==4:
					scale-=scale_change
					#offset[0]+=(cursor[0]+surface_size[0]/2)*scale_change
					#offset[1]+=(cursor[1]+surface_size[1]/2)*scale_change
					offset[0]+=(surface_size[0]/2)*scale_change
					offset[1]+=(surface_size[1]/2)*scale_change
				elif event.button==5:
					scale+=scale_change
					#offset[0]-=(cursor[0]+surface_size[0]/2)*scale_change
					#offset[1]-=(cursor[1]+surface_size[1]/2)*scale_change
					offset[0]-=(surface_size[0]/2)*scale_change
					offset[1]-=(surface_size[1]/2)*scale_change
			elif event.type==pygame.MOUSEBUTTONUP:
				if event.button==1 and old_cursor_pos:
					offset[0]+=cursor[0]-old_cursor_pos[0]
					offset[1]+=cursor[1]-old_cursor_pos[1]
					old_cursor_pos=None

		screen.fill((100,100,80))
		real_off=(offset[0],offset[1])
		if old_cursor_pos:
			real_off=(offset[0]+cursor[0]-old_cursor_pos[0],offset[1]+cursor[1]-old_cursor_pos[1])
		screen.blit(pygame.transform.rotozoom(surface,0,scale),real_off)
		pygame.display.flip()

		if keys[pygame.K_ESCAPE]:
			quit(0)
		if keys[pygame.K_LEFT]:
			offset[0]-=pos_change
		if keys[pygame.K_RIGHT]:
			offset[0]+=pos_change
		if keys[pygame.K_UP]:
			offset[1]-=pos_change
		if keys[pygame.K_DOWN]:
			offset[1]+=pos_change
		if keys[ord('0')]:
			offset=[(screen.get_size()[0]-surface_size[0])/2,(screen.get_size()[1]-surface_size[1])/2]
			scale=1
			old_cursor_pos=None
