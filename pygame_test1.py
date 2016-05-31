import sys, os, pygame, math

from pygame import gfxdraw

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()

size = width, height = 640, 480
speed = [2,2]
black = 0,0,0
white = 255,255,255
red = 255,0,0
blue = 0,0,255
green = 0,255,0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()

def height_indicators():
  if pygame.font:
    font = pygame.font.Font(None, 36)
    
    height_text = font.render("height: "+str(round(height-ballrect.centery-ballrect.height/2)), 1, (128,128,128))
    textpos = height_text.get_rect(centery=45)
    screen.blit(height_text, textpos)

    highest_text = font.render("top_height: "+str(round(highest)), 1, (128,128,128))
    textpos = highest_text.get_rect()
    screen.blit(highest_text, textpos)


def verbose_indicators():
  if pygame.font:
    font = pygame.font.Font(None, 36)

    fuel_text = font.render("fuel: " + str(round(fuel,2)), 1, (128,128,128))
    textpos = fuel_text.get_rect(centerx=width/2)
    screen.blit(fuel_text, textpos)

    height_text = font.render("height: "+str(round(height-ballrect.centery-ballrect.height/2)), 1, (128,128,128))
    textpos = height_text.get_rect(centerx=width/2, centery=45)
    screen.blit(height_text, textpos)

    vy_text = font.render("delta-y: "+str(round(-speed[1])), 1, (128,128,128))
    textpos = vy_text.get_rect(centerx=width/2, centery=75)
    screen.blit(vy_text, textpos)

    highest_text = font.render("top_height: "+str(round(highest)), 1, (128,128,128))
    textpos = highest_text.get_rect()
    screen.blit(highest_text, textpos)

    fuel_rate_text = font.render("fuel recovery: "+str(round(fuel_rate,3)), 1, (128,128,128))
    textpos = fuel_rate_text.get_rect(centery=45)
    screen.blit(fuel_rate_text, textpos)

    status_text = font.render("status: "+status, 1, (128,128,128))
    textpos = status_text.get_rect(centery=75)
    screen.blit(status_text, textpos)

def fuel_gauge():
  #pie guage for fuel
  cx, cy, r = width-50, height-50, 25
  fuel_angle = int(fuel)*360/100
  fuel_color = max(0,int(-255*fuel/100+255)),min(255,int(255*fuel/100)),0

  p = [(cx, cy)]
  for n in range(0,fuel_angle):
    x = cx + int(r*math.sin(-math.pi+n*math.pi/180))
    y = cy+int(r*math.cos(-math.pi+n*math.pi/180))
    p.append((x, y))
  p.append((cx, cy))

  if len(p) > 2:
    #gfxdraw.aapolygon(screen, p, fuel_color)
    pygame.draw.polygon(screen, fuel_color, p)

def fuel_recovery_gauge():
  #pie guage for fuel
  cx, cy, r = 50, height-50, 25
  fuel_angle = int(fuel_rate*360)
  fuel_color = int(-255*fuel_rate+255),0,int(255*fuel_rate)

  p = [(cx, cy)]
  for n in range(0,fuel_angle):
    x = cx + int(r*math.sin(-math.pi+n*math.pi/180))
    y = cy+int(r*math.cos(-math.pi+n*math.pi/180))
    p.append((x, y))
  p.append((cx, cy))

  if len(p) > 2:
    pygame.draw.polygon(screen, fuel_color, p)

def sanitize_color(color):
  new_color=[]
  for val in color:
    if val>255:
      val=255
    elif val<0:
      val=0
    new_color.append(val)
  return new_color
	
	
