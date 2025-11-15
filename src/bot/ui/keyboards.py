from typing import List

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types import CallbackButton, RequestGeoLocationButton, LinkButton

from src.models import Region, Payload


async def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(
            text='Начать',
            payload=Payload(foo='start').pack()
        )
    )
    return builder.as_markup()

async def cancel_region():
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(
            text='Отменить',
            payload=Payload(foo='cancel_region').pack()
        )
    )
    return builder.as_markup()

async def regions_keyboard(regions: List[Region]):
    builder = InlineKeyboardBuilder()
    for region in regions:
        button = CallbackButton(
            text=region.name,
            payload=Payload(foo=f'region_{region.name}').pack()
            # payload=region.okato
        )
        builder.row(button)
    return builder.as_markup()


async def region_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        RequestGeoLocationButton(
            text='Определить автоматически',
            quick=True  # возможность выбора метки на карте: True - нет, False - да
        )
    )
    builder.row(
        CallbackButton(
            text='Ввести вручную',
            payload=Payload(foo='region_input').pack()
        )
    )
    return builder.as_markup()


async def geo_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        RequestGeoLocationButton(
            text='Определить автоматически',
            quick=True  # возможность выбора метки на карте: True - нет, False - да
        )
    )
    builder.row(
        CallbackButton(
            text='Отменить',
            payload=Payload(foo='cancel_region').pack()
        )
    )
    return builder.as_markup()


async def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(
            text='Посмотреть меры поддержки',
            payload=Payload(foo='category_measure').pack()
        )
    )
    builder.row(
        CallbackButton(
            text='Изменить регион',
            payload=Payload(foo='change_region').pack()
        )
    )
    return builder.as_markup()


async def measures_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(
            text='Ветераны, инвалиды, члены семей',
            payload=Payload(foo='measure_fzo').pack()
        )
    )
    builder.row(
        CallbackButton(
            text='Военнослужащие',
            payload=Payload(foo='measure_millitary').pack()
        )
    )
    builder.row(
        CallbackButton(
            text='🔙 Назад: в Меню',
            payload=Payload(foo='return_to_menu').pack()
        )
    )
    return builder.as_markup()


async def search_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(
            text='Поиск по названию',
            payload=Payload(foo='manual_search').pack()
        ),
        CallbackButton(
            text='Просмотреть все',
            payload=Payload(foo='pagination_search').pack()
        )
    )
    builder.row(
        CallbackButton(
            text='🔙 Назад: в Меры поддержки',
            payload=Payload(foo='return_to_measures').pack()
        )
    )
    return builder.as_markup()

async def cancel_measure():
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(
            text='Отменить',
            payload=Payload(foo='cancel_measure').pack()
        )
    )
    return builder.as_markup()


async def benefit_keyboard(benefit_url, compare, benefit_type):
    builder = InlineKeyboardBuilder()
    if benefit_url:
        builder.row(
            LinkButton(
                text='Получить услугу',
                url=benefit_url
            )
        )
        builder.row(
            CallbackButton(
                text='Краткое описание',
                payload=Payload(foo='summary').pack()
            )
        )
        if compare == 'one':
            builder.row(
                CallbackButton(
                    text='🔙 Назад: в Поиск',
                    payload=Payload(foo='return_to_search').pack()
                )
            )
        else:
            builder.row(
                CallbackButton(
                    text='🔙 Назад: в Список мер поддержки',
                    payload=Payload(foo=f'return_to_benefit_{benefit_type}').pack()
                )
            )
    else:
        builder.row(
            CallbackButton(
                text='Краткое описание',
                payload=Payload(foo='summary').pack()
            )
        )
        if compare == 'one':
            builder.row(
                CallbackButton(
                    text='🔙 Назад: в Поиск',
                    payload=Payload(foo='return_to_search').pack()
                )
            )
        else:
            builder.row(
                CallbackButton(
                    text='🔙 Назад: в Список мер поддержки',
                    payload=Payload(foo=f'return_to_benefit_{benefit_type}').pack()
                )
            )
    return builder.as_markup()


async def benefits_manual_search_keyboard(matched_benefits):
    builder = InlineKeyboardBuilder()
    buttons_per_row = 7
    current_row = []

    for i, benefit in enumerate(matched_benefits):
        current_row.append(
            CallbackButton(
                text=str(i + 1),
                payload=Payload(foo=f'search_measure_id_{benefit.measure_id}').pack()
            )
        )
        if len(current_row) == buttons_per_row or i == len(matched_benefits) - 1:
            builder.row(*current_row)
            current_row = []

    builder.row(
        CallbackButton(
            text='🔙 Назад: в Поиск',
            payload=Payload(foo='return_to_search').pack()
        )
    )

    return builder.as_markup()

async def benefits_pagination_search_keyboard(matched_benefits, page=0):
    builder = InlineKeyboardBuilder()
    benefits_per_page = 10

    start_idx = page * benefits_per_page
    end_idx = start_idx + benefits_per_page
    current_benefits = matched_benefits[start_idx:end_idx]
    
    total_pages = (len(matched_benefits) + benefits_per_page - 1) // benefits_per_page
    
    buttons_per_row = 7
    current_row = []
    for i, benefit in enumerate(current_benefits):
        benefit_number = start_idx + i + 1
        current_row.append(
            CallbackButton(
                text=str(benefit_number),
                payload=Payload(foo=f'pagination_measure_id_{benefit.measure_id}').pack()
            )
        )
        if len(current_row) == buttons_per_row or i == len(current_benefits) - 1:
            builder.row(*current_row)
            current_row = []

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            CallbackButton(
                text="⏪",
                payload=Payload(foo=f'page_0').pack()
            )
        )
    if page > 0:
        nav_buttons.append(
            CallbackButton(
                text="◀️",
                payload=Payload(foo=f'page_{page-1}').pack()
            )
        )
    if page < total_pages - 1:
        nav_buttons.append(
            CallbackButton(
                text="▶️",
                payload=Payload(foo=f'page_{page+1}').pack()
            )
        )
    if page < total_pages - 1:
        nav_buttons.append(
            CallbackButton(
                text="⏩",
                payload=Payload(foo=f'page_{total_pages-1}').pack()
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)
        
    builder.row(
        CallbackButton(
            text=f"Страница {page + 1}/{total_pages}",
            payload='_'
        )
    )
    builder.row(
        CallbackButton(
            text="🔙 Назад: В поиск",
            payload=Payload(foo='return_to_search').pack()
        )
    )
    
    return builder.as_markup()
