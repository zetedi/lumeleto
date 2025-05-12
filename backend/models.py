from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many Lifeseed <-> Lifetree
guardianship = Table(
    "guardianship",
    Base.metadata,
    Column("lifeseed_id", Integer, ForeignKey("lifeseeds.id"), primary_key=True),
    Column("lifetree_id", Integer, ForeignKey("lifetrees.id"), primary_key=True),
)

# Association table for approvals of a Pulse
pulse_approvals = Table(
    "pulse_approvals",
    Base.metadata,
    Column("lifeseed_id", Integer, ForeignKey("lifeseeds.id"), primary_key=True),
    Column("pulse_id", Integer, ForeignKey("pulses.id"), primary_key=True),
)

# Association table for vetoes of a Pulse
pulse_vetoes = Table(
    "pulse_vetoes",
    Base.metadata,
    Column("lifeseed_id", Integer, ForeignKey("lifeseeds.id"), primary_key=True),
    Column("pulse_id", Integer, ForeignKey("pulses.id"), primary_key=True),
)

class Lifeseed(Base):
    __tablename__ = "lifeseeds"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=True)  # hashed password or null if OAuth
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    lifetrees = relationship("Lifetree", secondary=guardianship, back_populates="guardians")
    pulses = relationship("Pulse", back_populates="creator")
    approved_pulses = relationship("Pulse", secondary=pulse_approvals, back_populates="approvers")
    vetoed_pulses = relationship("Pulse", secondary=pulse_vetoes, back_populates="vetoers")

class Lifetree(Base):
    __tablename__ = "lifetrees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    latitude = Column(String)
    longitude = Column(String)
    planted_at = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String)

    # Guardians (many-to-many with Lifeseeds)
    guardians = relationship("Lifeseed", secondary=guardianship, back_populates="lifetrees")

class Pulse(Base):
    __tablename__ = "pulses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    fulfilled = Column(Boolean, default=False)

    creator_id = Column(Integer, ForeignKey("lifeseeds.id"))
    creator = relationship("Lifeseed", back_populates="pulses")

    approvers = relationship("Lifeseed", secondary=pulse_approvals, back_populates="approved_pulses")
    vetoers = relationship("Lifeseed", secondary=pulse_vetoes, back_populates="vetoed_pulses")
