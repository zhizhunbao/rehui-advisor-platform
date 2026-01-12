from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, UUIDMixin


class Flight(Base, UUIDMixin):
    __tablename__ = "flights"

    airline: Mapped[str] = mapped_column(String)
    flight_number: Mapped[str] = mapped_column(String)
    departure_code: Mapped[str] = mapped_column(String)
    departure_name: Mapped[str] = mapped_column(String)
    departure_city: Mapped[str] = mapped_column(String)
    arrival_code: Mapped[str] = mapped_column(String)
    arrival_name: Mapped[str] = mapped_column(String)
    arrival_city: Mapped[str] = mapped_column(String)
    departure_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration: Mapped[int] = mapped_column(Integer)
    stops: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    cabin_class: Mapped[str] = mapped_column(String)
    available_seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_flights_route", "departure_code", "arrival_code"),
        Index("ix_flights_departure_time", "departure_time"),
        Index("ix_flights_price", "price"),
    )


class Hotel(Base, UUIDMixin):
    __tablename__ = "hotels"

    name: Mapped[str] = mapped_column(String)
    street: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    zip_code: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, default="USA")
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    review_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    review_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price_per_night: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    amenities: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    distance_to_center: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_hotels_location", "city", "state"),
        Index("ix_hotels_price", "price_per_night"),
        Index("ix_hotels_review_score", "review_score"),
    )


class Job(Base, UUIDMixin):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String)
    company: Mapped[str] = mapped_column(String)
    street: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    zip_code: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, default="USA")
    job_type: Mapped[str] = mapped_column(String)
    salary_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String, default="USD")
    pay_period: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    requirements: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    benefits: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    hours_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    flexibility: Mapped[str | None] = mapped_column(String, nullable=True)
    shifts: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    posted_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    application_url: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_jobs_location", "city", "state"),
        Index("ix_jobs_type", "job_type"),
        Index("ix_jobs_salary", "salary_min", "salary_max"),
    )


class Car(Base, UUIDMixin):
    __tablename__ = "cars"

    make: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    condition: Mapped[str] = mapped_column(String)
    mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    vin: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
    transmission: Mapped[str | None] = mapped_column(String, nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String, nullable=True)
    features: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    seller_type: Mapped[str] = mapped_column(String)
    seller_name: Mapped[str | None] = mapped_column(String, nullable=True)
    seller_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    seller_contact: Mapped[str | None] = mapped_column(String, nullable=True)
    street: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    zip_code: Mapped[str | None] = mapped_column(String, nullable=True)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_cars_make_model", "make", "model"),
        Index("ix_cars_year", "year"),
        Index("ix_cars_price", "price"),
        Index("ix_cars_condition", "condition"),
    )


class House(Base, UUIDMixin):
    __tablename__ = "houses"

    listing_type: Mapped[str] = mapped_column(String)
    property_type: Mapped[str] = mapped_column(String)
    street: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    zip_code: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, default="USA")
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    bedrooms: Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[float] = mapped_column(Float)
    square_feet: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lot_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)
    features: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    school_district_name: Mapped[str | None] = mapped_column(String, nullable=True)
    school_district_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    nearby_amenities: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    agent_name: Mapped[str | None] = mapped_column(String, nullable=True)
    agent_contact: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_houses_location", "city", "state"),
        Index("ix_houses_listing_type", "listing_type"),
        Index("ix_houses_price", "price"),
        Index("ix_houses_bedrooms", "bedrooms"),
    )


class Education(Base, UUIDMixin):
    __tablename__ = "education"

    institution: Mapped[str] = mapped_column(String)
    program: Mapped[str] = mapped_column(String)
    degree: Mapped[str] = mapped_column(String)
    major: Mapped[str] = mapped_column(String)
    street: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, default="USA")
    tuition: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    duration: Mapped[int] = mapped_column(Integer)
    overall_ranking: Mapped[int | None] = mapped_column(Integer, nullable=True)
    program_ranking: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ranking_source: Mapped[str | None] = mapped_column(String, nullable=True)
    admission_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_gpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    employment_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_salary: Mapped[float | None] = mapped_column(Float, nullable=True)
    application_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_education_institution", "institution"),
        Index("ix_education_degree_major", "degree", "major"),
        Index("ix_education_tuition", "tuition"),
    )


class Investment(Base, UUIDMixin):
    __tablename__ = "investments"

    product_name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    ticker: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    current_price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    risk_level: Mapped[str] = mapped_column(String)
    minimum_investment: Mapped[float | None] = mapped_column(Float, nullable=True)
    provider: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sector: Mapped[str | None] = mapped_column(String, nullable=True)
    market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)
    dividend_yield: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_investments_type", "type"),
        Index("ix_investments_risk_level", "risk_level"),
        Index("ix_investments_price", "current_price"),
    )
