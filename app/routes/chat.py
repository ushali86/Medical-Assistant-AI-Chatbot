from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ChatMessage
from .auth import get_current_user

from ..services.ai_service import get_ai_response


router = APIRouter(
    prefix="/chat",
    tags=["Medical Chat"]
)



def check_emergency(message):

    words = [
        "chest pain",
        "heart attack",
        "breathing problem",
        "can't breathe",
        "unconscious",
        "severe bleeding",
        "बेहोश",
        "सांस नहीं"
    ]


    text = message.lower()


    for word in words:
        if word in text:
            return True

    return False



@router.post("/send")
def send_message(
    message: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):


    if check_emergency(message):

        ai_response = (
            "⚠️ Emergency warning: "
            "Please contact emergency services or visit a doctor immediately."
        )


    else:

        ai_response = get_ai_response(message)



    chat = ChatMessage(

        user_id=current_user["user_id"],

        user_message=message,

        ai_response=ai_response

    )


    db.add(chat)

    db.commit()

    db.refresh(chat)



    return {

        "success": True,

        "message": message,

        "response": ai_response

    }




@router.get("/history")
def history(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    chats = db.query(ChatMessage).filter(

        ChatMessage.user_id ==
        current_user["user_id"]

    ).all()


    return chats