from __future__ import print_function


class PicarControlMock(object):
    def drive_from_action(self, action):
        print("ACTION: {}".format(action))
