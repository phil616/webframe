from .BaseTimestampMixin import TimestampMixin
from tortoise import fields
from pydantic import BaseModel


class User(TimestampMixin):
    id = fields.IntField(pk=True, description="主键")
    username = fields.CharField(null=False, unique=True, max_length=255, description="用户名")
    password = fields.CharField(null=False, max_length=255, description="密码")
    fullname = fields.CharField(max_length=255, description="全名")
    email = fields.CharField(max_length=255, description="邮箱")

    class Meta:
        table_description = "用户表"
        table = "user"


class UserRole(TimestampMixin):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(unique=True, description="用户id")
    user_role = fields.IntField(default=1, description="用户scope")

    class Meta:
        table_description = "用户角色表"
        table = "user_role"
