import os
import sys
import stripe
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configura o Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def test_create_checkout_session():
    """Testa a criação de uma sessão de checkout."""
    try:
        # Cria uma sessão de checkout
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": os.getenv("STRIPE_PRICE_ID_MONTHLY"),
                "quantity": 1,
            }],
            mode="subscription",
            success_url="http://localhost:3000/payment/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:3000/payment/cancel",
        )

        print("Sessão de checkout criada com sucesso!")
        print(f"URL: {session.url}")
        print(f"ID: {session.id}")

    except Exception as e:
        print(f"Erro ao criar sessão de checkout: {str(e)}")


def test_webhook():
    """Testa a verificação de assinatura do webhook."""
    try:
        # Simula um payload de webhook
        payload = b'{"type": "checkout.session.completed", "data": {"object": {"id": "test"}}}'
        signature = "test_signature"

        # Tenta verificar a assinatura
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )

        print("Webhook verificado com sucesso!")
        print(f"Tipo do evento: {event.type}")

    except stripe.error.SignatureVerificationError:
        print("Erro: Assinatura do webhook inválida")
    except Exception as e:
        print(f"Erro ao verificar webhook: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test_stripe.py [checkout|webhook]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "checkout":
        test_create_checkout_session()
    elif command == "webhook":
        test_webhook()
    else:
        print("Comando inválido. Use 'checkout' ou 'webhook'")
