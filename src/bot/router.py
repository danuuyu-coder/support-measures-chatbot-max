from maxapi import Router, F
from maxapi.context import StatesGroup, State, MemoryContext
from maxapi.filters.command import Command
from maxapi.types import MessageCreated, BotStarted, DialogCleared, MessageCallback, Message

from src.bot.ui import (
    start_keyboard,
    cancel_region,
    cancel_measure,
    regions_keyboard,
    geo_keyboard,
    region_keyboard,
    main_menu_keyboard,
    measures_keyboard,
    search_keyboard,
    benefit_keyboard,
    benefits_manual_search_keyboard,
    benefits_pagination_search_keyboard,
    messages
)

from src.models import User, Services, Payload

class States(StatesGroup):
    waiting_region = State()
    input_region = State()
    main_menu = State()
    waiting_measure = State()
    waiting_search = State()
    waiting_benefit = State()
    benefit_description = State()


def create_router():
    router = Router()


    @router.bot_started()  # Запуск пользователем бота (без команд)
    async def on_start(event: BotStarted):
        keyboard = await start_keyboard()
        await event.bot.send_message(
            chat_id=event.chat_id,
            text=messages.start(),
            attachments=[keyboard])


    @router.dialog_removed()  # Очистка + остановка бота
    async def on_stop(event: DialogCleared, services: Services):
        user_id = event.user.user_id
        await services.user_service.remove(user_id)


    @router.message_callback(Payload.filter(F.foo == 'start'))
    @router.message_created(Command(['start', 'menu']))  # Отработка команд
    async def on_start(event: MessageCreated | MessageCallback, context: MemoryContext, services: Services):
        user_id = event.from_user.user_id
        user = await services.user_service.get_one(user_id)
        if not user:
            await on_choose_region(event, services, context)
        else:
            await on_main_menu(event, context)


    @router.message_callback(Payload.filter(F.foo == 'return_to_menu'))
    async def on_main_menu(event: MessageCallback | Message,
                           context: MemoryContext):  # Message - когда вызов корутины, MessageCallback - вызов по кнопке
        await context.clear()
        keyboard = await main_menu_keyboard()
        if isinstance(event, MessageCallback):
            await event.answer()
            await event.message.edit(messages.main_menu(), attachments=[keyboard])
        else:
            await event.message.answer(messages.main_menu(), attachments=[keyboard])


    @router.message_callback(Payload.filter(F.foo.in_(['change_region', 'cancel_region'])))  # Нажатие кнопки "Изменить регион"
    @router.message_created(Command('choose_region'))  # Начало регистрации (либо изменение региона)
    async def on_choose_region(event: MessageCreated | MessageCallback, services: Services, context: MemoryContext):
        # MessageCreated - вызов по команде, MessageCallback - вызов по кнопке
        keyboard = await region_keyboard()
        if isinstance(event, MessageCallback):
            await event.message.edit(messages.type_choice_region(), attachments=[keyboard])
        else:
            await event.message.answer(messages.type_choice_region(), attachments=[keyboard])
        await context.set_state(States.waiting_region)


    @router.message_created(F.message.body.attachments, States.waiting_region)  # F.message.body.attachments ловит LOCATION
    async def on_catch_region_by_geo(event: MessageCreated, services: Services, context: MemoryContext):
        location = event.message.body.attachments
        latitude = location[0].latitude  # ширина
        longitude = location[0].longitude  # долгота
        try:
            region, country = await services.geo_service.parse(longitude, latitude)
        except:
            keyboard = await geo_keyboard()
            await event.message.answer(messages.geocode_error(),
                                       attachments=[keyboard])
        else:
            if country == 'Россия':
                await context.clear()
                user_id = event.from_user.user_id
                okato = (await services.region_service.get_one(region)).okato
                user = User(user_id=user_id, okato=okato)
                await services.user_service.insert(user)  # добавление в таблицу

                keyboard = await main_menu_keyboard()
                await event.message.answer(messages.region_success(region))
                await event.message.answer(messages.main_menu(), attachments=[keyboard])
            else:
                keyboard = await geo_keyboard()
                await event.message.answer(messages.geocode_no_russia(),
                                           attachments=[keyboard])

    @router.message_callback(Payload.filter(F.foo == 'region_input'), States.waiting_region)
    async def on_region_input(event: MessageCallback, context: MemoryContext):
        await context.set_state(States.input_region)
        keyboard = await cancel_region()
        await event.message.edit(messages.region_input(), attachments=[keyboard])

    @router.message_created(F.message.body.text, States.input_region)
    async def on_waiting_region(event: MessageCreated, services: Services, context: MemoryContext):
        part_of_region = event.message.body.text
        regions = await services.region_service.get_all()

        cancel_keyboard = await cancel_region()
        matched_regions = []
        for region in regions:
            if part_of_region.lower() in region.name.lower():
                matched_regions.append(region)

        if len(matched_regions) == 0:
            matched_regions = await services.giga_service.recognize_region(part_of_region)

        if len(matched_regions) == 0:
            await event.message.answer(messages.region_not_found(), attachments=[cancel_keyboard])
        elif len(matched_regions) == 1:
            await context.clear()
            region = matched_regions[0]
            user_id = event.from_user.user_id
            okato = (await services.region_service.get_one(region.name)).okato
            user = User(user_id=user_id, okato=okato)
            await services.user_service.insert(user)  # добавление в таблицу

            keyboard = await main_menu_keyboard()
            await event.message.answer(messages.region_success(region.name))
            await event.message.answer(messages.main_menu(), attachments=[keyboard])
        elif 1 < len(matched_regions) <= 30:  # The number of buttons on the keyboard cannot be more than 30
            keyboard = await regions_keyboard(matched_regions)
            await event.message.answer(messages.region_list(len(matched_regions)), attachments=[keyboard])
            await context.set_state(States.main_menu)
        else:
            await event.message.answer(messages.region_many(len(matched_regions)), attachments=[cancel_keyboard])


    @router.message_callback(Payload.filter(F.foo.startswith('region_')), States.main_menu)
    async def on_catch_region_by_button(event: MessageCallback, services: Services, context: MemoryContext, payload: Payload):
        await context.clear()
        region_name = payload.foo.replace('region_', '')
        user_id = event.from_user.user_id
        okato = (await services.region_service.get_one(region_name)).okato
        user = User(user_id=user_id, okato=okato)
        await services.user_service.insert(user)  # добавление в таблицу

        await event.message.edit(messages.region_success(region_name))
        keyboard = await main_menu_keyboard()
        await event.message.answer(messages.main_menu(), attachments=[keyboard])


    @router.message_callback(Payload.filter(F.foo.in_(['category_measure', 'return_to_measures'])))
    async def on_choose_category_measure(event: MessageCallback, context: MemoryContext):
        await context.clear()  # если нажали "Назад"
        keyboard = await measures_keyboard()
        await event.message.edit(messages.choose_measure(), attachments=[keyboard])
        await context.set_state(States.waiting_measure)


    @router.message_callback(Payload.filter(F.foo.in_(['return_to_search', 'cancel_measure'])))
    @router.message_callback(Payload.filter(F.foo.in_(['measure_fzo', 'measure_millitary'])), States.waiting_measure)
    async def on_choose_search(event: MessageCallback, context: MemoryContext, payload: Payload):
        if payload.foo != 'return_to_search':
            measure = payload.foo
            await context.update_data(waiting_measure=measure)
        keyboard = await search_keyboard()
        await event.message.edit(messages.choose_search(), attachments=[keyboard])
        await context.set_state(States.waiting_search)


    @router.message_callback(Payload.filter(F.foo == 'manual_search'), States.waiting_search)
    async def on_choose_manual_search(event: MessageCallback, context: MemoryContext):
        keyboard = await cancel_measure()
        await event.message.edit(messages.benefit_input(), attachments=[keyboard])
        await context.set_state(States.waiting_benefit)


    @router.message_callback(Payload.filter(F.foo == 'return_to_benefit_search'))
    @router.message_created(F.message.body.text, States.waiting_benefit)
    async def on_waiting_benefit(event: MessageCreated | MessageCallback, context: MemoryContext, services: Services):
        if isinstance(event, MessageCallback):
            part_of_benefit = (await context.get_data())['waiting_benefit']
        else:
            part_of_benefit = event.message.body.text
            await context.update_data(waiting_benefit=part_of_benefit)
        user_id = event.from_user.user_id
        user_okato = (await services.user_service.get_one(user_id)).okato
        measure_category = (await context.get_data())['waiting_measure']
        if measure_category == 'measure_fzo':
            benefits = await services.measure_service.get_all(okato=user_okato)
        else:
            benefits = await services.measure_service.get_all_military(okato=user_okato)

        matched_benefits = []
        for benefit in benefits:
            if part_of_benefit.lower() in benefit.name.lower():
                matched_benefits.append(benefit)

        if len(matched_benefits) == 0:
            matched_benefits = await services.giga_service.recognize_measure(user_okato, part_of_benefit)

        if len(matched_benefits) == 0:
            keyboard = await cancel_measure()
            await event.message.answer(messages.benefit_not_found(), attachments=[keyboard])
        elif len(matched_benefits) == 1:
            benefit = matched_benefits[0]
            if benefit.documents:
                summary = await services.giga_service.recognize_summary(
                    f'{benefit.name} | {benefit.duration} | {benefit.documents} | {benefit.procedure} | {benefit.result}')
                await context.update_data(summary=summary)
                answer = messages.benefit_success_with_doc(
                    benefit_name=benefit.name,
                    benefit_duration=benefit.duration,
                    benefit_documents=benefit.documents.split('~'),
                    benefit_procedure=benefit.procedure.split('~'),
                    benefit_result=benefit.result
                )
            else:
                summary = await services.giga_service.recognize_summary(
                    f'{benefit.name} | {benefit.duration} | {benefit.procedure} | {benefit.result}')
                await context.update_data(summary=summary)
                answer = messages.benefit_success_no_doc(
                    benefit_name=benefit.name,
                    benefit_duration=benefit.duration,
                    benefit_procedure=benefit.procedure.split('~'),
                    benefit_result=benefit.result
                )
            if benefit.link:
                await benefit_keyboard(1, 1, 1)
                keyboard = await benefit_keyboard(benefit.link, 'one', 'search')
            else:
                keyboard = await benefit_keyboard(None, 'one', 'search')
            await event.message.answer(answer, attachments=[keyboard])
        elif 1 < len(matched_benefits) <= 10:
            keyboard = await benefits_manual_search_keyboard(matched_benefits)
            if isinstance(event, MessageCallback):
                await event.message.edit(messages.benefit_list(matched_benefits), attachments=[keyboard])
            else:
                await event.message.answer(messages.benefit_list(matched_benefits), attachments=[keyboard])
            await context.set_state(States.benefit_description)
        else:
            keyboard = await cancel_measure()
            await event.message.answer(messages.benefit_many(len(matched_benefits)), attachments=[keyboard])


    @router.message_callback(Payload.filter(F.foo.startswith('pagination_measure_id_')), States.benefit_description)
    @router.message_callback(Payload.filter(F.foo.startswith('search_measure_id_')), States.benefit_description)
    async def on_benefit_description(event: MessageCallback, context: MemoryContext, payload: Payload, services: Services):
        # await context.clear()
        if payload.foo.startswith('pagination_'):
            measure_id = payload.foo.replace('pagination_measure_id_', '')
        else:
            measure_id = payload.foo.replace('search_measure_id_', '')
        benefit = await services.measure_service.get_one(measure_id=measure_id)

        if benefit.documents:
            summary = await services.giga_service.recognize_summary(
                f'{benefit.name} | {benefit.duration} | {benefit.documents} | {benefit.procedure} | {benefit.result}')
            await context.update_data(summary=summary)
            answer = messages.benefit_success_with_doc(
                benefit_name=benefit.name,
                benefit_duration=benefit.duration,
                benefit_documents=benefit.documents.split('~'),
                benefit_procedure=benefit.procedure.split('~'),
                benefit_result=benefit.result
            )
        else:
            summary = await services.giga_service.recognize_summary(
                f'{benefit.name} | {benefit.duration} | {benefit.procedure} | {benefit.result}')
            await context.update_data(summary=summary)
            answer = messages.benefit_success_no_doc(
                benefit_name=benefit.name,
                benefit_duration=benefit.duration,
                benefit_procedure=benefit.procedure.split('~'),
                benefit_result=benefit.result
            )
        if benefit.link:
            if payload.foo.startswith('pagination_'):
                keyboard = await benefit_keyboard(benefit.link, 'more', 'pagination')
            else:
                keyboard = await benefit_keyboard(benefit.link, 'more', 'search')
        else:
            if payload.foo.startswith('pagination_'):
                keyboard = await benefit_keyboard(None, 'more', 'pagination')
            else:
                keyboard = await benefit_keyboard(None, 'more', 'search')
        await event.message.edit(answer, attachments=[keyboard])


    @router.message_callback(Payload.filter(F.foo == 'summary'))
    async def on_show_summary(event: MessageCallback, context: MemoryContext):
        summary = (await context.get_data())['summary']
        await event.message.answer(summary)


    @router.message_callback(Payload.filter(F.foo == 'pagination_search'), States.waiting_search)
    async def on_show_benefits_list(event: MessageCallback, context: MemoryContext, services: Services, payload: Payload):
        #await context.clear()
        await context.update_data(current_page=0)
        user_id = event.from_user.user_id
        okato = (await services.user_service.get_one(user_id)).okato
        measure_category = (await context.get_data())['waiting_measure']
        if measure_category == 'measure_fzo':
            matched_benefits = await services.measure_service.get_all(okato=okato)
        else:
            matched_benefits = await services.measure_service.get_all_military(okato=okato)
        #данные для пагинации
        await context.update_data(matched_benefits=matched_benefits)
        #1-я страница
        keyboard = await benefits_pagination_search_keyboard(matched_benefits, page=0)
        
        await event.message.edit(
            messages.benefit_pagination_search_list(matched_benefits, page=0),
            attachments=[keyboard]
        ) 
        await context.set_state(States.benefit_description)
        

    @router.message_callback(Payload.filter(F.foo == 'return_to_benefit_pagination'))
    @router.message_callback(Payload.filter(F.foo.startswith('page_')))
    async def on_handle_pagination(event: MessageCallback, context: MemoryContext, payload: Payload):
        try:
            if payload.foo == 'return_to_benefit_pagination':
                page = (await context.get_data())['current_page']
            else:
                page = int(payload.foo.replace('page_', ''))
                await context.update_data(current_page=page)
            
            matched_benefits = (await context.get_data())['matched_benefits']   
            if not matched_benefits:
                await event.message.edit("❌ Данные не найдены.")
                return
            
            keyboard = await benefits_pagination_search_keyboard(matched_benefits, page)
            await event.message.edit(
                messages.benefit_pagination_search_list(matched_benefits, page),
                attachments=[keyboard]
        )       
        except Exception:
            await event.message.edit("❌ Ошибка при переключении страницы.")


    return router