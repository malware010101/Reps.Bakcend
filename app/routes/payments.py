import stripe
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
from app.models import User
from tortoise.exceptions import DoesNotExist
from app.auth import hash_password, register_user_in_db


router = APIRouter()


class CreateSubscriptionSchema(BaseModel):
    plan: str
    email: str
    name: str
    password: str


@router.post("/create-subscription")
async def create_subscription(data: CreateSubscriptionSchema):
    try:
        hashed_password = hash_password(data.password)

        if data.plan == "pro":
            price_id = os.getenv("PRICE_ID_PRO")
            final_role = "pro"
        elif data.plan == "usuario":
            price_id = os.getenv("PRICE_ID_BASIC")
            final_role = "usuario"
        else:
            raise HTTPException(status_code=400, detail="Plan invalido")

        customer = stripe.Customer.create(
            email=data.email,
            name=data.name,
            metadata={
                "user_name": data.name,
                "user_email": data.email,
                "password_hash": hashed_password,
                "final_role": final_role
            }
        )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': price_id}],
            collection_method="charge_automatically",
            payment_behavior='default_incomplete',
            payment_settings={'payment_method_types': ['card']},
            expand=['latest_invoice.payment_intent']
        )

        latest_invoice = subscription["latest_invoice"]
        payment_intent = latest_invoice["payment_intent"]
        client_secret = payment_intent["client_secret"]

        return {
            "client_secret": client_secret,
            "subscription_id": subscription.id
        }

    except Exception as e:
        print(f"Error al crear suscripción in-app: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']

        if not invoice.get('subscription'):
            return {"status": "ignored"}

        subscription_id = invoice['subscription']

        subscription = stripe.Subscription.retrieve(
            subscription_id, expand=['customer'])
        customer = subscription.customer

        user_id = customer.metadata.get('user_id')

        if user_id:
            try:
                user = await User.get(id=int(user_id))
                user.rol = 'pro' if invoice['lines']['data'][0]['price']['id'] == os.getenv(
                    "PRICE_ID_PRO") else 'usuario'
                await user.save()
                print(
                    f"Renovación exitosa para user_id: {user_id}. Rol: {user.rol}")
            except DoesNotExist:
                print(
                    f"Error: Usuario con ID {user_id} no encontrado en renovación. Debe ser manual.")

        else:
            metadata = customer.metadata

            new_user = await register_user_in_db(
                nombre=metadata.get("user_name"),
                email=metadata.get("user_email"),
                password_hash=metadata.get("password_hash"),
                rol=metadata.get("final_role")
            )

            if new_user:
                print(
                    f"USUARIO REGISTRADO Y SUSCRITO {new_user.email}")

                # Asignar el user_id a los metadatos del cliente de Stripe
                stripe.Customer.modify(
                    customer.id,  # Usamos el ID del cliente actual
                    metadata={"user_id": str(new_user.id)}
                )
            else:
                print(f" Error al registrar usuario: Email duplicado o fallo DB.")

    return {"status": "success"}
