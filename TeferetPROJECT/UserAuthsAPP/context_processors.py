from .models import UserProfile


def loggedUser(request):
    LoggedUserProfile = None
    if 'admin' in request.path:
        return dict(userProfile=LoggedUserProfile)
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user) 
    return dict(userProfile=LoggedUserProfile)
