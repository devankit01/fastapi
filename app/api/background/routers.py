from fastapi import BackgroundTasks, APIRouter, Depends,  File, UploadFile, HTTPException
from app.utils.jwt import authenticate_user
from .tasks.send_email import send_email_to_users
import csv
from functools import partial

router = APIRouter()


class BackgroundTaskView:
    """
    This class contains background tasks
    """
    @router.post("/send-emails")
    async def add_task(background_tasks : BackgroundTasks, file: UploadFile = File(...),  user_id: int = Depends(authenticate_user)):

        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
        # Read the CSV file and extract the email addresses
        try:
            content = await file.read()
            reader = csv.DictReader(content.decode('utf-8').splitlines())
            emails = [row['Email'] for row in reader if 'Email' in row] # take care if email is in lower or upper in file
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="CSV file has invalid data. Check if file has email column")


        task = partial(send_email_to_users, emails=emails)
        background_tasks.add_task(task)

        return {"message": "email sending started in the background","emails": emails}