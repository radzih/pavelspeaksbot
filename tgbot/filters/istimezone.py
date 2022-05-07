import pytz

from aiogram.dispatcher.filters import BoundFilter

class IsTimezone(BoundFilter):
    async def check(self, obj) -> bool:
        return obj.text in pytz.all_timezones
