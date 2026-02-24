from pyrogram import filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

from maythusharmusic import app
from maythusharmusic.utils.decorators import AdminRightsCheck # လိုအပ်ပါက Admin သာသုံးရန် ကန့်သတ်နိုင်သည်

@app.on_message(filters.command(["getemoji", "emoji"]))
async def get_custom_emoji_id(client, message: Message):
    # Reply ပြန်ထားတဲ့ Message ကို ယူမယ်၊ Reply မလုပ်ထားရင် ကိုယ်ပို့တဲ့ Message ကို ယူမယ်
    target_msg = message.reply_to_message if message.reply_to_message else message
    
    # Message ထဲမှာ Entity (Link, Mention, Emoji စသည်) ပါ/မပါ စစ်ဆေးမယ်
    if not target_msg.entities:
        return await message.reply_text("⚠️ **ဒီစာထဲမှာ Premium / Custom Emoji မတွေ့ပါဘူး။**")
    
    extracted_emojis = []
    
    # Entity တွေကို တစ်ခုချင်းစီ စစ်မယ်
    for entity in target_msg.entities:
        # Custom Emoji ဖြစ်ခဲ့ရင်
        if entity.type == MessageEntityType.CUSTOM_EMOJI:
            # Emoji ရဲ့ ပုံစံ (Fallback text)
            emoji_text = target_msg.text[entity.offset : entity.offset + entity.length]
            # Emoji ရဲ့ ID
            emoji_id = entity.custom_emoji_id
            
            # HTML code ထုတ်ပေးမယ်
            html_format = f'`<emoji id="{emoji_id}">{emoji_text}</emoji>`'
            extracted_emojis.append(f"Emoji: {emoji_text}\nID: `{emoji_id}`\nHTML: {html_format}\n")
            
    # Custom Emoji တစ်ခုမှ မတွေ့ရင်
    if not extracted_emojis:
        return await message.reply_text("⚠️ **ဒီစာထဲမှာ Premium Emoji အစစ် မပါဝင်ပါဘူး။ (သာမန် Emoji များသာ ဖြစ်နိုင်ပါသည်။)**")
        
    # ရလာတဲ့ ID တွေကို စာပြန်ပို့မယ်
    final_text = "✨ **Custom Emoji IDs Found:**\n\n" + "\n".join(extracted_emojis)
    await message.reply_text(final_text)
