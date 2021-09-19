from constants import dateFormat, timeFormat

reply_unreg_user0 = "Привет!\n" \
                    "Как тебя зовут?\n"

reply_settings_change_name = "Хорошо!\n" \
                             "Как тебя зовут теперь?\n"

empty_msg = "хмех"
error_msg = "Упс бот словил неожиданный эксепшн! Сорян"
reply_already_admin = "Друг, так ты ж уже админ\nТочнее, уже нет"

help_note = "Привет!\nЭтот бот позволит оставаться в курсе ближайших событий и поможет регистрироваться на них!" \
            "\n\nБоту доступны следующие команды:\n" \
            "/start - начать работу\n" \
            "/menu - если ты потерялся, эта команда вызовет основное меню опций\n" \
            "/admin - если ты по счастливой случайности оказался членом нашей тимы " \
            "с помощью этой команды можно стать мэйкером ивентов!\n\n" \
            "Увидимся! ⛈💘🥰 "

reply_choose_command = "Выберите одну из возможных опций"
reply_reg_FIO = "Как тебя зовут?"
reply_main_options = "В общем опции: "
reply_event_markup = "{}\nКогда: {} {}\nКак долго: {}\nПроводит: {}\n{}\n"
reply_nothing_found = "Кажись ничего не будет!"
reply_choose_day_of_the_week = "Выбери кнопочкой день недели чтобы посмотреть что будет!"
reply_empty_week = "Кажись мы ничего не планируем на ближайшие 7 дней, залетай попозже"

# Запись на ивент
reply_event_choosing_part = "Хочу сюда: "
reply_choose_event = "Крутяк! Записаться можно на неделю вперед, выбери куда ты хочешь из списка ниже:"
reply_success_registration = "Шикарный выбор! Записали тебя на {}!\nУвидимся там елки-палки 😉"
inline_reg_button_text = "{} {}"
reply_already_reged = "Воу! Ты кажется уже сюда зареган!"

# Отмена реги
reply_guest_reged_events_offer = "Вы сейчас зарегестрированы на следующие ивенты: "
reply_choose_event_to_cancel = "Ты сейчас зарегестрирован на вот эти ивенты. На какой из них решил не идти?"
reply_event_cancel_choosing_part = "Я не пойду сюда: "
reply_success_unregistration = "Эх! Отменили твою запись на {}!\nУвидимся в другой раз"
reply_unsuccess_unregistration = "Странно, кажется не получилось отменить регестрацию"
reply_no_hay_events_to_cancel = "А ты еще не регестрировался ни на один ивент!"

# админ
reply_admin_password = "Чтобы стать админом надо знать особое слово...\n" \
                       "Знаешь его?"
reply_admin_change_succ = "Вау...ты теперь админ еклм! \U0001f604\nПри повторном вызове команды статус админа " \
                          "превратится в тыкву! "
reply_admin_change_denied = "Не тот пассворд..🙀🙎"

# админ
reply_choose_stat_to_show = "Выбери что-то из доступного"
reply_choose_months_to_show_stats = "Выбери месяц чтобы посмотреть статистику"
reply_event_markup_advanced = "№: {}\nНазвание: {}\nДата: {}\nВремя: {}\nПроводит: {}\nСтатус: {}\nОписание: {}\n"

reply_stats = "Статистика по ивентам:\nНазвание|Зарегестрированные|Отменившие\n"
reply_stats_row = "{:10}    👌{:5}    🚫{:5}\n"
reply_no_stat_for_month = "За этот месяц нет ивентов!"
reply_del = "\n--------\n"
reply_event_add_remind = "Круть! Напоминаю, пришли ивент в формате:"
reply_event_add = "Название: 🤤 мой ивент!\nДата: {}\nВремя: {}\n" \
                  "Проводит: @daniil_toro\nКак долго: сколько времени?\nОписание: что-нить\n".format(dateFormat, timeFormat)
reply_event_edit_part = "✏"
reply_event_edit = "Вот ближайшие ивенты:"
reply_event_edit1 = "Пришли ивент в том же формате, что и выше, но замени необходимое"
reply_event_succ_upd = "Оки! Обновили"
reply_event_unsucc_upd = "Почему-то не получилось обновить ивент"
