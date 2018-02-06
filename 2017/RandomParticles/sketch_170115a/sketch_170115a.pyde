import os

SOURCE_PATH = '/Users/Geeprox/Desktop/AnnualMeeting/RandomParticles/sketch_170115a/src/'
PARTICAL_COUNT = 5000
CURRENT_PARTICAL_COUNT = 1
IS_FREE = False
WINDOW_SIZE = (600, 600)

VELOCITY_RANGE = (6.0, 12.0)
PARTICLE_ERASING = 0.1
DIAMETER_ERASING = 0.08

files = []
particals = []
index = 0
images_count = 0
enable_sharpshooter = False

SHARPSHOOTER = {
    '0': '0.jpg',
    '1': '1.jpg',
    '2': '2.jpg',
    '3': '3.jpg',
    '4': '4.jpg',
    '5': '5.jpg',
    '6': '6.jpg',
    '7': '7.jpg',
    '8': '8.jpg',
    '9': '9.jpg',
    'a': '10.jpg',
    'b': '11.jpg',
    'c': '12.jpg',
    'd': '13.jpg',
    'e': '14.jpg',
    'f': '15.jpg',
    'g': '16.jpg',
    'h': '17.jpg',
    'i': '18.jpg',
    'j': '19.jpg',
    'k': '20.jpg',
    'l': '21.jpg',
    'm': '22.jpg',
    'n': '23.jpg',
    'o': '24.jpg',
    'p': '25.jpg',
    'q': '26.jpg',
    'r': '27.jpg',
    's': '28.jpg',
    't': '29.jpg',
    'u': '30.jpg',
    'v': '31.jpg',
    'w': '32.jpg',
    'x': '33.jpg',
    'y': '34.jpg',
    'z': '35.jpg',
}


class Partical():
    def __init__(self, position, diameter=[]):
        self.velocity = random(*VELOCITY_RANGE)
        self.velocity_theta = random(0.0, TWO_PI)
        self.current_diameter = diameter[index]
        self.diameter = diameter

        self.position = position
        self.destination = position

    def check_rebound(self, x, y):
        # For x
        if x < 0:
            self.velocity_theta = PI - self.velocity_theta
            x = 0 - x
        elif x > width:
            self.velocity_theta = PI - self.velocity_theta
            x = 2 * width - x
        # For y
        if y < 0:
            self.velocity_theta = 2 * PI - self.velocity_theta
            y = 0 - y
        elif y > height:
            self.velocity_theta = 2 * PI - self.velocity_theta
            y = 2 * height - y

        return x, y

    def update(self):
        if IS_FREE:
            prev_x, prev_y = self.position
            x = prev_x + cos(self.velocity_theta) * float(self.velocity)
            y = prev_y + sin(self.velocity_theta) * float(self.velocity)
            x, y = self.check_rebound(x, y)

            self.position = (x, y)
            d = self.diameter[index]
        else:
            prev_x, prev_y = self.position
            des_x, des_y = self.destination

            x = prev_x + (des_x - prev_x) * PARTICLE_ERASING
            y = prev_y + (des_y - prev_y) * PARTICLE_ERASING
            x, y = self.check_rebound(x, y)
            self.position = (x, y)

            prev_d = self.current_diameter
            target_d = self.diameter[index]
            d = prev_d + (target_d - prev_d) * DIAMETER_ERASING
            self.current_diameter = d

        fill(0)
        ellipse(x, y, d, d)


def setup():
    fullScreen()
    # size(*WINDOW_SIZE)

    # frameRate(30)
    # noCursor()

    phi = (sqrt(5)+1)/2 - 1
    golden_angle = phi * TWO_PI

    lg_rad = height * 0.45
    lg_area = sq(lg_rad) * PI

    sm_area = lg_area / PARTICAL_COUNT
    sm_rad = sqrt( sm_area / PI )

    fudge = 0.65
    adj_sm_diameter = sm_rad * 2 * fudge

    cx = width / 2
    cy = height / 2

    global files, images_count, index
    files = [filename for filename in os.listdir(SOURCE_PATH) if os.path.isfile(os.path.join(SOURCE_PATH, filename)) and not filename.startswith('.')]
    images_count = len(files)
    index = files.index('59.jpg')

    images = []
    for filename in files:
        file_path = os.path.join(SOURCE_PATH, filename)
        img = loadImage(file_path)
        if img:
            img.resize(height, height)
            img.filter(GRAY)
            images.append(img)

    for i in range(PARTICAL_COUNT):
        i += 1
        angle = i * golden_angle
        cum_area = i * sm_area
        spiral_rad = sqrt( cum_area / PI )
        x = cx + cos(angle) * spiral_rad
        y = cy + sin(angle) * spiral_rad

        diameter = []
        for i, img in enumerate(images):
            diameter.append(adj_sm_diameter * min(1.0, 1.45 - red(img.get(int(x-cx+cy), int(y))) / 255))

        partical = Partical((x, y), diameter)
        particals.append(partical)


def keyPressed():
    global enable_sharpshooter, IS_FREE, index
    if key == ENTER:
        if IS_FREE:
            index = int(random(images_count))

        IS_FREE = not IS_FREE
    elif key == ' ':
        for partical in particals:
            x, y = partical.destination
            partical.destination = (width-x, y)
    # Command pressed
    elif key == 65535:
        enable_sharpshooter = True
    else:

        if enable_sharpshooter and IS_FREE:
            if key in SHARPSHOOTER:
                filename = SHARPSHOOTER[key]
                index = files.index(filename)
                enable_sharpshooter = False
                IS_FREE = not IS_FREE


def draw():
    clear()
    smooth()
    background(255)

    fill(0)
    noStroke()

    global CURRENT_PARTICAL_COUNT
    if CURRENT_PARTICAL_COUNT < PARTICAL_COUNT:
        CURRENT_PARTICAL_COUNT += 50

    n = int(CURRENT_PARTICAL_COUNT)

    for i in range(min(n, PARTICAL_COUNT)):
        particals[i].update()

    # for partical in particals:
    #     partical.update()
