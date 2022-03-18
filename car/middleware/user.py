class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        from car.service.user import NULL_USER, UserService

        sessionid = request.COOKIES.get("sessionid") or ""
        user_id = UserService.get_user_id(sessionid)
        if user_id is None:
            user = NULL_USER
        else:
            user = UserService.get_one(user_id)
        setattr(request, "user", user)
        response = self.get_response(request)
        return response
