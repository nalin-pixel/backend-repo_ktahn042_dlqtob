"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (can be kept for reference/tests)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# CCBC Murrieta content schemas

class Sermon(BaseModel):
    """Sermons collection"""
    title: str
    speaker: Optional[str] = None
    series: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    notes_url: Optional[str] = None
    scripture: Optional[str] = None
    description: Optional[str] = None

class Event(BaseModel):
    """Events collection"""
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    registration_url: Optional[str] = None

class Ministry(BaseModel):
    """Ministries collection"""
    name: str
    summary: Optional[str] = None
    meeting_times: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class Story(BaseModel):
    """Stories/testimonies collection"""
    title: str
    body: str
    author: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)

class Leader(BaseModel):
    """Leadership bios"""
    name: str
    role: str
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None

class ContactMessage(BaseModel):
    """General connect/contact form submissions"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str
    newsletter_opt_in: bool = False

class PrayerRequest(BaseModel):
    """Prayer requests submissions"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    request: str
    allow_followup: bool = False

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint (if implemented)
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints for editor usage,
#    but we expose read + submit endpoints for the public site.
