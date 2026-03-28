from sqlalchemy import Column, Integer, Boolean, Text, String

# from sqlalchemy.orm import relationship
# We  call this SQLAlchemy Model: User, Order
# Package sqlalchemy_utils, sqlalchemy
# https://www.sqlalchemy.org/   vs. https://fastapi.tiangolo.com/tutorial/sql-databases/


class User:
    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)  # Bad practice , Store hashed_password
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    # Relation
    # order = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username} - {self.email}"
