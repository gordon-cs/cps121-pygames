import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "yes"
import pygame as pg

class Picture:

    window = None
    image = None
    size = None
    title = ''
    mag = 1

    def __init__(self, *args, **kwargs):
        default_size = (100, 100)
        default_color = (255, 255, 255)
        if len(args) == 0:
            # no parameters, make screen with default size and color
            num_bytes = 3 * default_size[0] * default_size[1]
            self.size = default_size
            self.image = pg.image.frombytes(bytes([0]*num_bytes), default_size, 'RGB')
            self.image.fill(default_color)
            #print(f'Init - no params')
        elif len(args) == 1:
            if isinstance(args[0], str):
                # one string parameter - assume it is a filename or path to a file
                self.image = pg.image.load(args[0])
                self.size = self.image.get_size()
                self.title = args[0]
                #print(f'Init - 1 param filename {args[0]}')
            elif isinstance(args[0], Picture):
                self.image = args[0].image.copy()
                self.size = args[0].size
                self.title = args[0].title
                self.mag = args[0].mag
                #print(f'Init - 1 param (Picture)')
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            # two integer parameters - assume these are width and height
            w, h = int(args[0]), int(args[1])
            num_bytes = 3 * w * h
            self.size = (w, h)
            self.image = pg.image.frombytes(bytes([0]*num_bytes), self.size, 'RGB')
            self.image.fill(default_color)
            #print(f'Init - 2 params: {self.image.get_width()}, {self.image.get_height()}')
        else:
            print("Unable to create image")

    def get_mag(self):
        return self.mag
    
    def set_mag(self, mag):
        self.mag = mag

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

    def get_green(self, x, y):
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
        return Picture(self)
    
    def copyInto(self, pic, x, y):
        self.image.blit(pic.image, (x, y))

    def magnify(self):
        orig_size = self.image.get_size()
        mag_size = (orig_size[0] * self.mag, orig_size[1] * self.mag)
        mag_image = pg.transform.scale(self.image, mag_size)
        return mag_image, mag_size
    
    def show(self, title=None):
        if title is not None:
            self.title = title
        mag_image, mag_size = self.magnify()
        self.window = pg.display.set_mode(mag_size)
        self.window.blit(mag_image, (0, 0))
        pg.display.set_caption(self.title)
        pg.display.update()

    def repaint(self, title=None):
        if title is not None:
            self.title = title
        mag_image, mag_size = self.magnify()
        self.window.blit(mag_image, (0, 0))
        pg.display.set_caption(self.title)
        pg.display.update()
    
    def close(self):
        pg.quit()

if __name__ == "__main__":
    from random import randint

    # create and show a picture with randomly colored pixels
    w = 30
    h = 20
    gr = Picture(w, h)
    gr.set_mag(15)
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
    newPic.set_mag(1)
    newPic.show()
    input('press Enter to continue...')
    gr.close()

    # try loading an image from a file
    nico = Picture('nico.jpg')
    nico.show()
    input('press Enter to continue...')

    nico.set_mag(2)
    nico.repaint()
    input('press Enter to continue...')
    
