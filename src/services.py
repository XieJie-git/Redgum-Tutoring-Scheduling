def validate_session_availability(session_data, tutor_availability):
    """
    
    :param session_data: dict start_time end_time 
    :param tutor_availability: list[dict]
    :return: True 
    :raises ValueError: 
    """
    session_start = session_data["start_time"]
    session_end = session_data["end_time"]

    valid_slot_found = False
    for slot in tutor_availability:
        slot_s = slot["start_time"]
        slot_e = slot["end_time"]
        
        if slot_s <= session_start and session_end <= slot_e:
            valid_slot_found = True
            break

    if not valid_slot_found:
        raise ValueError("Session time does not match tutor availability rules")
    return True
