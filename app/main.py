from config.models import User, PaymentForm, PaymentLog
from config.schemas import UserSchema, PaymentFormSchema, PaymentLogSchema
import authentication.auth as auth
import notification.mail as mail

from config.schemas import MailSchema
from notification.mailer import send_mail
from fastapi import BackgroundTasks

from config.dependencies import db_dependency, user_dependency
from fastapi import FastAPI, HTTPException, status


app = FastAPI()
app.include_router(auth.router)


@app.post('/payment-form/create', status_code=status.HTTP_201_CREATED)
async def create_payment_form(user: user_dependency, payment_form: PaymentFormSchema, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to create new form.')
    form_dict = payment_form.dict()
    form_name = str(form_dict["form_name"]).replace(' ', '-')
    url_param = f'{form_dict["user_id"]}/{form_name}' 
    form_dict['form_url'] = 'http://localhost:8000/'.join(url_param)
    
    new_form = PaymentForm(**form_dict)
    db.add(new_form)
    db.commit()

    return {'form': form_dict}


@app.get('/payment-form/{user_id}/{name}', status_code=status.HTTP_200_OK)
async def make_payment_ready(user_id: int, name: str, db: db_dependency):
    form_name = name.replace('-', ' ')
    payment_form = db.query(PaymentForm).filter(PaymentForm.user_id==user_id, PaymentForm.form_name==form_name).first()
    if payment_form is None:
        return HTTPException(status_code=404, detail= "No form is found in this link")
    
    return {'form_id': payment_form.id, 
            'form_name': form_name,
            'user_id': user_id,
            'amount': payment_form.amount,
            }


@app.post('/transaction/{user_id}/{form_id}', status_code=status.HTTP_201_CREATED)
async def make_the_transaction(pay_log: PaymentLogSchema, db: db_dependency):
    log_data = PaymentLog(**pay_log.dict())
    db.add(log_data)
    db.commit()

    user_email = db.query(User).filter(User.id==pay_log.user_id).first().email
    mail.schedule_mail(user_email)

    return {'status': 'transaction complete successfully'}


def schedule_mail(to_user: str):
    data['to'] = to_user
    data['subject'] = 'Payment notification'
    data['body'] = 'A payment is successfully executed'
    tasks = BackgroundTasks()
    tasks.add_task(send_mail, data)
    
    return {'status': 200, 'message': 'mail has been scheduled'}
