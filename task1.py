from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
import re

app = FastAPI()

MIN_USERNAME_LENGTH = 3
USERNAME_REGEX = r"^[a-zA-Z0-9_-]+$"

class Address(BaseModel):
  street: str
  city: str
  zip: str

class User(BaseModel):
  name: str
  email: str
  address: Address
  profile: dict

class Report(BaseModel):
  title: str
  content: str

@app.get("/items/")
async def get_items(name: str, category: str, price: float):
  return {"name": name, "category": category, "price": price}

@app.get("/search/")
async def search(
    query: str = Query(..., description="Search term"),
    page: int = Query(1, description="Page number"),
    size: int = Query(10, description="Items per page"),
):
  return {
      "query": query,
      "page": page,
      "size": size,
      "results": ["item1", "item2", "item3"],  # Replace with actual search results
  }

@app.post("/users/")
async def create_user(user: User):
  return user

@app.get("/validate/")
async def validate_username(username: str):
  if len(username) < MIN_USERNAME_LENGTH:
    raise HTTPException(400, detail="Username must be at least 3 characters long")
  if not re.match(USERNAME_REGEX, username):
    raise HTTPException(400, detail="Username can only contain letters, numbers, underscores, and hyphens")
  return {"message": "Username is valid"}

@app.post("/reports/{report_id}")
async def create_report(report_id: int, start_date: str, end_date: str, report: Report):
  if report_id <= 0:
    raise HTTPException(400, detail="Report ID must be positive")
  # Additional date format validation can be added here
  return {
      "report_id": report_id,
      "start_date": start_date,
      "end_date": end_date,
      "report": report.dict(),
  }
