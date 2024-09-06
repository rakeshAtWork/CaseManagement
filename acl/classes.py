import logging
from django.utils.encoding import force_str

logger = logging.getLogger(name="CMS")


class PermissionNamespace:
    _all_namespaces = []

    def __init__(self, name):
        self.name = name
        self.permissions = []
        self.__class__._all_namespaces.append(self)

    def add_permission(self, privilege_name, privilege_desc, module_id=""):
        permission = Permission(namespace=self, privilege_name=privilege_name, privilege_desc=privilege_desc,
                                module_id=module_id)
        self.permissions.append(permission)
        # create_permission([permission])
        return permission

    @classmethod
    def get_all_namespaces(cls):
        return cls._all_namespaces

    def __str__(self):
        return force_str(self.name)


class Permission:

    def __init__(self, namespace, privilege_name, privilege_desc, module_id):
        self.namespace = namespace
        self.privilege_name = privilege_name
        self.privilege_desc = privilege_desc
        self.module_id = module_id
        self.pk = self.get_pk()

    def get_pk(self):
        return self.privilege_name
