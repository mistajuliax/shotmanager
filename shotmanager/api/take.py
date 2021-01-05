def get_name(take_instance):
    return take_instance.name


def set_name(take_instance, name):
    """ Set a unique name to the take
    """
    take_instance.name = name


def get_name_path_compliant(take_instance):
    return take_instance.getName_PathCompliant()


def get_shot_list(take_instance, ignore_disabled=False):
    """ Return a filtered copy of the shots associated to this take
    """
    return take_instance.getShotList(ignoreDisabled=ignore_disabled)


def get_num_shots(take_instance, ignore_disabled=False):
    """ Return the number of shots of the take
    """
    return take_instance.getNumShots(ignoreDisabled=ignore_disabled)


def get_shots_using_camera(take_instance, cam, ignore_disabled=False):
    """ Return the list of all the shots used by the specified camera
    """
    return take_instance.getShotsUsingCamera(cam, ignoreDisabled=ignore_disabled)

