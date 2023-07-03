from abc import ABC, abstractmethod
from .tasks import send_email_with_match
from meeting.settings import EMAIL_HOST_USER


class CommonMessage(ABC):
    """Абстрактный класс шаблонов Email сообщений"""

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def __str__(self): ...

    @abstractmethod
    def get_subject(self): ...


class CommonMatchMessage(CommonMessage):
    """Класс сообщения о симпатии"""

    SUBJECT = 'User liked you!'

    def __init__(self, client_first_name: str, client_email: str):
        self.client_first_name = client_first_name
        self.client_email = client_email

    def __str__(self):
        return f"Вы понравились {self.client_first_name}! Почта участника: {self.client_email}"

    def get_subject(self):
        return self.SUBJECT


class EmailMessage:
    FROM_EMAIL = EMAIL_HOST_USER

    def __init__(self, message_recipient: str,
                 message_object: CommonMessage = None,
                 message_text: str = None,
                 subject: str = None):
        self.subject = subject
        self.message_recipient = (message_recipient,)
        self.message_text = str(message_text)
        if CommonMessage:
            self.__parse_message_object(message_object)

    def send(self) -> None:
        # Отправка сообщения с помощью celery
        print('ok')
        send_email_with_match.delay(subject=self.subject,
                                    message_text=self.message_text,
                                    from_email=self.FROM_EMAIL,
                                    recipient_list=self.message_recipient)

    def __parse_message_object(self, message_object: CommonMessage) -> None:
        """Функция парсит объект CommonMessage"""

        self.subject = message_object.get_subject()
        self.message_text = str(message_object)


def send_all_mails(messages: list[EmailMessage] | tuple[EmailMessage]) -> None:
    """Функция итерируется по списку с объектами Emailmessage и вызывает метод send()"""

    for message in messages:
        message.send()
