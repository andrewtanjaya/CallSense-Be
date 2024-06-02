from pydantic import BaseModel


class GetChatbotGeneratedAnswerModel(BaseModel):
    question: str
    answer: str

    class Config:
        schema_extra = {
            "example": {
                "question": "How are you?",
                "answer": "I am fine",
            }
        }
