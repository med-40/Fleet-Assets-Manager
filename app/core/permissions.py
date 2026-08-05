from enum import Enum


# =========================================================
# أدوار المستخدمين
# =========================================================

class UserRole(str, Enum):

    ADMIN = "admin"

    MANAGER = "manager"

    ACCOUNTANT = "accountant"

    TASK_MANAGER = "task_manager"

    VIEWER = "viewer"


# =========================================================
# الوحدات الرئيسية في النظام
# =========================================================

class ModuleName(str, Enum):

    DASHBOARD = "dashboard"

    EQUIPMENT = "equipment"

    DRIVERS = "drivers"

    MISSIONS = "missions"

    MAINTENANCE = "maintenance"

    FUEL = "fuel"

    FAULTS = "faults"

    BATTERIES = "batteries"

    TIRES = "tires"

    SPARE_PARTS = "spare_parts"

    WORKSHOPS = "workshops"

    REPORTS = "reports"

    NOTIFICATIONS = "notifications"

    USERS = "users"

    AUDIT_LOG = "audit_log"


# =========================================================
# العمليات
# =========================================================

class PermissionAction(str, Enum):

    VIEW = "view"

    CREATE = "create"

    EDIT = "edit"

    DELETE = "delete"


# =========================================================
# الصلاحيات الافتراضية
# =========================================================

DEFAULT_PERMISSIONS = {

    UserRole.ADMIN: {
        module.value: [
            action.value
            for action in PermissionAction
        ]
        for module in ModuleName
    },

    UserRole.MANAGER: {
        ModuleName.DASHBOARD.value: ["view"],
        ModuleName.EQUIPMENT.value: [
            "view",
            "create",
            "edit",
            "delete",
        ],
        ModuleName.DRIVERS.value: [
            "view",
            "create",
            "edit",
            "delete",
        ],
        ModuleName.MISSIONS.value: [
            "view",
            "create",
            "edit",
            "delete",
        ],
        ModuleName.MAINTENANCE.value: [
            "view",
            "create",
            "edit",
            "delete",
        ],
        ModuleName.FUEL.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.FAULTS.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.BATTERIES.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.TIRES.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.SPARE_PARTS.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.WORKSHOPS.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.REPORTS.value: [
            "view",
            "create",
        ],
        ModuleName.NOTIFICATIONS.value: [
            "view",
        ],
        ModuleName.USERS.value: [
            "view",
            "create",
            "edit",
            "delete",
        ],
        ModuleName.AUDIT_LOG.value: [
            "view",
        ],
    },

    UserRole.ACCOUNTANT: {
        ModuleName.DASHBOARD.value: ["view"],
        ModuleName.EQUIPMENT.value: ["view"],
        ModuleName.DRIVERS.value: ["view"],
        ModuleName.FUEL.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.SPARE_PARTS.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.REPORTS.value: [
            "view",
            "create",
        ],
        ModuleName.NOTIFICATIONS.value: [
            "view",
        ],
    },

    UserRole.TASK_MANAGER: {
        ModuleName.DASHBOARD.value: ["view"],
        ModuleName.EQUIPMENT.value: ["view"],
        ModuleName.DRIVERS.value: ["view"],
        ModuleName.MISSIONS.value: [
            "view",
            "create",
            "edit",
        ],
        ModuleName.REPORTS.value: ["view"],
        ModuleName.NOTIFICATIONS.value: ["view"],
    },

    UserRole.VIEWER: {
        ModuleName.DASHBOARD.value: ["view"],
        ModuleName.EQUIPMENT.value: ["view"],
        ModuleName.DRIVERS.value: ["view"],
        ModuleName.MISSIONS.value: ["view"],
        ModuleName.MAINTENANCE.value: ["view"],
        ModuleName.FUEL.value: ["view"],
        ModuleName.FAULTS.value: ["view"],
        ModuleName.BATTERIES.value: ["view"],
        ModuleName.TIRES.value: ["view"],
        ModuleName.SPARE_PARTS.value: ["view"],
        ModuleName.WORKSHOPS.value: ["view"],
        ModuleName.REPORTS.value: ["view"],
        ModuleName.NOTIFICATIONS.value: ["view"],
    },
}


# =========================================================
# فحص الصلاحية
# =========================================================

def has_permission(
    role: str,
    module: str,
    action: str,
) -> bool:

    try:
        user_role = UserRole(role)
    except ValueError:
        return False

    permissions = DEFAULT_PERMISSIONS.get(
        user_role,
        {},
    )

    allowed_actions = permissions.get(
        module,
        [],
    )

    return action in allowed_actions
