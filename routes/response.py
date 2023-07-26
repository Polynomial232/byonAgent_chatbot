""" docstring """

from fastapi import APIRouter

from handlers.reponse import *

router = APIRouter()

@router.get('/response')
async def get_response(message, sender, receiver):
    """ docstring """
    
    return get_response_handler(message, sender, receiver)