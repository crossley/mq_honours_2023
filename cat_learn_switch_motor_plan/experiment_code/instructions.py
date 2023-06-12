from psychopy import visual, event


def draw_screen_1(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['right'])

    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_2(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_3(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_4(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_5(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['d', 'f', 'j', 'k'])

    if k[0] == 'f':
        kk = 1
    if k[0] == 'j':
        kk = 1

    return (kk)


def draw_screen_6(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_7(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['d', 'f', 'j', 'k'])

    if k[0] == 'f':
        kk = 1
    if k[0] == 'j':
        kk = 1

    return (kk)


def draw_screen_8(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_9(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_10(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_11(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_12(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_13(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def draw_screen_14(win, s, im):

    im.draw()
    win.flip()

    k = event.waitKeys(keyList=['left', 'right'])

    if k[0] == 'left':
        kk = -1
    if k[0] == 'right':
        kk = 1

    return (kk)


def give_instructions(win):

    s = (1440 * .75, 900 * .75)
    instructions_dir = '/Users/mq20185996/Dropbox/catlearn_bin_delay/v2/instructions'
    im01 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 1.png',
                            pos=(0.0, 0.0))

    im02 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 2.png',
                            pos=(0.0, 0.0))

    im03 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 3.png',
                            pos=(0.0, 0.0))

    im04 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 4.png',
                            pos=(0.0, 0.0))

    im05 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 5.png',
                            pos=(0.0, 0.0))

    im06 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 6.png',
                            pos=(0.0, 0.0))

    im07 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 7.png',
                            pos=(0.0, 0.0))

    im08 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 8.png',
                            pos=(0.0, 0.0))

    im09 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 9.png',
                            pos=(0.0, 0.0))

    im10 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 10.png',
                            pos=(0.0, 0.0))

    im11 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 11.png',
                            pos=(0.0, 0.0))

    im12 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 12.png',
                            pos=(0.0, 0.0))

    im13 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 13.png',
                            pos=(0.0, 0.0))

    im14 = visual.ImageStim(win,
                            image=instructions_dir + '/Artboard 14.png',
                            pos=(0.0, 0.0))

    im = [
        im01, im02, im03, im04, im05, im06, im07, im08, im09, im10, im11, im12,
        im13, im14
    ]

    instructs = [
        draw_screen_1, draw_screen_2, draw_screen_3, draw_screen_4,
        draw_screen_5, draw_screen_6, draw_screen_7, draw_screen_8,
        draw_screen_9, draw_screen_10, draw_screen_11, draw_screen_12,
        draw_screen_13, draw_screen_14
    ]

    i = 0
    while i != len(instructs):
        k = instructs[i](win, s, im[i])
        i = i + k
