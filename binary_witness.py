#!/usr/bin/env python2
import mmap
import os
import pygame
import sys
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

def map_byte(mm,ind):
	return (ord(mm[ind]),ord(mm[ind]),ord(mm[ind]))

if __name__=='__main__':
	try:
		if len(sys.argv)<=1:
			print('usage: '+sys.argv[0]+' FILE')
			exit(1)

		file_path=sys.argv[1]

		if not os.path.isfile(file_path):
			print('"'+file_path+'" is not a file')
			exit(1)

		screen=init_screen((600,600))
		surface_size=[1000,100]
		surface=pygame.Surface(surface_size)
		surface.fill((0,0,0))
		pygame.display.set_caption('Binary Witness - '+sys.argv[1])

		old_mod_time=0
		last_y_start=None
		last_y_end=None

		keys={}
		for ii in range(0,300):
			keys[ii]=False

		old_time=get_time()
		offset=[(screen.get_size()[0]-surface_size[0])/2,(screen.get_size()[1]-surface_size[1])/2]
		scale=1
		min_scale=0.2
		max_scale=10
		pos_change=-800
		scale_change=0.5
		old_cursor_pos=None

		while True:
			new_time=get_time()
			dt=(new_time-old_time)

			cursor=pygame.mouse.get_pos()
			cursor=[cursor[0]-screen.get_size()[0]/2,cursor[1]-screen.get_size()[1]/2]


			def zoom_out():
				global dt
				global min_scale
				global offset
				global scale
				global scale_change
				global surface_size
				real_change=surface_size[1]*scale_change*dt
				if scale-real_change<min_scale:
					real_change=scale-min_scale
				scale-=real_change
				#offset[0]+=(cursor[0]+surface_size[0]/2)*real_change
				#offset[1]+=(cursor[1]+surface_size[1]/2)*real_change
				offset[0]+=(surface_size[0]/2)*real_change
				offset[1]+=(surface_size[1]/2)*real_change

			def zoom_in():
				global dt
				global max_scale
				global offset
				global scale
				global scale_change
				global surface_size
				real_change=surface_size[1]*scale_change*dt
				if scale+real_change>max_scale:
					real_change=max_scale-scale
				scale+=real_change
				#offset[0]-=(cursor[0]+surface_size[0]/2)*real_change
				#offset[1]-=(cursor[1]+surface_size[1]/2)*real_change
				offset[0]-=(surface_size[0]/2)*real_change
				offset[1]-=(surface_size[1]/2)*real_change

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					quit(0)
				elif event.type==pygame.KEYDOWN:
					keys[event.key]=True
				elif event.type==pygame.KEYUP:
					keys[event.key]=False
				elif event.type==pygame.VIDEORESIZE:
					screen=init_screen((event.w,event.h))
					last_y_end+=1
				elif event.type==pygame.MOUSEBUTTONDOWN:
					if event.button==1 and not old_cursor_pos:
						old_cursor_pos=cursor
					elif event.button==4:
						zoom_out()
					elif event.button==5:
						zoom_in()
				elif event.type==pygame.MOUSEBUTTONUP:
					if event.button==1 and old_cursor_pos:
						offset[0]+=cursor[0]-old_cursor_pos[0]
						offset[1]+=cursor[1]-old_cursor_pos[1]
						old_cursor_pos=None

			screen.fill((100,100,80))

			real_off=(offset[0],offset[1])
			if old_cursor_pos:
				real_off=(offset[0]+cursor[0]-old_cursor_pos[0],offset[1]+cursor[1]-old_cursor_pos[1])

			if keys[pygame.K_ESCAPE]:
				quit(0)
			if keys[pygame.K_MINUS]:
				zoom_out()
			if keys[pygame.K_EQUALS]:
				zoom_in()
			if keys[pygame.K_a]:
				offset[0]-=pos_change*scale*dt
			if keys[pygame.K_a]:
				offset[0]-=pos_change*scale*dt
			if keys[pygame.K_d]:
				offset[0]+=pos_change*scale*dt
			if keys[pygame.K_w]:
				offset[1]-=pos_change*scale*dt
			if keys[pygame.K_s]:
				offset[1]+=pos_change*scale*dt
			if keys[ord('0')]:
				offset=[(screen.get_size()[0]-surface_size[0])/2,0]
				scale=1
				old_cursor_pos=None

			scaled_surface_height=surface_size[1]*scale
			scaled_visible_y_amount=min(max(scaled_surface_height+real_off[1],0),scaled_surface_height)
			scaled_visible_y_start=scaled_surface_height-scaled_visible_y_amount
			scaled_visible_y_end=max(min(screen.get_size()[1]-real_off[1],scaled_surface_height),0)

			real_visible_y_start=scaled_visible_y_start/scale
			real_visible_y_end=scaled_visible_y_end/scale

			new_mod_time=os.stat(file_path).st_mtime
			if new_mod_time!=old_mod_time or real_visible_y_start!=last_y_start or real_visible_y_end!=last_y_end:
				try:
					with open(file_path,'r+b') as f:
						old_mod_time=new_mod_time
						last_y_start=real_visible_y_start
						last_y_end=real_visible_y_end

						mm=mmap.mmap(f.fileno(),0)
						new_surface_height=len(mm)/surface_size[0]+1

						if surface_size[1]!=new_surface_height:
							surface_size[1]=new_surface_height
							surface=pygame.Surface(surface_size)

						for yy in range(int(real_visible_y_start),int(real_visible_y_end)+1):
							for xx in range(surface_size[0]):
								ind=yy*surface_size[0]+xx
								if ind>=len(mm):
									break
								surface.set_at((xx,yy),map_byte(mm,ind))

					screen.blit(pygame.transform.rotozoom(surface,0,scale),real_off)
					pygame.display.flip()

					pygame.display.update()
				except ValueError:
					pass

			time.sleep(0.001)
			old_time=get_time()

	except KeyboardInterrupt:
		quit(0)
