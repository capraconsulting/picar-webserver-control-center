from __future__ import print_function


class ActionParseFailedException(Exception):
    pass

class PicarModulesUnavailableException(Exception):
    pass

def get_control_action(data):
    "Determines the control_action from JSON payload. Throws Exception otherwise"

    valid_actions = ("START_PICAR", "FORWARD", "BACKWARD", "RIGHT", "LEFT")
    action = data.get("action")
    if action in valid_actions:
        return action
    else:
        raise ActionParseFailedException

class PicarControl(object):
    def __init__(self):
        try:
            from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
            from picar import front_wheels
            from picar import back_wheels
            import time
            import picar
            import random
        except ImportError:
            # the Picar moduls are not available, most likely due to the code running outside the Raspberry Pi
            raise PicarModulesUnavailableException

        # 0 = random direction, 1 = force left, 2 = force right, 3 = orderdly
        force_turning = 0

        picar.setup()
        # ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
        self.fw = front_wheels.Front_Wheels(db='config')
        self.bw = back_wheels.Back_Wheels(db='config')
        self.fw.turning_max = 45

    def drive_from_action(self, action):
        pass
