# =========================================================
# صلاحيات وحدة الصيانة
# =========================================================

MAINTENANCE_VIEW = "maintenance.view"
MAINTENANCE_CREATE = "maintenance.create"
MAINTENANCE_UPDATE = "maintenance.update"
MAINTENANCE_DELETE = "maintenance.delete"
MAINTENANCE_COMPLETE = "maintenance.complete"


MAINTENANCE_PERMISSIONS = {
    MAINTENANCE_VIEW,
    MAINTENANCE_CREATE,
    MAINTENANCE_UPDATE,
    MAINTENANCE_DELETE,
    MAINTENANCE_COMPLETE,
}


def has_maintenance_permission(
    user_permissions,
    permission: str,
) -> bool:
    """
    التحقق من امتلاك المستخدم لصلاحية معينة.
    """

    if not user_permissions:
        return False

    return permission in user_permissions


def can_view_maintenance(user_permissions) -> bool:
    return has_maintenance_permission(
        user_permissions,
        MAINTENANCE_VIEW,
    )


def can_create_maintenance(user_permissions) -> bool:
    return has_maintenance_permission(
        user_permissions,
        MAINTENANCE_CREATE,
    )


def can_update_maintenance(user_permissions) -> bool:
    return has_maintenance_permission(
        user_permissions,
        MAINTENANCE_UPDATE,
    )


def can_delete_maintenance(user_permissions) -> bool:
    return has_maintenance_permission(
        user_permissions,
        MAINTENANCE_DELETE,
    )


def can_complete_maintenance(user_permissions) -> bool:
    return has_maintenance_permission(
        user_permissions,
        MAINTENANCE_COMPLETE,
)
