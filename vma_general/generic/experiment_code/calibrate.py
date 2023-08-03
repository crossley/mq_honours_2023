import numpy as np

state = 'pos_1'

# NOTE: collect Calibration Data
while False:

    resp = event.getKeys(keyList=['escape', 'space'])

    if state == 'pos_1':
        text_stim.text = 'move sensor to position 1'
        text_stim.draw()

        # press button to record sensor reading from position 1
        # x_raw =
        # y_raw =
        # x_physical =
        # y_physical =
        pass

    if state == 'pos_2':
        text_stim.text = 'move sensor to position 2'
        text_stim.draw()

        # press button to record sensor reading from position 2
        # x_raw =
        # y_raw =
        # x_physical =
        # y_physical =
        pass

    if 'escape' in resp:
        win.close()
        core.quit()

# NOTE: compute calibration parameters
# Calibration parameter for x: y = mx + c
# Calibration parameter for y: y = ny + d
