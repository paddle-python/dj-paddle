from . import settings


def vendor_id(request):
    """
    Return the paddle.com vendor ID as a context variable
    """
    return {"DJPADDLE_VENDOR_ID": settings.DJPADDLE_VENDOR_ID}


def sandbox(request):
    """
    Return whether to use the Paddle.com sandbox environment
    as a context variable
    """
    return {"DJPADDLE_SANDBOX": settings.DJPADDLE_SANDBOX}
