from . import settings


def vendor_id(request):
    """
    Return the paddle.com vendor ID as a context variables
    """
    return {"DJPADDLE_VENDOR_ID": settings.DJPADDLE_VENDOR_ID}
