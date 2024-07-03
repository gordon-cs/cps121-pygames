import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "yes"
import pygame as pg

class autoUpdate():
  autoUpdateBool = False

  def __init__(self):
    autoUpdateBool = False

  def getAutoUpdate(self):
    return self.autoUpdateBool
  
  def setAutoUpdate(self, status):
     self.autoUpdateBool = status

class Picture:
  window = None
  image = None
  size = None
  title = ''
  magnification = 1
  autoUpdate = autoUpdate()

  def __init__(self, *args, **kwargs):
      size = (100, 100)
      if len(args) == 0:
          # no parameters, make screen with default size and color
          num_bytes = 3 * size[0] * size[1]
          self.size = size
          self.image = pg.image.frombytes(bytes([0]*num_bytes), size, 'RGB')
          self.image.fill("white")
      elif len(args) == 1:
          if isinstance(args[0], str):
              # one string parameter - filename or path to a file
              self.image = pg.image.load(args[0])
              self.size = self.image.get_size()
              self.title = args[0]
          elif isinstance(args[0], Picture):
              # one image parameter - pre-existing image to clone
              self.image = args[0].image.copy()
              self.size = args[0].size
              self.title = args[0].title
              self.magnification = args[0].magnification
      elif (len(args) == 2 and \
          isinstance(args[0], int) and isinstance(args[1], int)) or \
            len(args) == 3:
          # two integer parameters - assume these are width and height
          # third parameter is a color
          c = pg.Color(255, 255, 255) if len(args) == 2 else args[2]
          w, h = int(args[0]), int(args[1])
          num_bytes = 3 * w * h
          self.size = (w, h)
          self.image = pg.image.frombytes(bytes([0]*num_bytes), \
                                          self.size, 'RGB')
          self.image.fill(c)
      else:
          print("Unable to create image")
  
  def show(self, title=None):
    if title is not None:
      self.title = title
    mag_image, mag_size = self.magnify()
    self.window = pg.display.set_mode(mag_size)
    self.window.blit(mag_image, (0, 0))
    pg.display.set_caption(self.title)
    pg.display.update()
    pg.event.pump()

  def magnify(self, title=None):
    orig_size = self.image.get_size()
    mag_size = (orig_size[0] * self.magnification,
                orig_size[1] * self.magnification)
    mag_image = pg.transform.scale(self.image, mag_size)
    return mag_image, mag_size

  def repaint(self):
    self.show()
    pg.display.flip()
    pg.event.pump()
  
  def copyInto(self, dest, x, y):
    img = self.image
    dest.image.blit(img, (x, y))
    if self.autoUpdate.autoUpdateBool:
      pg.display.update()

  def get_magnification(self):
      return self.magnification
  
  def set_magnification(self, magnification):
      self.magnification = magnification
  
  def getWidth(self):
    return self.image.get_width()
    
  def getHeight(self):
      return self.image.get_height()
  
  # def getPixel(self, x, y):
  #   px = Pixel(self.image, x, y)
  #   return px
  
  def getColor(self, x, y):
     return pg.Color(self.image.get_at((x, y))[0:3])
  
  def setColor(self, x, y, color):
     self.image.set_at((x,y), color)
     if self.autoUpdate.autoUpdateBool:
      pg.display.update()

  def getRed(self, x, y):
    c = pg.Color(self.getColor(x, y))
    return c.r
  
  def getGreen(self, x, y):
    c = pg.Color(self.getColor(x, y))
    return c.g
  
  def getBlue(self, x, y):
    c = pg.Color(self.getColor(x, y))
    return c.b
  
  def setRed(self, red):
    r = red
    g = self.getGreen()
    b = self.getBlue()
    self.setColor((r, g, b))
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def setGreen(self, green):
    r = self.getRed()
    g = green
    b = self.getBlue()
    self.setColor((r, g, b))
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def setBlue(self, blue):
    r = self.getRed()
    g = self.getGreen()
    b = blue
    self.setColor((r, g, b))
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()
  
  # def getPixels(self):
  #   pxarray = pg.PixelArray(self.image)
  #   return pxarray
  
  def addLine(self, acolor, x1, y1, x2, y2, width=1):
    img = self.image
    pg.draw.line(img, acolor, (x1, y1), (x2, y2), width)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addRectFilled(self, width, height, x, y, acolor="red"):
    """
    Draws a filled rectangle onto a given surface

    Args:
      width (int) - width of the rectangle (in pixels)
      height (int) - height of the rectangle (in pixels)
      x (int) - the x position of the top left corner of the rectangle
      y (int) - the y position of the top left corner of the rectangle
      acolor (Color, int, str, tuple) - the color of the rectangle

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.rect(img, acolor, newRect)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addRect(self, width, height, x, y, acolor="red", linew=1):
    """
    Draws a rectangle onto a given surface
    
    Args:
      width (int) - width of the rectangle (in pixels)
      height (int) - height of the rectangle (in pixels)
      x (int) - the x position of the top left corner of the rectangle
      y (int) - the y position of the top left corner of the rectangle
      acolor (Color, int, str, tuple) - the color of the rectangle
      linew (int) - width of the outline of the rectangle

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.rect(img, acolor, newRect, linew)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addOvalFilled(self, width, height, x, y, acolor="red"):
    """
    Draws a filled oval onto a given surface

    Args:
      width (int) - width of the oval (in pixels)
      height (int) - height of the oval (in pixels)
      x (int) - the x position of the oval
      y (int) - the y position of the oval
      acolor (Color, int, str, tuple) - the color of the oval

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.ellipse(img, acolor, newRect)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addOval(self, width, height, x, y, acolor="red", linew=1):
    """
    Draws an oval onto a given surface

    Args:
      width (int) - width of the oval (in pixels)
      height (int) - height of the oval (in pixels)
      x (int) - the x position of the oval
      y (int) - the y position of the oval
      acolor (Color, int, str, tuple) - the color of the oval
      linew (int) - width of the outline of the oval

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.ellipse(img, acolor, newRect, linew)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()
     
