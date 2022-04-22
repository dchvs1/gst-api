#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

import gi

try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except BaseException:
    _gstreamerAvailable = False
else:
    _gstreamerAvailable, args = Gst.init_check(None)

from gstapi.gstreamer.gstmanager import GstManager, GstAppManager, GstMaps, GstRecording


MOCKED_BUFFER_SIZE = 1


class MockGstBuffer:
    @classmethod
    def get_buffer(cls):
        buffer = Gst.Buffer.new_allocate(None, MOCKED_BUFFER_SIZE, None)
        return buffer


class GstManagerTests(unittest.TestCase):
    def setUp(self):
        self.GstManager = GstManager('videotestsrc ! fakesink')

    def test_make(self):
        self.assertIsInstance(
            GstManager.make('videotestsrc ! fakesink'),
            Gst.Pipeline)

    def test_start(self):
        self.GstManager.start()
        self.assertEqual(Gst.State.PLAYING, self.GstManager.get_state())

    def test_stop(self):
        self.GstManager.stop()
        self.assertEqual(Gst.State.NULL, self.GstManager.get_state())

    def test_get_state(self):
        self.assertIsInstance(self.GstManager.get_state(), Gst.State)


class MockPulledBuffersClient():
    def __init__(self, GstAppManager):
        self.GstAppManager = GstAppManager

    def __call__(self):
        return self.GstAppManager.pulled_buffer


class GstAppManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.GstAppManager = GstAppManager(
            'videotestsrc ! appsink emit-signals=true appsrc')
        self.GstAppManager.start()
        self.buffer = MockGstBuffer().get_buffer()

    def test_pull_buffer(self) -> None:
        buffer = self.GstAppManager.pull_buffer()
        self.assertIsInstance(buffer, Gst.Buffer)

    def test_pull_buffer_with_callback(self) -> None:
        pulled_buffer_client_callback = unittest.mock.create_autospec(
            MockPulledBuffersClient(self.GstAppManager))
        self.GstAppManager.pull_buffer.add_callback(
            pulled_buffer_client_callback)
        self.buffer = self.GstAppManager.pull_buffer()

        # Check the callback was called.
        pulled_buffer_client_callback.assert_called()

        pulled_buffer_client_callback = MockPulledBuffersClient(
            self.GstAppManager)
        self.GstAppManager.pull_buffer.add_callback(
            pulled_buffer_client_callback)
        self.buffer = self.GstAppManager.pull_buffer()

        # Check the returned buffer from callable method has the buffer than
        # its client got from it.
        self.assertEqual(self.buffer, pulled_buffer_client_callback.__call__())

    def test_push_buffer(self) -> None:
        self.GstAppManager.push_buffer(self.buffer)

    def test__install_pull_buffers_callback(self) -> None:
        self.GstAppManager._install_pull_buffers_callback()


class GstMapsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.buffer = MockGstBuffer().get_buffer()

    def test_map_buffer(self) -> None:
        result, mapinfo = GstMaps().map_buffer(self.buffer)
        self.assertTrue(True, result)
        self.assertIsInstance(mapinfo, Gst.MapInfo)
        self.assertTrue(mapinfo.size, MOCKED_BUFFER_SIZE)


class GstRecordingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.GstRecording = GstRecording()

    def test_make_recording(self) -> None:
        self.GstRecording.make_recording()
