from django.core.exceptions import PermissionDenied

class UserIsOwnerOrAdminMixin():
    '''
    Выполняем проверку. Будет возвращать True в случае, если USER_id
    объекта совпадает с пользователем, залогинившимся в систему. Это означает, что это его владелец,
    либо это администратор user.is.staff.
    '''

    def has_permission(self):
        return self.get_object().user == self.request.user or self.request.user.is_staff # является ли тот кто зарегеистрировался пользователем или администратором

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise PermissionDenied #Сбрасываем ошибку 403
        return super().dispatch(request, *args, **kwargs)
