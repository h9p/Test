from os import path

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice

from .. import converter
from .. import queues
from ..callsmusic import callsmusic
from ..config import DURATION_LIMIT
from ..downloaders import youtube
from ..helpers.chat_id import get_chat_id
from ..helpers.decorators import errors
from ..helpers.errors import DurationLimitError
from ..helpers.filters import command
from ..helpers.filters import other_filters


@Client.on_message(command('play') & other_filters)
@errors
async def play(_, message: Message):
    audio = (
        message.reply_to_message.audio or message.reply_to_message.voice
    ) if message.reply_to_message else None
    response = await message.reply_text('<b>🔄 دنعالج الصوت انطي صبر 😒</b>', False)
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f'يعني مدتشوف المقطع اطول من فلم الرسالة ؟ شنو لوتي تشغل صوت اطول من  '
                f'{round(audio.duration / 60)} دقيقة 😒',
            )
        file_name = audio.file_unique_id + '.' + (
            (
                audio.file_name.split('.')[-1]
            ) if (
                not isinstance(audio, Voice)
            ) else 'ogg'
        )
        file_name = path.join(path.realpath('downloads'), file_name)
        file = await converter.convert(
            (
                await message.reply_to_message.download(file_name)
            )
            if (
                not path.isfile(file_name)
            )
            else file_name,
        )
    else:
        entities = []
        if message.entities:
            entities += entities
        elif message.caption_entities:
            entities += message.caption_entities
        if message.reply_to_message:
            text = message.reply_to_message.text \
                or message.reply_to_message.caption
            if message.reply_to_message.entities:
                entities = message.reply_to_message.entities + entities
            elif message.reply_to_message.caption_entities:
                entities = message.reply_to_message.entities + entities
        else:
            text = message.text or message.caption

        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]

        if urls:
            url = text[urls[0].offset:urls[0].offset + urls[0].length]
        elif text_links:
            url = text_links[0].url
        else:
            await response.edit_text(
                '<b>❌ منطيتني شي اشغله شلايتي</b>',
            )
            return

        file = await converter.convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file)
        await response.edit_text(
            f'<b>#️⃣ العينتين مكانه بالسره هو {position}</b>...',
        )
    else:
        await callsmusic.set_stream(chat_id, file)
        await response.edit_text('<b>▶️ فرحان هسة ؟ شغلنالك الاغنية سوي كتم واسمع</b>')
