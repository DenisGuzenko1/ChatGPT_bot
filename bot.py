# Импортируем необходимые библиотеки
import aiogram
import openai

# Устанавливаем токены для телеграм бота и openai
TELEGRAM_TOKEN = "6075431236:AAFgu93i451YbnTfVJL3q3Wa5GGChCGmGbc"
openai.api_key = "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"

# Создаем объекты бота и диспетчера
bot = aiogram.Bot(token=TELEGRAM_TOKEN)  # Какой бот будет использоваться
dp = aiogram.Dispatcher(bot)  # Диспетчера

# История чатов пользователей (хранение в памяти - до перезапуска программы)
users_chat_history = {}


# Создаем первый раз чат для пользователя
def init_user_chat(tg_id):
    # Для конкретного пользователя мы задаем настройку chatGPT
    users_chat_history[tg_id] = [
        {
            "role": "system",
            "content": "Ты помощник, который отвечает правильно и с подробным пояснением ответа.",
        }
    ]


# Создаем функцию для генерации ответа с помощью chatgpt
def generate_response(tg_id, message):
    # tg_id - идентификатор пользователя
    # message - его сообщение

    # Если еще нет истории чата для `tg_id`, инициализируем чат
    if tg_id not in users_chat_history:
        init_user_chat(tg_id)  # Вызов функции для инициализации чата

    # После этого у нас уже есть настройка чата и первый запрос к chatGPT

    # Добавляем в историю чата новый запрос пользователя
    users_chat_history[tg_id].append(
        {
            "role": "user",
            "content": message,
        }
    )

    # Делаем запрос в ChatGPT и получаем результат
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=users_chat_history[tg_id],  # Отправляем всю историю чата
        temperature=0.7,
    )

    # Ответ от ChatGPT (текстовый)
    chat_gpt_answer = response["choices"][-1]["message"]["content"]

    # Добавляем ответ от ChatGPT в историю чата
    users_chat_history[tg_id].append(
        {
            "role": "assistant",  # Роль другая
            "content": chat_gpt_answer,
        }
    )
    return chat_gpt_answer


# Создаем обработчик для текстовых сообщений TG
@dp.message_handler()
async def handle_text(message: aiogram.types.Message):
    await bot.send_message(message.from_user.id, 'Введите запрос')
    # В момент получения текста от пользователя
    tg_id = message.from_user.id  # 1317283709

    # Отправляем статус, что бот печатает текст
    await bot.send_chat_action(message.chat.id, "typing")
    # =========================================

    # Генерируем ответ с помощью chatgpt
    chatgpt_text_answer = generate_response(tg_id, message.text)

    # Отправляем ответ пользователю
    await message.reply(chatgpt_text_answer)


print("Start BOT")
aiogram.executor.start_polling(dp)
