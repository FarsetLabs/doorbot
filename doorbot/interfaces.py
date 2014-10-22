import time
from doorbot import app

def pick(choice):
    """
    Select and return an interface definition
    :param choice:
    :return:
    """

    candidate_cls = {
        'dummy': Dummy,
        'piface':PiFace
    }.get(choice)
    try:
        candidate_cls.import_prerequisites()
        return candidate_cls
    except ImportWarning as e:
        app.log.error("Prequsite Failed, loading dummy interface: {}".format(e))
        return Dummy


class Abstract_Interface(object):
    """
    Generic interface definition providing minimum operation standard
    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        self.door_name = kwargs.get('door_name',"Default")

    def activate(self):
        """
        Wake up the interface
        :return:
        """
        raise NotImplementedError("Abstract Interface")

    def is_active(self):
        """
        Bool response if interface is available and active
        :return:
        """
        raise NotImplementedError("Abstract Interface")

    def open(self, duration=10):
        """
        Open the door for <duration> seconds

        Return state is constrained and this call may or may not be asynchronous
        :param durationdefault 10
        :return:
        """
        raise NotImplementedError("Abstract Interface")

    def is_open(self):
        """
        (Optional) Detect if door is open.

        Return "None" if no reed switch configured
        :return:
        """
        return None

    @classmethod
    def import_prerequisites(cls):
        """
        Lay the ground work
        """
        pass

class Logging_MixIn(Abstract_Interface):
    """
    Logging Version
    """
    def __init__(self, *args, **kwargs):
        """
        Instantiate logging interface
        :param args:
        :param kwargs:
        :return:
        """
        Abstract_Interface.__init__(self, *args, **kwargs)
        from logbook import Logger
        self.log = Logger("{}-{}".format(type(self).__name__,self.door_name))
        self.log.debug("Initialised using : {}".format(kwargs))

    def activate(self):
        self.log.debug("Activated")

    def is_active(self):
        self.log.debug("Checking activation")

    def open(self, duration=10):
        self.log.info("Opening for {}".format(duration))

class Dummy(Logging_MixIn):
    open_status = False
    open_time = time.time()
    def is_active(self):
        super(Dummy, self).is_active()
        return (True,True)

    def open(self, duration=10):
        """
        True on success, False on Exception (not implemented), None on 'double jeopardy'
        """

        Logging_MixIn.open(self)
        if not self.open_status:
            self.open_status=True
            self.open_time = time.time()
            while time.time() - self.open_time < duration:
                time.sleep(1.0)
                if not self.open_status:
                    self.log.error("Door closed before told, possible race condition")

            self.open_status=False
            return (True, "Door opened {}s ago".format(time.time()-self.open_time))
        else:
            self.log.warn("Door already open")
            return (None, "Door already open for {}s".format(time.time()-self.open_time))

    def is_open(self):
        return self.open_status

class PiFace(Logging_MixIn):
    pfd = None
    open_time = None

    def __init__(self, *args, **kwargs):

        super(PiFace, self).__init__(*args, **kwargs)
        self.pfd = pifacedigitalio.PiFaceDigital()
        self.relay = kwargs.get('interfaceopt',0)
        self.log.warn("Got Config {}".format(kwargs))
        self.log.warn("Using Relay {}".format(self.relay))

    def is_active(self):
        return self.pfd is not None

    def _open(self):
        self.pfd.relays[self.relay].value=1
        self.pfd.leds[self.relay].value=1
        self.open_time = time.time()

    def _close(self):
        self.pfd.relays[self.relay].value=0
        self.pfd.leds[self.relay].value=0

    def open(self, duration=1):
        super(PiFace, self).open(duration)
        self._open()
        while time.time() - self.open_time < duration:
            time.sleep(1.0)
        self._close()

        return (True, "{} opened {}s ago".format(self.door_name, time.time()-self.open_time))

    def is_open(self, door=0):
        return self.pfd.relays[door].value

    @classmethod
    def import_prerequisites(cls):
        """
        Lay the ground work
        """
        try:
            import pifacedigitalio
        except ImportError:
            raise ImportWarning("No PiFaceDigitalIO Module, Cannot instantiate PiFace")

