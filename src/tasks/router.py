from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks

from src.auth.base_config import current_user
from src.tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix='/report')


# вариант с celery
@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return  {
        'status': 'success',
        'data': 'Письмо отправлено',
        'details': None
    }


# вариант без celery
'''
@router.get('/dashboard')
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    background_tasks.add_task(send_email_report_dashboard, user.username)
    return  {
        'status': 'success',
        'data': 'Письмо отправлено',
        'details': None
    }
'''