#!/usr/bin/env python3

import gi
from gi.repository import GLib

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except BaseException:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)


class GstManagerError(RuntimeError):
    pass


class GstManager:
    """
    Class that does the GStreamer operations.

    ...

    Attributes
    ----------
    gst_app : Gst.Pipeline
        The GStreamer application object.

    Methods
    -------
    make()
        Make the GStreamer application object.
    start()
        Start the GStreamer application.
    stop()
        Stop the GStreamer application.
    get_state():
        Getter for the Gstreamer application state.

    Raises
    ------
    GstManagerError
        This class custom exception.
    """

    def __init__(self, desc):
        """
         Parameters
         ----------
        _gst_app : Gst.Pipeline
            The GStreamer application object.
         """
        Gst.init(None)
        GLib.MainLoop()

        self._gst_app = self.make(desc)

    @classmethod
    def make(cls, desc):
        """Make the GStreamer application process.

        Parameters
        ----------
        desc : str
            The description of the application process to make.

        Returns
        -------
        gst_app : Gst.Pipeline
            The GStreamer application object.

        Raises
        ------
        GstManagerError
            If unable to make the GStreamer application process.
        """
        try:
            gst_app = Gst.parse_launch(desc)
        except BaseException:
            raise GstManagerError(
                'Unable to make the GStreamer application process.')

        return gst_app

    def start(self):
        """Start the GStreamer application.

        Parameters
        ----------

        Raises
        ------
        GstManagerError
            If unable to start the GStreamer application.
        """
        try:
            self._gst_app.set_state(Gst.State.PLAYING)
        except BaseException:
            GstManagerError('Unable to start the GStreamer application')

    def stop(self):
        """Stop the GStreamer application.

        Parameters
        ----------

        Raises
        ------
        GstManagerError
            If unable to stop the GStreamer application.
        """
        try:
            self._gst_app.set_state(Gst.State.NULL)
        except BaseException:
            GstManagerError('Unable to stop the GStreamer application')

    def get_state(self):
        """Getter for the Gstreamer application state.

        Parameters
        ----------

        Returns
        -------
        state : Gst.State
            The GStreamer application state.

        Raises
        ------
        """
        state = self._gst_app.get_state(Gst.CLOCK_TIME_NONE)[1]
        return state