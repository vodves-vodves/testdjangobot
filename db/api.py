import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from db.settings import TOKEN
from db.settings import admins
from vkbot.models import Specialization, Group, Users

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


def user_info(user_id):
    line_counter = 0
    items = []
    specialnost = Specialization.objects.all()  # Получаем список специальностей из БД
    for specializ in specialnost:
        if line_counter == 2:  # Для разделения кнопок - line
            items.append("line")
            line_counter = 0
        items.append(specializ.name)  # Добавляем специальность в лист
        line_counter += 1
    items.append("line")
    items.append("Главное меню|b")
    keyboard = generate_keyboard(items)
    message = "Пожалуйста, выберите вашу специальность: "
    send_message(user_id, message, keyboard=keyboard)


def get_spec(user_id, spec):
    user = Users.objects.get(vk_id=user_id)
    speci = Specialization.objects.get(name=spec)
    user.specialization = speci
    user.save()
    line_counter = 0
    items = []
    groups = Group.objects.all()
    print(groups)
    for group in groups:
        print(group)
        if line_counter == 2:
            items.append("line")
            line_counter = 0
        if group.specialnost == spec:
            items.append(group.name)
        line_counter += 1
    items.append("line")
    items.append("Главное меню|b")
    keyboard = generate_keyboard(items)
    message = "Пожалуйста, выберите номер группы: "
    send_message(user_id, message, keyboard=keyboard)


def get_group(user_id, group, spec):
    user = Users.objects.get(vk_id=user_id)
    groupi = Group.objects.get(name=group)
    user.group = groupi
    user.save()

    items = ("главное меню|b",)
    keyboard = generate_keyboard(items)
    message = "Пожалуйста, введите данные: "
    send_message(user_id, message, keyboard=keyboard)


def get_id(message):  # Узнать ид
    user_id = message.split('https://vk.com/')
    text = vk_session.method('users.get', {
        'user_ids': user_id[1],
        'name_case': 'Nom',
    })
    return text[0].get('id')


def add_spec(spec, user_id):
    pass


def del_spec(spec, user_id):
    pass


def add_group(group, user_id):
    pass


def del_group(group, user_id):
    pass


def del_starosta(vk_id, user_id):
    try:
        id_starosta = vk_id.split('del')
        starosta = Users.objects.get(vk_id=id_starosta[1])
        starosta.delete()
        send_message(user_id, "Староста успешно удален!", keyboard=main_menu())
    except Exception as e:
        for admin in admins:
            send_message(admin, f"Не удалось удалить старосту: {e}")


def add_starosta(vk_id, user_id):
    try:
        id_starosta = vk_id.split('add')  # Здесь мы получаем запись типа add3453453
        starosta = Users.objects.create(vk_id=id_starosta[1])
        starosta.save()
        send_message(user_id, "Староста успешно добавлен!", keyboard=main_menu())
    except Exception as e:
        for admin in admins:
            send_message(admin, f"Не удалось добавить старосту: {e}")


def admin(user_id):
    items = (
        "Добавить старосту|g", "Удалить старосту|r", "line", "Добавить специальность|g", "Удалить специальность|r",
        "line", "Добавить группу|g", "Удалить группу|r", "line",
        "Включить каждодневное напоминание|g", "line", "Выключить каждодневное напоминание|r", "line", "Узнать ид|g",
        "line", "Главное меню|b")
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
    elif body == "добавить старосту":
        if user_id in admins:
            send_message(user_id, "Введите его id (Например, add12345678)")
    elif body.startswith('add'):
        if user_id in admins:
            add_starosta(body, user_id)
    elif body == "удалить старосту":
        if user_id in admins:
            send_message(user_id, "Введите его id (Например, del12345678)")
    elif body.startswith('del'):
        if user_id in admins:
            del_starosta(body, user_id)
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
    elif body == "узнать ид":
        if user_id in admins:
            send_message(user_id, 'Введите ссылку на профиль:')
    elif body.startswith('https://vk.com/'):
        if user_id in admins:
            send_message(user_id, f"Его id: {get_id(body)}")
    elif spec in [i.name for i in Specialization.objects.all()]:
        get_spec(user_id, spec)
    elif group in [i.name for i in Group.objects.all()]:
        get_group(user_id, group)
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
