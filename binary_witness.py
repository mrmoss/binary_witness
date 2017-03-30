#!/usr/bin/env python2
import pygame
import time

def init_screen(size):
	return pygame.display.set_mode(size,pygame.RESIZABLE|pygame.DOUBLEBUF)

def pyscale(size,scale):
	return (max(1,int(size[0]*scale)),max(1,int(size[1]*scale)))

def get_time():
	return time.time()

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

	old_time=get_time()
	offset=[(screen.get_size()[0]-surface_size[0])/2,(screen.get_size()[1]-surface_size[1])/2]
	scale=2
	min_scale=0.2
	max_scale=10
	pos_change=-800
	scale_change=200
	old_cursor_pos=None

	while True:
		pygame.display.update()
		new_time=get_time()
		dt=(new_time-old_time)
		old_time=new_time

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
					real_change=scale_change*dt
					if scale-real_change<min_scale:
						real_change=scale-min_scale
					scale-=real_change
					#offset[0]+=(cursor[0]+surface_size[0]/2)*real_change
					#offset[1]+=(cursor[1]+surface_size[1]/2)*real_change
					offset[0]+=(surface_size[0]/2)*real_change
					offset[1]+=(surface_size[1]/2)*real_change
				elif event.button==5:
					real_change=scale_change*dt
					if scale+real_change>max_scale:
						real_change=max_scale-scale
					scale+=real_change
					#offset[0]-=(cursor[0]+surface_size[0]/2)*real_change
					#offset[1]-=(cursor[1]+surface_size[1]/2)*real_change
					offset[0]-=(surface_size[0]/2)*real_change
					offset[1]-=(surface_size[1]/2)*real_change
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
		if keys[pygame.K_a]:
			offset[0]-=pos_change*scale*dt
		if keys[pygame.K_d]:
			offset[0]+=pos_change*scale*dt
		if keys[pygame.K_w]:
			offset[1]-=pos_change*scale*dt
		if keys[pygame.K_s]:
			offset[1]+=pos_change*scale*dt
		if keys[ord('0')]:
			offset=[(screen.get_size()[0]-surface_size[0])/2,(screen.get_size()[1]-surface_size[1])/2]
			scale=1
			old_cursor_pos=None

		old_time=get_time()
		time.sleep(0.001)
		scaled_surface_height=surface_size[1]*scale
		scaled_visible_y_amount=min(max(scaled_surface_height+real_off[1],0),scaled_surface_height)
		scaled_visible_y_start=scaled_surface_height-scaled_visible_y_amount
		scaled_visible_y_end=max(min(screen.get_size()[1]-real_off[1],scaled_surface_height),0)

		real_visible_y_start=scaled_visible_y_start/scale
		real_visible_y_end=scaled_visible_y_end/scale

		print(str(real_off[1])+'\t'+str(real_visible_y_start)+'\t'+str(real_visible_y_end))
