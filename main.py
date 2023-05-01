import logging
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from chat_bot import ChatBot
from constants import API_ID, API_HASH, TOKEN, SESSION_STRING

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    chat_bot = ChatBot(client)
    await client.start(bot_token=TOKEN)
    inactive_conversations_task = asyncio.create_task(chat_bot.send_inactive_conversations())
    client.add_event_handler(chat_bot.start_handler, events.NewMessage(pattern="/start"))
    client.add_event_handler(chat_bot.button_handler, events.NewMessage(pattern="🎉 Порадоваться|🙏 Сказать спасибо создателю"))
    client.add_event_handler(chat_bot.message_handler, events.NewMessage())
    await client.send_message(137487102, "Бот включился.")
    await client.run_until_disconnected()
    return inactive_conversations_task

async def shutdown(tasks):
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    if client.is_connected:
        await client.send_message(137487102, "Бот выключается.")
        await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Получен сигнал прерывания. Ожидание завершения...")
        pending_tasks = asyncio.all_tasks(asyncio.get_event_loop())
        asyncio.run(shutdown(pending_tasks))
