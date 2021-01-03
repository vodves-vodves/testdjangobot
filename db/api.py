import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from db.settings import TOKEN
from db.settings import admins

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


def admin(user_id):
    items = (
        "Добавить специальность|g", "Удалить специальность|r", "line", "Добавить группу|g", "Удалить группу|r", "line",
        "Включить каждодневное напоминание|g", "Выключить каждодневное напоминание|r")
    keyboard = generate_keyboard(items)
    message = "Меню управления ботом: "
    send_message(user_id, message, keyboard=keyboard)


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


def select_method(data, user_id):
    body = data["object"]["message"]["text"].lower()
    if body == "отправить":
        send_message(user_id, "Привет")
    elif body == "админ":
        if user_id in admins:
            admin(user_id)
    else:
        send_message(user_id, "Главное меню", keyboard=main_menu())
