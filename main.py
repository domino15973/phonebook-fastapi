from fastapi import FastAPI, status, HTTPException, Depends, Form
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import models
import schemas
from database import Base, engine, SessionLocal
import os
from dotenv import load_dotenv, find_dotenv


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Mount the templates and static directory
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Load .env
load_dotenv(find_dotenv(), override=True)


# Basic Authentication
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("USERNAME")
    correct_password = os.getenv("PASSWORD")

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, session: Session = Depends(get_session)):
    # get all contacts from the database
    contact_list = session.query(models.ContactModel).all()
    return templates.TemplateResponse("contact_list.html", {"request": request, "contacts": contact_list})


@app.get("/contact/create", response_class=HTMLResponse)
async def create_contact_page(request: Request):
    return templates.TemplateResponse("contact_create.html", {"request": request})


@app.post("/contact", response_model=schemas.PhonebookSchema, status_code=status.HTTP_201_CREATED)
def create_contact(
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone_number: str = Form(...),
        email: str = Form(...),
        session: Session = Depends(get_session)
):
    # create an instance of the ContactModel
    contact = models.ContactModel(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email
    )

    # add it to the session and commit it
    session.add(contact)
    session.commit()
    session.refresh(contact)

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/contact/{id}", response_class=HTMLResponse)
async def view_contact_page(id: int, request: Request, session: Session = Depends(get_session)):
    # get the contact with the given id
    contact = session.query(models.ContactModel).get(id)

    # check if contact with given id exists. If not, raise exception and return 404 not found response
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact with id {id} not found")

    return templates.TemplateResponse("contact_view.html", {"request": request, "contact": contact})


@app.get("/contact/{id}/edit", response_class=HTMLResponse)
async def edit_contact_page(id: int, request: Request, session: Session = Depends(get_session)):
    # get the contact with the given id
    contact = session.query(models.ContactModel).get(id)

    # check if contact with given id exists. If not, raise exception and return 404 not found response
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact with id {id} not found")

    return templates.TemplateResponse("contact_edit.html", {"request": request, "contact": contact})


@app.put("/contact/{id}/edit", response_model=schemas.PhonebookSchema)
def edit_contact(
        id: int,
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone_number: str = Form(...),
        email: str = Form(...),
        session: Session = Depends(get_session)
):
    # get the contact with the given id
    contact = session.query(models.ContactModel).get(id)

    # check if contact with given id exists. If not, raise exception and return 404 not found response
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact with id {id} not found")

    # update contact with the given data
    contact.first_name = first_name
    contact.last_name = last_name
    contact.phone_number = phone_number
    contact.email = email
    session.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/contact/{id}/delete", response_class=HTMLResponse)
async def delete_contact_page(id: int, request: Request, session: Session = Depends(get_session)):
    # get the contact with the given id
    contact = session.query(models.ContactModel).get(id)

    # check if contact with given id exists. If not, raise exception and return 404 not found response
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact with id {id} not found")

    return templates.TemplateResponse("contact_delete.html", {"request": request, "contact": contact})


@app.delete("/contact/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_username)])
def delete_contact(
    id: int,
    session: Session = Depends(get_session)
):
    # get the contact with the given id
    contact = session.query(models.ContactModel).get(id)

    # if contact with given id exists, delete it from the database. Otherwise, raise 404 error
    if contact:
        # Get the index of the contact
        contact_index = contact.id

        # Delete the contact
        session.delete(contact)
        session.commit()

        # Update the indexes of the remaining contacts
        session.execute(update(models.ContactModel).where(models.ContactModel.id > contact_index).values(id=models.ContactModel.id - 1))
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Contact with id {id} not found")

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
