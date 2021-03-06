import vk_api
import datetime
import xlsxwriter
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from db.settings import TOKEN
from db.settings import admins
from vkbot.models import Specialization, Group, Users, BlackList

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
    for group in groups:
        if group.specialnost == speci:
            if line_counter == 2:
                items.append("line")
                line_counter = 0
            items.append(group.name)
            line_counter += 1
    items.append("line")
    items.append("Главное меню|b")
    keyboard = generate_keyboard(items)
    message = "Пожалуйста, выберите номер группы: "
    send_message(user_id, message, keyboard=keyboard)


def get_group(user_id, group):
    user = Users.objects.get(vk_id=user_id)
    groupi = Group.objects.get(name=group)
    user.group = groupi
    user.save()

    items = ("главное меню|b",)
    keyboard = generate_keyboard(items)
    message = "Введите данные, которые вы хотите отправить. \n"
    message += "Например, !0-1-3-0-0-0.\n"
    message += "Восклицательный знак '!' перед вашим сообщение ОБЯЗАТЕЛЬНО.\n"
    send_message(user_id, message, keyboard=keyboard)


def send_info(user_id, message):
    info = message.split("!")[1]
    user = Users.objects.get(vk_id=user_id)
    group = str(user.specialization) + '-' + str(user.group)
    message_send = f"Имя и фамилия: {str(user.name)}\n"
    message_send += f"Группа: {str(group)}\n"
    message_send += f"Сообщение: {info}\n"

    now_day = datetime.date.today().day
    user.send_date = str(now_day)
    user.send_message = message_send
    user.send_info = info
    user.save()

    for admin in admins:
        send_message(admin, message_send, keyboard=main_menu_admin())
    send_message(user_id, "Информация успешно отправлена!", keyboard=main_menu())


def get_id(message):  # Узнать ид
    user_id = message.split('https://vk.com/')
    text = vk_session.method('users.get', {
        'user_ids': user_id[1],
        'name_case': 'Nom',
    })
    return text[0].get('id')


def add_group(group, user_id):
    name = group.split("ga")
    try:
        name_spec = name[1].split("-")
        speci = Specialization.objects.get_or_create(name=name_spec[0])
        spec = Specialization.objects.get(name=name_spec[0])
        group = Group.objects.get_or_create(name=name_spec[1], specialnost=spec)
        send_message(user_id, "Группа добавлена!", keyboard=main_menu_admin())
    except Exception as e:
        for admin in admins:
            send_message(admin, f"Не удалось добавить группу: {e}", keyboard=main_menu_admin())


def del_group(group, user_id):
    name = group.split("gd")
    try:
        name_spec = name[1].split("-")
        group = Group.objects.get(name=name_spec[1])
        group.delete()
        send_message(user_id, "Группа успешно удалена!", keyboard=main_menu_admin())
    except Exception as e:
        for admin in admins:
            send_message(admin, f"Не удалось удалить группу: {e}", keyboard=main_menu_admin())


def del_starosta(vk_id, user_id):
    try:
        id_starosta = vk_id.split('del')
        starosta = Users.objects.get(vk_id=id_starosta[1])
        starosta.delete()
        send_message(user_id, "Староста успешно удален!", keyboard=main_menu_admin())
    except Exception as e:
        for admin in admins:
            send_message(admin, f"Не удалось удалить старосту: {e}", keyboard=main_menu_admin())


def add_starosta(vk_id, user_id):
    try:
        id_starosta = vk_id.split('add')  # Здесь мы получаем запись типа add3453453
        text = vk_session.method('users.get', {
            'user_ids': id_starosta,
            'name_case': 'Nom',
        })
        firstname = text[0].get('first_name')
        lastname = text[0].get('last_name')
        name = firstname + ' ' + lastname
        starosta = Users.objects.create(vk_id=id_starosta[1], name=name)
        starosta.save()
        send_message(user_id, "Староста успешно добавлен!", keyboard=main_menu_admin())
    except Exception as e:
        for admin in admins:
            send_message(admin, f"Не удалось добавить старосту: {e}", keyboard=main_menu_admin())


def mailing():
    ids = [i.vk_id for i in Users.objects.all()]
    for i in ids:
        try:
            send_message(i, "Не забудьте отправить данные об отсутствющих студентов", keyboard=main_menu())
        except:
            continue
    for i in admins:
        send_message(i, "Напоминание студентам успешно отправлено!", keyboard=main_menu_admin())


