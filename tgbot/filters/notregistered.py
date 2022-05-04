from aiogram.dispatcher.filters import BoundFilter

from tgbot.services.db import db_get_users_telegram_ids


class NotRegistered(BoundFilter):
    async def check(self, obj):

        return obj.from_user.id not in [
            user.get('telegram_id') for user in await db_get_users_telegram_ids() 
            ]

