import stripe 
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from app.models import User
from tortoise.exceptions import DoesNotExist

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

class CreateSubscriptionSchema(BaseModel):
    plan: str
    email: str
    user_id: int

@router.post("/create-subscription")
async def create_subscription(data: CreateSubscriptionSchema):
    try:
        if data.plan == "pro":
            price_id = os.getenv("PRICE_ID_PRO")
        else:
            price_id = os.getenv("PRICE_ID_BASIC")

        # 1. Crear el cliente en Stripe
        customer = stripe.Customer.create(
            email=data.email,
            metadata={"user_id": str(data.user_id)},  # Guardar el user_id en los metadatos data.user_id}
        )

        # 2. Crear la suscripción
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
        )
        
        # 3. Obtener el client_secret para el frontend
        client_secret = subscription.latest_invoice.payment_intent.client_secret
        
        return {"client_secret": client_secret, "subscription_id": subscription.id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Maneja el evento cuando un pago es exitoso
    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        subscription_id = invoice['subscription']
        
        # Obtener la suscripción y el customer_id
        subscription = stripe.Subscription.retrieve(subscription_id, expand=['customer'])
        customer = subscription.customer
        
        # Aquí es donde obtienes el user_id que guardaste en los metadatos
        user_id = customer.metadata.get('user_id')
        
        if user_id:
            try:
                # Actualiza el rol del usuario en tu base de datos
                user = await User.get(id=int(user_id))
                user.rol = 'pro' if invoice['lines']['data'][0]['price']['id'] == os.getenv("PRICE_ID_PRO") else 'usuario'
                await user.save()
                print(f"Rol del usuario {user.email} actualizado a {user.rol}")
            except DoesNotExist:
                print(f"Error: Usuario con ID {user_id} no encontrado.")

    # Puedes manejar otros eventos aquí si quieres
    
    return {"status": "success"}


