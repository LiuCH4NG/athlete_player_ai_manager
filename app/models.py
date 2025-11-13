from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Date
from sqlalchemy.sql import func
from app.database import Base


class MedicalSupply(Base):
    __tablename__ = "medical_supplies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # 耗材名称
    code = Column(String, unique=True, index=True)  # 耗材编码
    category = Column(String, index=True)  # 分类（如：注射器、纱布、手套等）
    specification = Column(String)  # 规格型号
    manufacturer = Column(String)  # 生产厂家
    unit = Column(String)  # 单位（个、包、盒等）
    unit_price = Column(Float)  # 单价
    stock_quantity = Column(Integer)  # 库存数量
    min_stock = Column(Integer)  # 最低库存预警
    expiry_date = Column(Date)  # 有效期
    batch_number = Column(String)  # 批号
    storage_location = Column(String)  # 存储位置
    description = Column(String)  # 描述
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)
    remarks = Column(String)  # 备注
