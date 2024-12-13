import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Card, Account
from datetime import datetime

@csrf_exempt
@api_view(['POST'])
def check_user(request):
    # queries the database to check whether user has sufficient funds
    data = json.loads(request.body)
    card_number = data.get('card_number')
    cvv = data.get('cvv')
    expiry_date = data.get('expiry_date')
    name = data.get('name')
    amount = data.get('amount')
    print('At the Bank Server: ' + name)

    cards = Card.objects.filter(cvv=cvv, expiry_date = expiry_date, card_number = card_number)
    print(cards)
    if cards:
        print('This user is legit! Verfied User!')
        for card in cards:
            if card.status == 'active':
                balance = card.account.account_balance
                print(balance)
                if(float(amount) > balance):
                    print("You can't donate this amount! Insufficent balance!")
                    return JsonResponse({'message': 'Insufficent balance!'}, status = 400)
            else:
                print("Your card is not active!")
                return JsonResponse({'message': 'Inactive Card! Either blocked or expired!'}, status = 400)
            message = 'Verfied User!'
            status = 200
    else:
        print('Card details could not be verified!')
        message = 'Unverified User!'
        status = 400

    return JsonResponse({'message': message}, status = status)
    
@csrf_exempt
@api_view(['POST'])
def check_ngo(request):
    # checks the database to check whether ngo has sufficient funds
    data = json.loads(request.body)
    account_number = data.get('account_number')
    print('Recieved Bank details: Account Number is: ' + account_number)
    ngo_account = Account.objects.get(account_number=account_number)
    if not ngo_account:
        return JsonResponse({'message': 'Account for the NGO does not exists in the bank'}, status = 400)
    if ngo_account.account_status != 'active':
        return JsonResponse({'message': 'NGO Bank account cannot currently recieve money!'}, status = 400)
    return JsonResponse({'message': 'NGO Account can actively recieve money!'}, status = 200)
    

@csrf_exempt
@api_view(['POST'])
def make_transactions(request):
    # makes the actual additions and deductions.
    data = json.loads(request.body)
    card_number = data.get('card_number')
    cvv = data.get('cvv')
    expiry_date = data.get('expiry_date')
    user_name = data.get('user_name')
    amount = data.get('amount')
    ngo_account_number = data.get('ngo_account_number')
    
    cards = Card.objects.filter(cvv=cvv, expiry_date = expiry_date, card_number = card_number)
    print(cards)
    for card in cards:
        user_account_number = card.account.account_number
    print(user_account_number)

    user_account = Account.objects.filter(account_number=user_account_number).first()  # safer than [0]
    print(user_account)


    ngo_account = Account.objects.get(account_number = ngo_account_number)
    print(ngo_account)

    #actual money transfer goes here

    user_account.account_balance = float(user_account.account_balance) - float(amount)
    ngo_account.account_balance = float(ngo_account.account_balance) + float(amount)

    user_account.save()
    ngo_account.save()

    return JsonResponse({'message': 'Transaction Completed', 'user_balance' : user_account.account_balance}, status = 200)


import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from django.conf import settings


def load_public_key():
    # Read publickeys.json
    with open('publickeys.json', 'r') as f:
        keys_data = json.load(f)
    
    # Choose the public key (keypair_1, keypair_2, etc.)
    public_key_str = keys_data.get("payment processor")
    
    # Load the public key into an object
    public_key = serialization.load_pem_public_key(public_key_str.encode('utf-8'))

    print(public_key)
    return public_key


def encrypt_message(message, public_key):
    # Encrypt the message using RSA and the public key
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    print(encrypted)
    return encrypted
