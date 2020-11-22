import atexit
import math
import time
import board
import neopixel
import colorsys

from gradient import polylinear_gradient, bezier_gradient

DATA_OUT = board.D18
NUM_PIXELS = 60
BRIGHTNESS = 1
ORDER = neopixel.GRB

def hsv_to_rgb(hsv):
  '''converts an hsv tuple into rgb'''
  rgb = colorsys.hsv_to_rgb(hsv/360, 1.0, 1.0)

  return tuple(map(lambda float: int(255*float), rgb))

def set_all_hsv(pixels, hsv):
  '''sets all pixels on the led to a specified hsv value'''
  for i in range(NUM_PIXELS):
    pixels[i] = hsv_to_rgb(hsv)

def set_all_rgb(pixels, rgb):
  '''sets all pixels on the led to a specified rgb value'''
  for i in range(NUM_PIXELS):
    pixels[i] = rgb

def set_all_alternate(pixels, colors):
  '''sets all pixels on the led to a list of alternatating rgb values'''
  j = 0
  for i in range(NUM_PIXELS):
    pixels[i] = colors[j % len(colors)]
    j += 1

def rainbow(pixels):
  '''makes the led rainbowy'''
  while True:
    for i in range(360):
      set_all_hsv(pixels, i)
      pixels.show()
      time.sleep(0.5)

def shift_pixels(pixels):
  '''shifts all the colors on the led strip one down'''
  for i in range(NUM_PIXELS-1):
    pixels[i] = pixels[i+1]

def moving_rainbow(pixels, speed, width):
  '''makes the led strip rainbowy and makes it move down the led'''
  current_hue = 0
  hue_increment = 360/width

  endingSequence = False

  while True:
    shift_pixels(pixels)

    if not endingSequence:
      pixels[NUM_PIXELS-1] = hsv_to_rgb(current_hue)
      current_hue += hue_increment
    else:
      pixels[NUM_PIXELS-1] = [0, 0, 0]
      if pixels[0] == [0, 0, 0]:
        endingSequence = False

    pixels.show()

    if current_hue >= 360:
      current_hue %= 360
      endingSequence = True 
    
    time.sleep(1/speed)

def play_sequence(pixels, colors, speed):
  ''' Play list rgb colors at a specified speed'''
  for color in colors:
    set_all_rgb(pixels, color)
    pixels.show()
    time.sleep(1/speed)

def sunrise(pixels):
  '''plays a sunrise sequence on the led strip'''
  pixels.brightness = 1

  length = 1000
  duration = 0.5 # minutes

  # gradient = bezier_gradient(("#0400ff", "#7e0083", "#ff0000", "#ff5b00", "#ffa600", "#80c980", "#00ecff"), length)
  gradient = bezier_gradient(("#0400ff", "#7e0083", "#ff0000", "#ff5b00", "#ffa600"), length)

  # # blue sunrise sequence
  # set_all_rgb(pixels, (0, 0, 255))
  # pixels.show()

  # # brightness sequence
  # for i in range(300):
  #   pixels.brightness += 1/300
  #   pixels.show()
  #   time.sleep(0.05)
  
  for color in gradient:
    set_all_rgb(pixels, color)
    pixels.show()
    time.sleep(duration*60/length)


def clear_range(pixels, start, end):
  '''clears a range of pixels on the led strip'''
  for i in range(end-start):
    pixels[start + i] = (0, 0, 0)
  pixels.show()

def clear(pixels):
  '''clears all pixels on the led strip'''
  for i in range(NUM_PIXELS):
    pixels[i] = (0, 0, 0)
  pixels.show()

def fill(pixels, startPixel, endPixel, hue):
  '''fills all pixels within a range with a given hsv value'''
  for i in range(endPixel - startPixel):
    pixels[startPixel + i] = hsv_to_rgb(hue) 

def police(pixels, speed):
  '''plays a police light sequence'''
  switch = False
  while True:
    if switch:
      fill(pixels, 0, math.floor(NUM_PIXELS/2), 0)
      fill(pixels, math.floor(NUM_PIXELS/2) +1, NUM_PIXELS-1, 250)
      switch = False
    else:
      fill(pixels, 0, math.floor(NUM_PIXELS/2), 250)
      fill(pixels, math.floor(NUM_PIXELS/2) +1, NUM_PIXELS-1, 0)
      switch = True
    pixels.show()
    time.sleep(1/speed)

def main(args):
  pixels = neopixel.NeoPixel(
    DATA_OUT, NUM_PIXELS, brightness=BRIGHTNESS, pixel_order=ORDER, auto_write=False
  )

  def exit_handler():
    clear(pixels)

  atexit.register(exit_handler)
  
  # police(pixels,30)
  # moving_rainbow(pixels, 120, 250)
  sunrise(pixels)
  # rainbow(pixels)

  # set_all_alternate(pixels, [(244, 1, 1), (120, 120, 120)])

  
  return 0

if __name__ == '__main__':
  import sys

  main(sys.argv)
