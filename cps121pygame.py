import os, time
import threading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "yes"
import pygame as pg

black   = (  0,  0,  0)
red     = (255,  0,  0)
green   = (  0,255,  0)
blue    = (  0,  0,255)
cyan    = (  0,255,255)
magenta = (255,  0,255)
yellow  = (255,255,  0)
white   = (255,255,255)

class EventMonitor(threading.Thread):
    """Thread class to handle window close event"""

    running = False

    def __init__(self, daemon=True):
        """Instantiate daemon thread"""
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        """Polls pygame event queue and handles window close events"""
        self.running = True
        while self.running:
            time.sleep(0.01)
            if not pg.display.get_init():
                pg.display.init()
            for event in pg.event.get():
                if event.type == 32787: # WindowClose event
                    # Want window to disappear but shouldn't call pg.quit()
                    pg.display.set_mode((0,0), flags=pg.HIDDEN)
                    self.running = False

class Picture:
    monitor = None
    window = None
    image = None
    size = None
    title = ''
    magnification = 1

    def __init__(self, *args, **kwargs):
        size = (100, 100)
        if len(args) == 0:
            # no parameters, make screen with default size and color
            num_bytes = 3 * size[0] * size[1]
            self.size = size
            self.image = pg.image.frombytes(bytes([0]*num_bytes), size, 'RGB')
            self.image.fill(white)
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
        elif len(args) == 2 and \
            isinstance(args[0], int) and isinstance(args[1], int):
            # two integer parameters - assume these are width and height
            w, h = int(args[0]), int(args[1])
            num_bytes = 3 * w * h
            self.size = (w, h)
            self.image = pg.image.frombytes(bytes([0]*num_bytes), \
                                            self.size, 'RGB')
            self.image.fill(white)
        else:
            print("Unable to create image")

    def get_magnification(self):
        return self.magnification
    
    def set_magnification(self, magnification):
        self.magnification = magnification

    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
    def set_color(self, x, y, c):
        self.image.set_at((x, y), c)

    def get_color(self, x, y):
        return self.image.get_at((x, y))[0:3]

    def get_red(self, x, y):
        return self.image.get_at((x,y))[0]

    def get_gree(self, x, y):
        return self.image.get_at((x,y))[1]

    def get_blue(self, x, y):
        return self.image.get_at((x,y))[2]

    def set_red(self, x, y, value):
        c = self.image.get_at((x,y))[0:3]
        self.image.set_at((x, y), (value, c[1], c[2]))

    def set_green(self, x, y, value):
        c = self.image.get_at((x,y))[0:3]
        self.image.set_at((x, y), (c[0], value, c[2]))

    def set_blue(self, x, y, value):
        c = self.image.get_at((x,y))[0:3]
        self.image.set_at((x, y), (c[0], c[1], value))

    def copy(self):
        """Returns a new copy of an image"""
        return Picture(self)
    
    def copyInto(self, pic, x, y):
        """Copies pic into the image with upper-left at (x,y)"""
        self.image.blit(pic.image, (x, y))
        
    def magnify(self):
        """Returns magnified image and image size
        
        Returns the scaled image and the true size (in pixels)
        of the image.
        """
        orig_size = self.image.get_size()
        mag_size = (orig_size[0] * self.magnification,
                    orig_size[1] * self.magnification)
        mag_image = pg.transform.scale(self.image, mag_size)
        return mag_image, mag_size

    def show(self, title=None):
        # start event monitor if it's not running
        if self.monitor is None or not self.monitor.running:
            self.monitor = EventMonitor()
            self.monitor.start()

        # get image and image size and create window
        mag_image, mag_size = self.magnify()
        self.window = pg.display.set_mode(mag_size, flags=pg.SHOWN)

        # display image
        self.window.blit(mag_image, (0, 0))
        if title is not None:
            self.title = title
        pg.display.set_caption(self.title)
        pg.display.update()
        pg.event.pump()

    def repaint(self, title=None):
        # start event monitor if it's not running
        if self.monitor is None or not self.monitor.running:
            self.monitor = EventMonitor()
            self.monitor.start()

        # get image and image size, and make it shown if previously hidden
        mag_image, mag_size = self.magnify()
        if not pg.display.get_active():
            pg.display.set_mode(mag_size, flags=pg.SHOWN)

        # update image
        self.window.blit(mag_image, (0, 0))
        if title is not None:
            self.title = title
            pg.display.set_caption(self.title)
        pg.display.update()
        pg.event.pump()
    
    def close(self):
        pg.quit()

if __name__ == "__main__":
    from random import randint

    # create and show a picture with randomly colored pixels
    w = 30
    h = 20
    gr = Picture(w, h)
    gr.set_magnification(15)
    print(gr.get_width(), gr.get_height())
    for y in range(h):
        for x in range(w):
            c = tuple(randint(0,255) for i in range(3))
            gr.set_color(x, y, c)
    gr.show('A Picture')
    input("press Enter to continue...")

    # change colors in the picture
    for y in range(h):
        for x in range(w):
            c = tuple(randint(0,255) for i in range(3))
            gr.set_color(x, y, c)
    gr.repaint('Modified Picture')
    input("press Enter to continue...")

    # make a copy and close original picture
    newPic = gr.copy()
    gr.close()
    input('press Enter to continue...')

    # reset magnification to 1 (actual size)
    newPic.set_magnification(1)
    newPic.show()
    input('press Enter to continue...')
    gr.close()

    # try loading an image from a file
    nico = Picture('nico.jpg')
    nico.show()
    input('press Enter to continue...')

    for x in range(100, 200):
        r = nico.get_red(x, 100)
        r = 255-r
        nico.set_red(x, 100, r)

    nico.set_magnification(2)
    nico.repaint()
    input('press Enter to continue...')
    