# class Pixel:

#   def __init__(self, image=None, x=None, y=None):
#     self.image = pg.Surface.convert(image)
#     self.array = pg.PixelArray(image)
#     self.x = x
#     self.y = y
#     self.color = self.image.unmap_rgb(self.array[x,y])
  
#   def getX(self):
#     return self.x
  
#   def getY(self):
#     return self.y
  
#   def getColor(self):
#     return self.color
  
#   def setColor(self, new_color):
#     self.color = new_color
#     self.array.close()
#     pg.display.flip()
  
#   def getRed(self):
#     c = pg.Color(self.getColor())
#     return c.r
  
#   def setRed(self, red):
#     r = red
#     g = self.getGreen()
#     b = self.getBlue()
#     self.setColor((r, g, b))
#     pg.display.flip()
  
#   def getGreen(self):
#     c = pg.Color(self.getColor())
#     return c.g
  
#   def setGreen(self, green):
#     r = self.getRed()
#     g = green
#     b = self.getBlue()
#     self.setColor((r, g, b))
#     pg.display.flip()
  
#   def getBlue(self):
#     c = pg.Color(self.getColor())
#     return c.b

#   def setBlue(self, blue):
#     r = self.getRed()
#     g = self.getGreen()
#     b = blue
#     self.setColor((r, g, b))
#     pg.display.flip()
  
  # def getPixels(self):
  #   pixels = list()
  #   for x in range(self.image.getWidth()):
  #     for y in range(self.image.getHeight()):
  #       pixels.append(Pixel(self.image, x, y))
  #   return pixels

  # def getPixel(self, x, y):
  #   px = Pixel(self.image, x, y)
  #   return px
     

  


# if __name__ == "__main__":
#   canvas = makeEmptyCanvas(200, 200, "light green")
#   addOvalFilled(canvas, 20, 30, 0, 0, "blue")
#   input("Press Enter")

