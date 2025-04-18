import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


load_dotenv()

TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT = ptbot.Bot(TG_TOKEN)


def say_timer_finished(author_id):
    BOT.send_message(author_id, "Время вышло")


def countdown_answer(secs_left, author_id, message_id, secs_max):
    BOT.update_message(author_id,
                       message_id,
                       f"Осталось секунд: {secs_left}\n"
                       f"{render_progressbar(secs_max, secs_max - secs_left)}")


def notify_progress(author_id, message):
    secs_max = parse(message)
    secs_left = parse(message)
    message_id = BOT.send_message(author_id, "Запускаю таймер...")
    BOT.create_countdown(secs_left,
                         countdown_answer,
                         author_id=author_id,
                         message_id=message_id,
                         secs_max=secs_max)
    BOT.create_timer(secs_left, say_timer_finished, author_id=author_id)


def render_progressbar(total, iteration, prefix='', suffix='', length=30,
                       fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    BOT.reply_on_message(notify_progress)
    BOT.run_bot()


if __name__ == '__main__':
    main()
