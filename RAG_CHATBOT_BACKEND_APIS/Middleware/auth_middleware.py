import logging
from functools import wraps
from django.shortcuts import redirect

# Configure logger
logger = logging.getLogger(__name__)

def custom_login_required(view_func):
    """
    Custom login required decorator for MVC-based Django structure.
    Redirects to '/login/' if the user is not authenticated.
    
    Args:
        view_func: The view function to decorate.
    
    Returns:
        wrapper: A wrapped function that checks authentication status.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f"Checking authentication for view: {view_func.__name__}, user: {request.user}")
        if not request.user.is_authenticated:
            logger.info(f"User {request.user} is not authenticated, redirecting to /login/")
            return redirect('/login/')  # Redirect unauthorized users
        logger.debug(f"User {request.user} is authenticated, proceeding to view: {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return wrapper

def redirect_if_authenticated(view_func):
    """
    Redirects logged-in users away from login/register pages.
    
    Args:
        view_func: The view function to decorate.
    
    Returns:
        wrapper: A wrapped function that checks authentication status.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f"Checking authentication status for view: {view_func.__name__}, user: {request.user}")
        if request.user.is_authenticated:
            logger.info(f"User {request.user} is authenticated, redirecting to /dashboard/")
            return redirect('/dashboard/')  # Redirect logged-in users
        logger.debug(f"User {request.user} is not authenticated, proceeding to view: {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return wrapper