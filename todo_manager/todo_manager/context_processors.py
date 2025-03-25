def user_info(request):
    if request.user.is_authenticated:
        return {
            "user_balance": request.user.balance,
            "user_rating": request.user.rating,
        }
    return {}
