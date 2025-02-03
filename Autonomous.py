#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT2, 1.0, False)
right_drive_smart = Motor(Ports.PORT1, 1.0, True)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
Choochoo = Motor(Ports.PORT6, False)
Flywheel = Motor(Ports.PORT4, False)
Tensioner = Motor(Ports.PORT3, False)
controller = Controller()
LeftDistance = Distance(Ports.PORT7)
RightDistance = Distance(Ports.PORT11)
CataDistance = Distance(Ports.PORT5)



# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
# Initialize random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axisA + axisC
            # right = axisA - axisC
            drivetrain_left_side_speed = controller.axisA.position() + controller.axisC.position()
            drivetrain_right_side_speed = controller.axisA.position() - controller.axisC.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

#endregion VEXcode Generated Robot Configuration

vexcode_brain_precision = 0
vexcode_console_precision = 0
Goal = 0
Direction = 0
ExtraTension = 0

def when_started1():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    Low = 2.7
    High = 5
    Tension = 5
    Direction = FORWARD
    Balls = 0
    BallDistance = LeftDistance.object_distance(MM) + RightDistance.object_distance(MM)
    BallDistanceGoal = BallDistance/2 - 170
    Choochoo.spin_for(FORWARD,0.1,DEGREES,wait=False)
    while not controller.buttonEUp.pressing():
        pass
    while True:
        # Sets the tension for the selected goal
        if (Goal == "High"):
            Tension = High + ExtraTension
        else:
            Tension = Low + ExtraTension
        Tensioner.set_velocity(abs(Tension-Tensioner.position(TURNS))*300, PERCENT)
        Tensioner.spin_to_position(Tension, TURNS, wait=False)
    
        # Makes the screen green if there is a ball in the middle of the flywheel
        BallDistance = LeftDistance.object_distance(MM)+RightDistance.object_distance(MM)
        if (BallDistance < BallDistanceGoal):
            brain.screen.set_fill_color(Color.GREEN)
        else:
            brain.screen.set_fill_color(Color.BLACK)
        brain.screen.draw_rectangle(100,0,70,70)
    
        # Makes the screen green if there is a ball in the middle of the flywheel
        BallDistance = LeftDistance.object_distance(MM)+RightDistance.object_distance(MM)
        if (Goal == "High"):
            brain.screen.set_fill_color(Color.GREEN)
        else:
            brain.screen.set_fill_color(Color.WHITE)
        brain.screen.draw_rectangle(0,0,70,70)
    
        # 0 balls means none in the cata, 1 means 1 in the cata and still picking up a
        # second ball. 2 means 2 balls, with 1 in the middle of the flywheel.
        if (CataDistance.object_distance(MM)>100):
            Balls = 0
        elif (CataDistance.object_distance(MM)<100 and BallDistance > BallDistanceGoal):
            Balls = 1
        else:
            Balls = 2
            if (not controller.buttonFUp.pressing()):
                Flywheel.set_velocity(drivetrain.velocity(RPM)/2, RPM)
        
        Flywheel.spin(Direction)
    
        wait(20, MSEC)

def onevent_controllerbuttonLUp_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    Choochoo.spin_for(FORWARD, 0.3, TURNS)

def onevent_controllerbuttonRUp_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    Flywheel.set_velocity(100, PERCENT)
    Direction = FORWARD

def onevent_controllerbuttonLDown_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    Choochoo.spin_for(FORWARD, 2.5, TURNS)

def onevent_controllerbuttonRDown_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    while not controller.buttonRDown.pressing():
        Flywheel.set_velocity(100, PERCENT)
        Direction = REVERSE
    Flywheel.set_velocity(0, PERCENT)

def onevent_controllerbuttonEUp_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    ExtraTension += 0.1

def onevent_controllerbuttonFUp_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision


def onevent_controllerbuttonEDown_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    ExtraTension += -0.1

def onevent_controllerbuttonFDown_pressed_0():
    global Goal, Direction, ExtraTension, vexcode_brain_precision, vexcode_console_precision
    if (Goal == "High"):
        Goal = "Low"
    else:
        Goal = "High"

# system event handlers
controller.buttonLUp.pressed(onevent_controllerbuttonLUp_pressed_0)
controller.buttonRUp.pressed(onevent_controllerbuttonRUp_pressed_0)
controller.buttonLDown.pressed(onevent_controllerbuttonLDown_pressed_0)
controller.buttonRDown.pressed(onevent_controllerbuttonRDown_pressed_0)
controller.buttonEUp.pressed(onevent_controllerbuttonEUp_pressed_0)
controller.buttonFUp.pressed(onevent_controllerbuttonFUp_pressed_0)
controller.buttonEDown.pressed(onevent_controllerbuttonEDown_pressed_0)
controller.buttonFDown.pressed(onevent_controllerbuttonFDown_pressed_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()
