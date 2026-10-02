import pytest
import sys
sys.path.insert(0, ".")
from src.services import validate_session_availability


def test_session_inside_available_slot_pass():
    tutor_time_slots = [
        {"start_time": "09:00", "end_time": "11:00"}
    ]
    session = {"start_time": "09:30", "end_time": "10:30"}
    assert validate_session_availability(session, tutor_time_slots) is True


def test_session_outside_slot_raise_exception():
    tutor_time_slots = [
        {"start_time": "09:00", "end_time": "11:00"}
    ]
    session = {"start_time": "14:00", "end_time": "15:00"}
    with pytest.raises(ValueError):
        validate_session_availability(session, tutor_time_slots)


def test_session_cross_slot_raise_exception():
    
    tutor_time_slots = [
        {"start_time": "09:00", "end_time": "11:00"}
    ]
    session = {"start_time": "10:00", "end_time": "11:30"}
    with pytest.raises(ValueError):
        validate_session_availability(session, tutor_time_slots)