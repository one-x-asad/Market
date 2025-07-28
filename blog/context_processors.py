from .models import UserProfile

def user_balance(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'balance': profile.balance}
        except UserProfile.DoesNotExist:
            return {'balance': 0}
    return {'balance': 0}
