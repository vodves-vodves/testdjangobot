import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from db.settings import TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


def select_method(data, user_id):
    body = data["object"]["body"].lower()
    if body == "отправить":
        send_message(user_id, "Привет")
    else:
        send_message(user_id, "главное меню", keyboard=main_menu())


def main_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(f"Отправить сообщение", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    return keyboard.get_keyboard()


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
            print(current_title, current_color)

            for key, item in colors.items():
                if key == current_color:
                    current_color = item

            keyboard.add_button(current_title, color=current_color)
    return keyboard.get_keyboard()
