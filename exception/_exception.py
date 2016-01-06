import sys

Generic_Error_msg = "*** Error -- "


def icheck_TypeError(obj, cls_to_be_checked, message = ""):
    try:
        input_cls = obj.__class__.__name__
        if input_cls != cls_to_be_checked:
            raise TypeError(Generic_Error_msg + "Type Error -- [{0}] class is incorrect. ".format(input_cls) + message)
    except TypeError as err:
        sys.exit(err.args[0])
