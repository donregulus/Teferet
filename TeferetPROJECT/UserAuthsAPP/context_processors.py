from .models import UserProfile


def loggedUser(request):
    LoggedUserProfile = None
    if 'admin' in request.path:
        return dict(userProfile=LoggedUserProfile)
    if request.user.is_authenticated and not request.user.is_superuser:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user) 
    return dict(userProfile=LoggedUserProfile)
