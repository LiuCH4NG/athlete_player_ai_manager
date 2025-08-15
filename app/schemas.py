from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models for request and response


class AthleteBase(BaseModel):
    name: str
    height: Optional[float] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    sport_event: Optional[str] = None
    age: Optional[int] = None
    hometown: Optional[str] = None
    remarks: Optional[str] = None


class AthleteCreate(AthleteBase):
    # 可以添加创建时的特定验证或默认值
    pass


class AthleteUpdate(AthleteBase):
    # 使用可选字段以便只更新提供的字段
    name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    sport_event: Optional[str] = None
    age: Optional[int] = None
    hometown: Optional[str] = None
    remarks: Optional[str] = None


class AthleteInDB(AthleteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_deleted: bool

    class Config:
        from_attributes = True
