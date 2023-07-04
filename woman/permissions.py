from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """ все права наследуются от этого класса BasePermission пример прав скопировал из IsAdminUser этого класса
    Такой класс дает всем доступ по ГЕТ , но удаление только админам
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ все права наследуются от этого класса BasePermission.
    Такой класс дает всем доступ по ГЕТ , но удаление только админам
    ! обратить внимание на функцию. она принимает другие аргументы
    """
    def has_object_permission(self, request, view, obj):
        # obj это по сути строка из бд по id в гет запросе именно поэтому has_object_permission
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user