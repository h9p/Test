from pyrogram import Client
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message

from ..helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f'<b>👋🏻 ها ضلعي {message.from_user.mention()} شلونك .. شني نايم كاعد </b>\n\n'
        'شوف ضلعي تعرف كلش زين اني شنو , '
        'بس اخر مرة راح اشرحلك اني بووووت ماااال اغاااااانيييي تمام ؟ لتضوج/ين اني احبك/ج بس شوية معصب'
        '\n\nالاوامر حتى تشغلني هي مثل ممكتوب جوة \n\n'
        '/play - تشغل الاغاني .. \n'
        '/mute - حتى تكتمني .. \n'
        '/unmute - حتى تلغي الكتم علية .. \n'
        '/pause - توكف الاغاني\n'
        '/resume - تكمل الاغنية وين ما وصلت بيها\n'
        '/skip - تتخطى الاغنية\n'
        '/stop - حتى توكف الاغنية ونخلص من جهرتكم 😒',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '🔈 القناة مال البوت', url='https://t.me/pRincebotsCh',
                    ),
                    InlineKeyboardButton(
                        'حساب المطور💬', url='https://t.me/ihumam',
                    ),
                ],
            ],
        ),
    )
