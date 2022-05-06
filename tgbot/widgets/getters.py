from aiogram_dialog import DialogManager

from tgbot.services.db import db_get_user_info, db_get_words_categories

async def get_words_categories(**kwargs) -> dict:
    dialog_manager = kwargs.get('dialog_manager')
    telegram_id = dialog_manager.current_context().start_data
    _, user_level, *_ = await db_get_user_info(
        telegram_id=telegram_id
    )
    categories_objects = await db_get_words_categories(
        level=user_level
    )
    return {
        "categories": [
            (
                object.category.capitalize(),
                object.id
                ) for object in categories_objects
            ],
        "count": len(categories_objects),
    }
    