def fuel_gauge_alt():
  #pie guage for fuel
  #draw circle aa
  #draw background color wedge out of it
  cx, cy, r = width-50, height-50, 25
  fuel_angle = 360 - int(fuel)*360/100
  fuel_color = int(-255*fuel/100+255),int(255*fuel/100),0
  fuel_color = sanitize_color(fuel_color)
  
  p = [(cx, cy)]
  for n in range(0,fuel_angle):
    x = cx + int(r*1.2*math.sin(-(-math.pi+n*math.pi/180)))
    y = cy+int(r*1.2*math.cos(-(-math.pi+n*math.pi/180)))
    p.append((x, y))
  p.append((cx, cy))

  gfxdraw.aacircle(screen, cx, cy, r, fuel_color)
  gfxdraw.filled_circle(screen, cx, cy, r, fuel_color)
  
  if len(p) > 2:
    gfxdraw.aapolygon(screen, p, black)
    pygame.draw.polygon(screen, black, p)
	
def fuel_recovery_gauge_alt():
#pie guage for fuel recovery
  #draw circle aa
  #draw background color wedge out of it
  #pie guage for fuel
  cx, cy, r = 50, height-50, 25  
  fuel_angle = 360 - int(fuel_rate*360)
  fuel_color = int(-255*fuel_rate+255),0,int(255*fuel_rate)
  fuel_color = sanitize_color(fuel_color)
  
  p = [(cx, cy)]
  for n in range(0,fuel_angle):
    x = cx + int(r*1.2*math.sin(-(-math.pi+n*math.pi/180)))
    y = cy+int(r*1.2*math.cos(-(-math.pi+n*math.pi/180)))
    p.append((x, y))
  p.append((cx, cy))

  gfxdraw.aacircle(screen, cx, cy, r, fuel_color)
  gfxdraw.filled_circle(screen, cx, cy, r, fuel_color)
  
  if len(p) > 2:
    gfxdraw.aapolygon(screen, p, black)
    pygame.draw.polygon(screen, black, p)

    
fuel = 100
fuel_rate = 1.
highest=0

def velocity_indicator():
  cx, cy = width/2, height-50
  max_speed = 100
  max_r = 25

  p = [(cx-max_r*1.5,cy),(cx+max_r*1.5,cy)]
  y = cy + speed[1]/100 * 25
  if y>cy:
    y=min(y,cy+max_r)
  elif y<cy:
    y=max(y,cy-max_r)
  p.append((cx,y))

  if len(p) > 2:
    gfxdraw.aapolygon(screen, p, white)
    pygame.draw.polygon(screen, white, p)


while 1:

  ticks_start = pygame.time.get_ticks()

  status = "nominal"
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  fill = black

  keys = pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:
    if fuel>0:
      speed[1]-=.4
      fuel-=1
      fuel_rate-=.001
      status = "firing engine"
    elif fuel<=0:
      fuel=0
      status = "out of fuel"
      if fuel_rate>0:
        fuel_rate-=.01
      elif fuel_rate<0:
        fuel_rate=0
  elif fuel<100:
    fuel+=fuel_rate
  elif fuel >100:
    fuel=100
  if fuel_rate == 0:
    status = "out of fuel"
    
  if keys[pygame.K_ESCAPE]:
    sys.exit()

  ballrect = ballrect.move(speed)
  speed[1]+=.5
  if ballrect.left < 0 or ballrect.right > width:
    speed[0] = -speed[0]
  if ballrect.bottom > height:
    speed[1]*=.9
    speed[1] = -speed[1]

  if height-ballrect.centery-ballrect.height/2 < 0:
    ballrect.centery = height-ballrect.height/2 

  screen.fill(fill)

  if highest<height-ballrect.centery-ballrect.height/2:
    highest = height-ballrect.centery-ballrect.height/2

  #verbose_indicators()
  height_indicators()
  fuel_gauge_alt()
  fuel_recovery_gauge_alt()
  velocity_indicator()

  screen.blit(ball, ballrect)
  pygame.display.flip()
  
  ticks_end=pygame.time.get_ticks()
  wait=(1000/60)-(ticks_end-ticks_start)
  pygame.time.wait(wait)
