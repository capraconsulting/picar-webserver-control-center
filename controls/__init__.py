from __future__ import print_function

import time

SPEED = 70


class ActionParseFailedException(Exception):
    pass


class PicarModulesUnavailableException(Exception):
    pass


def get_control_action(data):
    """Determines the control_action from JSON payload.
    Throws Exception otherwise""" ""

    valid_actions = ("DRIVE", "FORWARD", "BACKWARD", "RIGHT", "LEFT")
    action = data.get("action")
    if action in valid_actions:
        return action
    else:
        raise ActionParseFailedException


class PicarControl(object):
    right_angle = 45
    left_angle = 30

    def __init__(self, debug=False):
        try:
            from picar import front_wheels
            from picar import back_wheels
            import picar
        except ImportError:
            # the Picar moduls are not available,
            # most likely due to the code running outside the Raspberry Pi
            raise PicarModulesUnavailableException

        picar.setup()
        # ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
        self.fw = front_wheels.Front_Wheels(db='config')
        # self.fw.turning_max = 45
        self.fw.debug = debug

        self.bw = back_wheels.Back_Wheels(db='config')
        self.bw.debug = debug

    def drive_from_action(self, action):
        # if action == "DRIVE":
        if action == "FORWARD":
            self.fw.turn_straight()
            self.bw.forward()
            self.bw.speed = SPEED
            time.sleep(1)
            self.bw.stop()
            self.fw.turn_straight()

        elif action == "BACKWARD":
            self.fw.turn_straight()
            self.bw.backward()
            self.bw.speed = SPEED
            time.sleep(1)
            self.bw.stop()

        elif action == "RIGHT":
            self.bw.forward()
            self.fw.turn_right()
            self.bw.speed = SPEED
            time.sleep(1)
            self.bw.stop()

        elif action == "LEFT":
            self.bw.forward()
            self.fw.turn_left()
            self.bw.speed = SPEED
            time.sleep(1)
            self.bw.stop()

    def shut_down(self):
        self.bw.stop()
        self.fw.turn_straight()
