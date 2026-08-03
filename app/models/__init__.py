"""
Fleet Assets Manager - Models Package

يتم استيراد جميع النماذج هنا صراحة حتى يتم تسجيلها
في SQLAlchemy Base.metadata قبل استدعاء create_all(),
وحتى تكون كل النماذج معروفة لبعضها عند تعريف
العلاقات (relationships) بينها.
"""

from app.models import audit_log
from app.models import battery
from app.models import branch
from app.models import department
from app.models import driver
from app.models import equipment
from app.models import equipment_assignment
from app.models import equipment_status
from app.models import equipment_type
from app.models import fuel_log
from app.models import maintenance_order
from app.models import maintenance_schedule
from app.models import maintenance_type
from app.models import mission
from app.models import notification
from app.models import organization
from app.models import part
from app.models import part_request
from app.models import part_type
from app.models import permission
from app.models import role
from app.models import setting
from app.models import stock
from app.models import tire
from app.models import user
from app.models import user_role
