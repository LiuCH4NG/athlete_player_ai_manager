from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Pydantic models for request and response


class MedicalSupplyBase(BaseModel):
    name: str  # 耗材名称
    code: str  # 耗材编码
    category: Optional[str] = None  # 分类
    specification: Optional[str] = None  # 规格型号
    manufacturer: Optional[str] = None  # 生产厂家
    unit: Optional[str] = None  # 单位
    unit_price: Optional[float] = None  # 单价
    stock_quantity: Optional[int] = None  # 库存数量
    min_stock: Optional[int] = None  # 最低库存预警
    expiry_date: Optional[date] = None  # 有效期
    batch_number: Optional[str] = None  # 批号
    storage_location: Optional[str] = None  # 存储位置
    description: Optional[str] = None  # 描述
    remarks: Optional[str] = None  # 备注


class MedicalSupplyCreate(MedicalSupplyBase):
    # 可以添加创建时的特定验证或默认值
    pass


class MedicalSupplyUpdate(BaseModel):
    # 使用可选字段以便只更新提供的字段
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    specification: Optional[str] = None
    manufacturer: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    min_stock: Optional[int] = None
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = None
    storage_location: Optional[str] = None
    description: Optional[str] = None
    remarks: Optional[str] = None


class MedicalSupplySearch(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    specification: Optional[str] = None
    manufacturer: Optional[str] = None
    unit: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = None
    storage_location: Optional[str] = None
    description: Optional[str] = None
    remarks: Optional[str] = None


class MedicalSupplyInDB(MedicalSupplyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_deleted: bool

    class Config:
        from_attributes = True
