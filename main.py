import math
import cairo


# Constants #

tau = 2 * math.pi

# World coordinates.
# H is the height of an equilateral triangle with side 1.
H = math.sqrt(3) / 2
SIZE_X = 2 * H
SIZE_Y = 3

# Screen coordinates.
SCALE = 512
# SCALE = 350
LINE_WIDTH = 0.108
# WIDTH, HEIGHT = (SCALE * SIZE_X, SCALE * SIZE_Y)
WIDTH, HEIGHT = 2560, 1440

# ORIGIN = (H, 1)
ORIGIN = (WIDTH / 2 / SCALE, HEIGHT / 2 / SCALE)
BASIS_U = (2*H, 0)
BASIS_V = (H, 3/2)


# How many layers to recurse.
DEPTH = 7

# Colors.

def html_to_rgb(color):
    b = (color & 0x0000ff) / 255
    g = ((color & 0x00ff00) >> 8) / 255
    r = ((color & 0xff0000) >> 16) / 255
    return (r, g, b)


BG_COLOR = html_to_rgb(0x10000D)
FG_COLOR = html_to_rgb(0x00AEBA)
FG_ALPHA = 0.014
FG_ALPHA_STEP = 0.003


def main():
    # Create cairo surface.
    # surface = cairo.SVGSurface('output.svg', WIDTH, HEIGHT)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(WIDTH), int(HEIGHT))

    cr = cairo.Context(surface)

    # Set a view box.
    cr.scale(SCALE, SCALE)

    # Draw.

    # Fill background color.
    cr.set_source_rgb(*BG_COLOR)
    cr.rectangle(0, 0, WIDTH / SCALE, HEIGHT / SCALE)
    cr.fill()

    # Initialize line drawing.
    cr.set_line_width(LINE_WIDTH)
    cr.set_line_cap(cairo.LineCap.ROUND)

    # Draw hexagons.
    size = 1
    for d in range(DEPTH):
        cr.set_line_width(size * LINE_WIDTH)
        cr.set_source_rgba(*FG_COLOR, FG_ALPHA + d * FG_ALPHA_STEP)
        hexagon_grid(cr, size)
        size /= 2

    # surface.finish()
    surface.write_to_png('output.png')


def hexagon_grid(cr, r):
    hexagon(cr, ORIGIN, r)

    n = int(1 / r)
    indices = list(range(-5*n, 5*n + 1))

    for u in indices:
        for v in indices:
            center = vadd(
                vadd(ORIGIN,
                     vmul(r * u, BASIS_U)),
                vmul(r * v, BASIS_V)
            )

            # Don't draw hexagons out of bounds.
            # cx, cy = center
            # if (
            #     cx < 0 - r or
            #     cx > SIZE_X + r or
            #     cy < 0 - r or
            #     cy > SIZE_Y + r
            # ):
            #     continue

            hexagon(cr, center, r)


def hexagon(cr, p, r):
    x, y = p
    cr.move_to(x, y - r)
    cr.rel_line_to(-r*H, r/2)
    cr.rel_line_to(0, r)
    cr.rel_line_to(r*H, r/2)
    cr.rel_line_to(r*H, -r/2)
    cr.rel_line_to(0, -r)
    cr.close_path()
    cr.stroke()


def dot(cr, p):
    cr.save()
    cr.set_source_rgb(0.85, 0.0, 0.0)
    cr.arc(*p, 0.02, 0, tau)
    cr.fill()
    cr.restore()


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def vmul(c, v):
    return (c * v[0], c * v[1])


def vneg(v):
    return (-v[0], -v[1])


if __name__ == '__main__':
    main()

