import os
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

"""
backref='addresses'  #直接使用表名
backref = backref('address')
backref = backref('address', order_by=id)

"""

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'data.one.many.sqlite')
engine = create_engine('sqlite:///' + db_path, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'     # User类映射到users表
    
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True) # Sequence表示id自增长, 主键       name = Column(String)
    fullname = Column(String)
    password = Column(String) 
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password     
              
        
    def __repr__(self):
        return "< User (name = '%s', fullname='%s', password='%s')>" %( self.name, self.fullname, self.password  )
    
    
class Address(Base):
    __tablename__ = 'addresses'      # Address类映射到addresses表
    #id = Column(Integer, primary_key=True)    
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True) # Sequence表示id自增长, 主键    
    email_address = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id'))   # 多对一。此表的外键就是 users表中的主键，id.多个Address属于一个User
    
    user_view = relationship("User", back_populates='addresses')    # 用户和地址关系表，没有实际数据库表，只是一个关系对照表
    
    def __init__(self, email_address):
        self.email_address = email_address        
        
    def __repr__(self):
        return "<Address (email_address='%s')>"  % self.email_address
    

User.addresses = relationship("Address", order_by=Address.id, back_populates="user_view") # 在User类中增加一个地址属性，指向地址的对照表
Base. metadata.create_all(engine)


  
#使用
zhangsan = User('zs','ZhangSan', 'abc222')   # 设置用户名
lisi = User('ls','LiSi', '123456') 

# 用户邮址
zhangsan.addresses = [
    Address(email_address="zhangsan@qq.com"),
    Address(email_address="zhangsan@163.com"),
]

lisi.addresses = [
    Address(email_address="lisi3@qq.com"),
    Address(email_address="lisi8@163.com"),
]



session.add_all([zhangsan, lisi])
session.commit()



