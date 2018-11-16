import RPi.GPIO as GPIO

#
#  0 _ _ _ _ _ _ _ _ 64 - lengthX (Direction: True)
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#   |_|_|_|_|_|_|_|_|
#
#  64 - lengthY (Direction: True)

# rPi3 GPIO Pins
# 4, 5, 6, 7,

GPIO.setmode(GPIO.BOARD)

# Step motor pins for X and Y directions
step_motor_pin_x = 4
step_motor_pin_y = 5

# Direction pins for the X and Y motors
dir_pin_x = 6
dir_pin_y = 7

# End stop switches for min and maximum length of the X lead screws
end_stop_pin_min_x = 12
end_stop_pin_max_x = 13

# End stop switches for min and maximum length of the Y lead screws
end_stop_pin_min_y = 16
end_stop_pin_max_y = 17

# Step Motor setup for X and Y motors
GPIO.setup(step_motor_pin_x, GPIO.OUT)
GPIO.setup(step_motor_pin_y, GPIO.OUT)

# Direction pin setup for X and Y motors
GPIO.setup(dir_pin_x, GPIO.OUT)
GPIO.setup(dir_pin_y, GPIO.OUT)

# End stop pin setup for X
GPIO.setup(end_stop_pin_min_x, GPIO.IN)
GPIO.setup(end_stop_pin_max_x, GPIO.IN)

# End stop pin setup for Y
GPIO.setup(end_stop_pin_min_y, GPIO.IN)
GPIO.setup(end_stop_pin_max_y, GPIO.IN)

# How much the platform moves per step of the motor in the X and Y direction
distPerStepX = 0.5
distPerStepY = 0.5

# Length of the actual board in centimeters
lengthX = 64
lengthY = 64

# Length of half a square
half_length = 4

# Current X and Y location of the electromagnet
currLocationX = 0
currLocationY = 0

# Starting X and Y position of the electromagnet
starting_position_x = 0
starting_position_y = 0


# Moves the platform to the X, Y location by moving in one axis at a time
def go_to_location(x, y):
    go_x(x)
    go_y(y)
    return


# Move the platform in the X direction
def go_x(x):

    global currLocationX

    if x > currLocationX:
        direction = True
    elif x < currLocationX:
        direction = False
    else:
        return

    set_x_direction(direction)

    num_of_steps = abs(currLocationX - x) / distPerStepX

    num_of_steps = round(num_of_steps)

    for i in range(num_of_steps):
        GPIO.output(step_motor_pin_x, GPIO.HIGH)
        GPIO.output(step_motor_pin_x, GPIO.LOW)
        if direction:
            currLocationX += distPerStepX
        else:
            currLocationX -= distPerStepX

    return


# Move the platform in the Y direction
def go_y(y):

    global currLocationY

    if y > currLocationY:
        direction = True
    elif y < currLocationY:
        direction = False
    else:
        return

    set_y_direction(direction)

    num_of_steps = abs(currLocationY - y) / distPerStepY

    num_of_steps = round(num_of_steps)

    for i in range(num_of_steps):
        GPIO.output(step_motor_pin_y, GPIO.HIGH)
        GPIO.output(step_motor_pin_y, GPIO.LOW)
        if direction:
            currLocationY += distPerStepY
        else:
            currLocationY -= distPerStepY

    return


# Goes to the starting point in the X direction
def reset_x():

    set_x_direction(False)

    while GPIO.input(end_stop_pin_min_x):
        GPIO.output(step_motor_pin_x, GPIO.HIGH)
        GPIO.output(step_motor_pin_x, GPIO.LOW)
    return


# Goes to the starting point in the Y direction
def reset_y():

    set_y_direction(False)

    while GPIO.input(end_stop_pin_min_y):
        GPIO.output(step_motor_pin_y, GPIO.HIGH)
        GPIO.output(step_motor_pin_y, GPIO.LOW)
    return


# Go to the defined starting position (subset of the entire area available)
def go_to_starting_position():
    reset_x()
    reset_y()
    go_to_location(starting_position_x, starting_position_y)
    return


# Set direction for the X stepper
def set_x_direction(direction):

    if direction:
        GPIO.output(dir_pin_x, GPIO.HIGH)
    else:
        GPIO.output(dir_pin_x, GPIO.LOW)
    return


# Set direction for the Y stepper
def set_y_direction(direction):
    if direction:
        GPIO.output(dir_pin_y, GPIO.HIGH)
    else:
        GPIO.output(dir_pin_y, GPIO.LOW)
    return


# Move half right/ in between chess squares
def go_half_right():
    global currLocationX
    set_x_direction(True)

    num_of_steps = half_length / distPerStepY

    num_of_steps = round(num_of_steps)

    for i in range(num_of_steps):
        GPIO.output(step_motor_pin_x, GPIO.HIGH)
        GPIO.output(step_motor_pin_x, GPIO.LOW)
        currLocationX += distPerStepX

    return


# Move half left/ in between chess squares
def go_half_left():
    global currLocationX
    set_x_direction(False)

    num_of_steps = half_length / distPerStepY

    num_of_steps = round(num_of_steps)

    for i in range(num_of_steps):
        GPIO.output(step_motor_pin_x, GPIO.HIGH)
        GPIO.output(step_motor_pin_x, GPIO.LOW)
        currLocationX -= distPerStepX

    return


# Move half up/ in between chess squares
def go_half_up():
    global currLocationY
    set_y_direction(False)

    num_of_steps = half_length / distPerStepY

    num_of_steps = round(num_of_steps)

    for i in range(num_of_steps):
        GPIO.output(step_motor_pin_y, GPIO.HIGH)
        GPIO.output(step_motor_pin_y, GPIO.LOW)
        currLocationY -= distPerStepY

    return


# Move half down/ in between chess squares
def go_half_down():
    global currLocationY
    set_y_direction(True)

    num_of_steps = half_length / distPerStepY

    num_of_steps = round(num_of_steps)

    for i in range(num_of_steps):
        GPIO.output(step_motor_pin_y, GPIO.HIGH)
        GPIO.output(step_motor_pin_y, GPIO.LOW)
        currLocationY += distPerStepY

    return


