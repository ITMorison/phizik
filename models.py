from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    experiment_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    author: Mapped[str] = mapped_column(String(120), default="Eco Pack Lab", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    samples: Mapped[list["Sample"]] = relationship(back_populates="experiment", cascade="all, delete-orphan")


class Sample(Base):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    composition: Mapped[str] = mapped_column(Text, default="", nullable=False)
    experiment: Mapped[Experiment] = relationship(back_populates="samples")
    mass_measurements: Mapped[list["MassMeasurement"]] = relationship(back_populates="sample", cascade="all, delete-orphan")
    quality: Mapped["QualityCriteria | None"] = relationship(back_populates="sample", cascade="all, delete-orphan", uselist=False)


class MassMeasurement(Base):
    __tablename__ = "mass_measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sample_id: Mapped[int] = mapped_column(ForeignKey("samples.id", ondelete="CASCADE"), nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    mass: Mapped[float] = mapped_column(Float, nullable=False)
    sample: Mapped[Sample] = relationship(back_populates="mass_measurements")


class QualityCriteria(Base):
    __tablename__ = "quality_criteria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sample_id: Mapped[int] = mapped_column(ForeignKey("samples.id", ondelete="CASCADE"), nullable=False, unique=True)
    flexibility: Mapped[float] = mapped_column(Float, nullable=False)
    strength: Mapped[float] = mapped_column(Float, nullable=False)
    water_resistance: Mapped[float] = mapped_column(Float, nullable=False)
    water_stability: Mapped[float] = mapped_column(Float, nullable=False)
    biodegradability: Mapped[float] = mapped_column(Float, nullable=False)
    sample: Mapped[Sample] = relationship(back_populates="quality")


class WeightSetting(Base):
    __tablename__ = "weight_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flexibility: Mapped[float] = mapped_column(Float, default=0.25, nullable=False)
    strength: Mapped[float] = mapped_column(Float, default=0.20, nullable=False)
    water_resistance: Mapped[float] = mapped_column(Float, default=0.20, nullable=False)
    water_stability: Mapped[float] = mapped_column(Float, default=0.15, nullable=False)
    biodegradability: Mapped[float] = mapped_column(Float, default=0.20, nullable=False)
