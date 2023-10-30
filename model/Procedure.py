from .BaseTimestampMixin import TimestampMixin
from tortoise import fields


class Procedure(TimestampMixin):
    id = fields.IntField(pk=True, description="主键")
    procedure_b64 = fields.TextField(description="b64存储的函数")
    aes_mode = fields.CharField(max_length=255, default="ECB-pad", description="aes加密模式")
    aes_key = fields.TextField(max_length=255, description="b64形式存储的key")

    class Meta:
        table_description = "过程表"
        table = "procedure"