def check_send_message():  # проверяем отправил ли староста сообщение
    users = [user for user in Users.objects.all()]
    for user in users:
        try:
            now_day = datetime.date.today().day
            if user.send_date != str(now_day):
                blacklist = BlackList.objects.create(vk_id=user.vk_id)
                blacklist.save()
        except:
            continue


def send_checked_message_admin():
    check_send_message()
    blacklist_users = [user for user in BlackList.objects.all()]
    if blacklist_users:  # не пустой
        message = "Сегодня не отправили сообщения:\n"
        for blacklist_user in blacklist_users:
            try:
                user = Users.objects.get(vk_id=blacklist_user.vk_id)
                message += f"{user.name} - https://vk.com/id{user.vk_id}\n"
            except:
                continue
        for i in admins:
            send_message(i, message, keyboard=main_menu_admin())
        BlackList.objects.all().delete()
    else:
        for i in admins:
            send_message(i, "Сегодня все отправили сообщения!", keyboard=main_menu_admin())


def add_excel():
    users = [user for user in Users.objects.all()]
    now_day = datetime.date.today()
    orz = 0
    covid = 0
    pnevmonia = 0
    yv_prich = 0
    ne_yv_prich = 0
    po_prikazy = 0
    for user in users:
        if user.send_date == now_day:
            user_send_info = user.send_info
            orz += int(user_send_info.split('-')[0])
            covid += int(user_send_info.split('-')[1])
            pnevmonia += int(user_send_info.split('-')[2])
            yv_prich += int(user_send_info.split('-')[3])
            ne_yv_prich += int(user_send_info.split('-')[4])
            po_prikazy += int(user_send_info.split('-')[5])

    workbook = xlsxwriter.Workbook(f'{now_day}.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('B1', f'{now_day}')

    worksheet.write('A2', 'ОРЗ')
    worksheet.write('A3', 'Ковид')
    worksheet.write('A4', 'Пневмония')
    worksheet.write('A5', 'По не ув. пр.')
    worksheet.write('A6', 'По ув. пр.')
    worksheet.write('A7', 'По приказу')

    worksheet.write('B2', f'{orz}')
    worksheet.write('B3', f'{covid}')
    worksheet.write('B4', f'{pnevmonia}')
    worksheet.write('B5', f'{yv_prich}')
    worksheet.write('B6', f'{ne_yv_prich}')
    worksheet.write('B7', f'{po_prikazy}')

    workbook.close()


def admin(user_id):
    items = (
        "Добавить старосту|g", "Удалить старосту|r", "line",
        "Добавить группу|g", "Удалить группу|r", "line",
        "Узнать ид|g",
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
    elif body.startswith('!'):
        send_info(user_id, body)
    elif body == "добавить старосту":
        if user_id in admins:
            send_message(user_id, "Введите id (Например, add12345678)")
    elif body.startswith('add'):
        if user_id in admins:
            add_starosta(body, user_id)
    elif body == "удалить старосту":
        if user_id in admins:
            send_message(user_id, "Введите id (Например, del12345678)")
    elif body.startswith('del'):
        if user_id in admins:
            del_starosta(body, user_id)
    elif body == "добавить группу":
        if user_id in admins:
            send_message(user_id, "Введите название (Например, gaПКС-407)")
    elif body.startswith('ga'):
        if user_id in admins:
            add_group(body, user_id)
    elif body == "удалить группу":
        if user_id in admins:
            send_message(user_id, "Введите название (Например, gdПКС-407)")
    elif body.startswith('gd'):
        if user_id in admins:
            del_group(body, user_id)
    elif body == "начать рассылку":
        if user_id in admins:
            mailing()
    elif body == "узнать ид":
        if user_id in admins:
            send_message(user_id, 'Введите ссылку на профиль:')
    elif body.startswith('https://vk.com/'):
        if user_id in admins:
            send_message(user_id, get_id(body), keyboard=main_menu_admin())
    elif spec in [i.name for i in Specialization.objects.all()]:
        get_spec(user_id, spec)
    elif group in [i.name for i in Group.objects.all()]:
        get_group(user_id, group)
    else:
        if user_id in admins:
            send_message(user_id, "Главное меню", keyboard=main_menu_admin())
        else:
            send_message(user_id, "Главное меню", keyboard=main_menu())


def main_menu():
    items = ("Отправить|g", "line", "Главное меню|b")
    keyboard = generate_keyboard(items)
    return keyboard


def main_menu_admin():
    items = ("Начать рассылку|g", "line", "Админ|r", "line", "Главное меню|b")
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
