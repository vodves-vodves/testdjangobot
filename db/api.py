import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from db.settings import TOKEN
from db.settings import admins
from vkbot.models import Specialization, Group

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


def user_info(user_id):
    line_counter = 0
    items = []
    specialnost = Specialization.objects.all()
    for specializ in specialnost:
        if line_counter == 2:
            items.append("line")
            line_counter = 0
        items.append(specializ)
    items.append("line")
    items.append("главное меню|b")
    keyboard = generate_keyboard(items)
    message = "Пожалуйста, выберите вашу специальность: "
    send_message(user_id, message, keyboard=keyboard)


def get_spec(user_id, spec):
    pass


def admin(user_id):
    items = (
        "Добавить специальность|g", "Удалить специальность|r", "line", "Добавить группу|g", "Удалить группу|r", "line",
        "Включить каждодневное напоминание|g", "line", "Выключить каждодневное напоминание|r", "line", "Узнать Id")
    keyboard = generate_keyboard(items)
    message = "Меню управления ботом: "
    send_message(user_id, message, keyboard=keyboard)


def select_method(data, user_id):
    spec = data["object"]["message"]["text"]
    group = data["object"]["message"]["text"]
    body = data["object"]["message"]["text"].lower()
    if body == "отправить":
        user_info(user_id)
    elif body == "админ":
        if user_id in admins:
            admin(user_id)
    elif body == "добавить специальность":
        if user_id in admins:
            pass
    elif body == "удалить специальность":
        if user_id in admins:
            pass
    elif body == "добавить группу":
        if user_id in admins:
            pass
    elif body == "удалить группу":
        if user_id in admins:
            pass
    elif body == "включить каждодневное напоминание":
        if user_id in admins:
            pass
    elif body == "выключить каждодневное напоминание":
        if user_id in admins:
            pass
    elif body == "узнать Id":
        if user_id in admins:
            pass
    elif body == "выбрать специальность":
        pass
    elif body == "выбрать номер группы":
        pass
    else:
        send_message(user_id, "Главное меню", keyboard=main_menu())


def main_menu():
    items = ("Отправить|g", "line", "Помощь|r", "Главное меню|b")
    keyboard = generate_keyboard(items)
    return keyboard


def send_message(user_id, message, attachment=None, keyboard=None):
    vk.messages.send(user_id=str(user_id),
                     message=message,
                     attachment=attachment,
                     keyboard=keyboard,
                     random_id=get_random_id())


def generate_keyboard(items):
    keyboard = VkKeyboard(one_time=True)
    for title in items:
        if title == "line":
            keyboard.add_line()
        else:
            try:
                current_title = title.split("|")[0]
                current_color = title.split("|")[1]
            except IndexError:
                current_color = VkKeyboardColor.SECONDARY
            colors = {
                "r": VkKeyboardColor.NEGATIVE,
                "b": VkKeyboardColor.PRIMARY,
                "g": VkKeyboardColor.POSITIVE
            }
            # (current_title, current_color)

            for key, item in colors.items():
                if key == current_color:
                    current_color = item

            keyboard.add_button(current_title, color=current_color)
    return keyboard.get_keyboard()
