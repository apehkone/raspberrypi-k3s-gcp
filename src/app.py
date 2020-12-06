from sense_hat import SenseHat

s = SenseHat()
s.low_light = True

green = (0, 150, 57)
dark_green = (0, 255, 0)
nothing = (0, 0, 0)


def nortal():
    G = green
    DG = dark_green
    O = nothing
    logo = [
        DG, G, O, O, O, G, DG, G,
        DG, G, DG, O, O, G, DG, G,
        DG, G, DG, G, O, G, DG, G,
        DG, G, DG, G, DG, G, DG, G,
        DG, G, DG, G, DG, G, DG, G,
        DG, G, DG, O, DG, G, DG, G,
        DG, G, DG, O, O, G, DG, G,
        DG, G, DG, O, O, O, DG, G,
    ]
    return logo


while True:
    s.set_pixels(nortal())
