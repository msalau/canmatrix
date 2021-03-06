# -*- coding: utf-8 -*-
import pytest
import io
import canmatrix.canmatrix
import canmatrix.formats


@pytest.fixture
def default_matrix():
    matrix = canmatrix.canmatrix.CanMatrix()
    some_define = canmatrix.Define("INT 0 65535")
    frame = canmatrix.canmatrix.Frame(name="test_frame", id=10)
    frame.addAttribute("my_attribute1", "my_value1")
    signal = canmatrix.canmatrix.Signal(name="test_signal", size=8)
    signal.addValues(0xFF, "Init")
    signal.addAttribute("my_attribute2", "my_value2")
    frame.addSignal(signal)

    signal = canmatrix.canmatrix.Signal(name="multi", multiplex=True, size=3, unit="attosecond")
    frame.addSignal(signal)

    matrix.addFrame(frame)
    matrix.frameDefines["my_attribute1"] = some_define
    matrix.signalDefines["my_attribute2"] = some_define
    return matrix


def test_export_with_jsonall(default_matrix):
    """Check the jsonAll doesn't raise and export some additional field."""
    matrix = default_matrix
    out_file = io.BytesIO()
    canmatrix.formats.dump(matrix, out_file, "cmjson", jsonAll=True)
    data = out_file.getvalue().decode("utf-8")
    assert "my_value1" in data
    assert "my_value2" in data


def test_export_additional_frame_info(default_matrix):
    matrix = default_matrix
    out_file = io.BytesIO()
    canmatrix.formats.dump(matrix, out_file, "cmjson", additionalFrameAttributes="my_attribute1")
    data = out_file.getvalue().decode("utf-8")
    assert "my_value1" in data
