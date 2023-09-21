import telebot
import time
from telebot import apihelper
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("6268369826:AAHrv4JLOIGW_yqke9T3n1yX3F0VKulzfe0")
waiting_list = []
chat_sessions = {}
blocker_enabled = False



# Handle "/start" command
@bot.message_handler(commands=["start"])
def start(message):
    description = "Welcome to the Encrypted Pair Chat Bot!\n\n"
    description += "This chat bot pairs you with a random stranger for an encrypted chat session.\n\n"
    description += "Rules:\n"
    description += "- Speak in English.\n"
    description += "- Be respectful and polite.\n"
    description += "- Do not share personal information.\n"
    description += "- Do not engage in illegal or harmful activities.\n\n"
    description += "Commands:\n"
    description += "To start chatting, type /find.\n"
    description += "To find the next stranger,type /next.\n"
    description += "To End the chat, type /end.\n\n"
    description += "Enjoy your chat!"

    bot.send_message(message.chat.id, description)



# Handle "/find" command
@bot.message_handler(commands=["find"])
def find_partner(message):
    user_id = message.chat.id
    active_users = len(chat_sessions)  + len(waiting_list) # Divide by 2 to get the number of chat sessions
    chat_session = len(chat_sessions) // 2
    waiting_lists = len(waiting_list)
    bot.send_message(user_id, f"Searching for a stranger... Active users: {active_users}\n Chat connect pairs: {chat_session}\n Waiting Lists: {waiting_lists}")

    if user_id in chat_sessions:
        bot.send_message(user_id, "You are already in a chat. Use /end to leave the chat.")
    elif user_id in waiting_list:
        bot.send_message(user_id, "You are already in the waiting list. Please wait for a partner to be assigned.")
    else:
        waiting_list.append(user_id)
        try_match_partners()


# Handle "/end" command
@bot.message_handler(commands=["end"])
def end_chat(message):
    user_id = message.chat.id

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            bot.send_message(user_id, "Chat ended.")
            bot.send_message(partner_id, "Chat ended.")
            chat_sessions.pop(user_id, None)  # Remove the key if it exists, otherwise do nothing
            chat_sessions.pop(partner_id, None)  # Remove the key if it exists, otherwise do nothing
            try_match_partners()
        else:
            bot.send_message(user_id, "You don't have an ongoing chat.")
    elif user_id in waiting_list:
        waiting_list.remove(user_id)
        bot.send_message(user_id, "You have left the waiting list.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat.")

# Handle "/next" command
@bot.message_handler(commands=["next"])
def next_stranger(message):
    user_id = message.chat.id
    active_users = len(chat_sessions)  + len(waiting_list) # Divide by 2 to get the number of chat sessions
    chat_session = len(chat_sessions) // 2
    waiting_lists = len(waiting_list)
    bot.send_message(user_id, f" Active users: {active_users}\n Chat connect pairs: {chat_session}\n Waiting Lists: {waiting_lists}")

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            bot.send_message(user_id, "Chat ended.")
            bot.send_message(partner_id, "Chat ended.")
            chat_sessions.pop(user_id, None)  # Remove the key if it exists, otherwise do nothing
            chat_sessions.pop(partner_id, None)  # Remove the key if it exists, otherwise do nothing
            try_match_partners()
        else:
            bot.send_message(user_id, "You don't have an ongoing chat.")
    elif user_id in waiting_list:
        waiting_list.remove(user_id)
        bot.send_message(user_id, "You have left the waiting list.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat.")

    if user_id in chat_sessions:
        bot.send_message(user_id, "You are already in a chat. Use /end to leave the chat.")
    elif user_id in waiting_list:
        bot.send_message(user_id, "You are already in the waiting list. Please wait for a partner to be assigned.")
    else:
        waiting_list.append(user_id)
        try_match_partners()
        bot.send_message(user_id, f" Active users: {active_users}\n Chat connect pairs: {chat_session}\n Waiting Lists: {waiting_lists}")

@bot.message_handler(commands=["blockon"])
def enable_blocker(message):
    global blocker_enabled
    blocker_enabled = True
    bot.send_message(message.chat.id, "Word blocking is enabled.")



# Handle "/unblock" command
@bot.message_handler(commands=["unblock"])
def disable_blocker(message):
    global blocker_enabled
    blocker_enabled = False
    bot.send_message(message.chat.id, "Word blocking is disabled.")



# Modify the handle_message function to check if blocking is enabled
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            if blocker_enabled and contains_blocked_word(text):
                bot.send_message(message.chat.id, "Your partner enabled the blocker. Please refrain from using toxic or inappropriate language and respect your partner.")
                # If blocking is enabled and the message contains a blocked word, ignore the message
                return
            bot.send_message(partner_id, text)
        else:
            bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")

# Add the contains_blocked_word function
def contains_blocked_word(message):
    blocked_words = ["2g1c", "2 girls 1 cup", "acrotomophilia", "alabama hot pocket", "alaskan pipeline", "anal", "anilingus", "anus", "apeshit", "arsehole", "ass", "asshole", "assmunch", "auto erotic", "autoerotic", "babeland", "baby batter", "baby juice", "ball gag", "ball gravy", "ball kicking", "ball licking", "ball sack", "ball sucking", "bangbros", "bangbus", "bareback", "barely legal", "barenaked", "bastard", "bastardo", "bastinado", "bbw", "bdsm", "beaner", "beaners", "beaver cleaver", "beaver lips", "beastiality", "bestiality", "big black", "big breasts", "big knockers", "big tits", "bimbos", "birdlock", "bitch", "bitches", "black cock", "blonde action", "blonde on blonde action", "blowjob", "blow job", "blow your load", "blue waffle", "blumpkin", "bollocks", "bondage", "boner", "boob", "boobs", "booty call", "brown showers", "brunette action", "bukkake", "bulldyke", "bullet vibe", "bullshit", "bung hole", "bunghole", "busty", "butt", "buttcheeks", "butthole", "camel toe", "camgirl", "camslut", "camwhore", "carpet muncher", "carpetmuncher", "chocolate rosebuds", "cialis", "circlejerk", "cleveland steamer", "clit", "clitoris", "clover clamps", "clusterfuck", "cock", "cocks", "coprolagnia", "coprophilia", "cornhole", "coon", "coons", "creampie", "cum", "cumming", "cumshot", "cumshots", "cunnilingus", "cunt", "darkie", "date rape", "daterape", "deep throat", "deepthroat", "dendrophilia", "dick", "dildo", "dingleberry", "dingleberries", "dirty pillows", "dirty sanchez", "doggie style", "doggiestyle", "doggy style", "doggystyle", "dog style", "dolcett", "domination", "dominatrix", "dommes", "donkey punch", "double dong", "double penetration", "dp action", "dry hump", "dvda", "eat my ass", "ecchi", "ejaculation", "erotic", "erotism", "escort", "eunuch", "fag", "faggot", "fecal", "felch", "fellatio", "feltch", "female squirting", "femdom", "figging", "fingerbang", "fingering", "fisting", "foot fetish", "footjob", "frotting", "fuck", "fuck buttons", "fuckin", "fucking", "fucktards", "fudge packer", "fudgepacker", "futanari", "gangbang", "gang bang", "gay sex", "genitals", "giant cock", "girl on", "girl on top", "girls gone wild", "goatcx", "goatse", "god damn", "gokkun", "golden shower", "goodpoop", "goo girl", "goregasm", "grope", "group sex", "g-spot", "guro", "hand job", "handjob", "hard core", "hardcore", "hentai", "homoerotic", "honkey", "hooker", "horny", "hot carl", "hot chick", "how to kill", "how to murder", "huge fat", "humping", "incest", "intercourse", "jack off", "jail bait", "jailbait", "jelly donut", "jerk off", "jigaboo", "jiggaboo", "jiggerboo", "jizz", "juggs", "kike", "kinbaku", "kinkster", "kinky", "knobbing", "leather restraint", "leather straight jacket", "lemon party", "livesex", "lolita", "lovemaking", "make me come", "male squirting", "masturbate", "masturbating", "masturbation", "menage a trois", "milf", "missionary position", "mong", "motherfucker", "mound of venus", "mr hands", "muff diver", "muffdiving", "nambla", "nawashi", "negro", "neonazi", "nigga", "nigger", "nig nog", "nimphomania", "nipple", "nipples", "nsfw", "nsfw images", "nude", "nudity", "nutten", "nympho", "nymphomania", "octopussy", "omorashi", "one cup two girls", "one guy one jar", "orgasm", "orgy", "paedophile", "paki", "panties", "panty", "pedobear", "pedophile", "pegging", "penis", "phone sex", "piece of shit", "pikey", "pissing", "piss pig", "pisspig", "playboy", "pleasure chest", "pole smoker", "ponyplay", "poof", "poon", "poontang", "punany", "poop chute", "poopchute", "porn", "porno", "pornography", "prince albert piercing", "pthc", "pubes", "pussy", "queaf", "queef", "quim", "raghead", "raging boner", "rape", "raping", "rapist", "rectum", "reverse cowgirl", "rimjob", "rimming", "rosy palm", "rosy palm and her 5 sisters", "rusty trombone", "sadism", "santorum", "scat", "schlong", "scissoring", "semen", "sex", "sexcam", "sexo", "sexy", "sexual", "sexually", "sexuality", "shaved beaver", "shaved pussy", "shemale", "shibari", "shit", "shitblimp", "shitty", "shota", "shrimping", "skeet", "slanteye", "slut", "s&m", "smut", "snatch", "snowballing", "sodomize", "sodomy", "spastic", "spic", "splooge", "splooge moose", "spooge", "spread legs", "spunk", "strap on", "strapon", "strappado", "strip club", "style doggy", "suck", "sucks", "suicide girls", "sultry women", "swastika", "swinger", "tainted love", "taste my", "tea bagging", "threesome", "throating", "thumbzilla", "tied up", "tight white", "tit", "tits", "titties", "titty", "tongue in a", "topless", "tosser", "towelhead", "tranny", "tribadism", "tub girl", "tubgirl", "tushy", "twat", "twink", "twinkie", "two girls one cup", "undressing", "upskirt", "urethra play", "urophilia", "vagina", "venus mound", "viagra", "vibrator", "violet wand", "vorarephilia", "voyeur", "voyeurweb", "voyuer", "vulva", "wank", "wetback", "wet dream", "white power", "whore", "worldsex", "wrapping men", "wrinkled starfish", "xx", "xxx", "yaoi", "yellow showers", "yiffy", "zoophilia", "🖕"]  # Add your list of blocked words here
    message = message.lower()  # Convert the message to lowercase for case-insensitive matching

    for word in blocked_words:
        if word in message:
            return True

    return False


# Handle incoming image messages
@bot.message_handler(content_types=["photo"])
def handle_image_message(message):
    user_id = message.chat.id

    if blocker_enabled:
        bot.send_message(user_id, "Word blocking is enabled. Image messages are not allowed.")
        return

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            photo = message.photo[-1]  # Get the largest available photo
            bot.send_photo(partner_id, photo.file_id)
        else:
            bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")


# Handle incoming sticker messages
@bot.message_handler(content_types=["sticker"])
def handle_sticker_message(message):
    user_id = message.chat.id

    if blocker_enabled:
        bot.send_message(user_id, "Word blocking is enabled. Stickers are not allowed.")
        return

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            sticker = message.sticker.file_id
            bot.send_sticker(partner_id, sticker)
        else:
            bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")

# Handle incoming voice messages
@bot.message_handler(content_types=["voice"])
def handle_voice_message(message):
    user_id = message.chat.id

    if blocker_enabled:
        bot.send_message(user_id, "Word blocking is enabled. Voice messages are not allowed.")
        return

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            voice = message.voice.file_id
            bot.send_voice(partner_id, voice)
        else:
            bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")

# Handle incoming video messages
@bot.message_handler(content_types=["video"])
def handle_video_message(message):
    user_id = message.chat.id

    if blocker_enabled:
        bot.send_message(user_id, "Word blocking is enabled. Video messages are not allowed.")
        return

    if user_id in chat_sessions:
        partner_id = chat_sessions[user_id]
        if partner_id:
            video = message.video.file_id
            bot.send_video(partner_id, video)
        else:
            bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")
    else:
        bot.send_message(user_id, "You don't have an ongoing chat. Use /find to search for a partner to chat with.")

# Try to match partners from the waiting list
def try_match_partners():
    while len(waiting_list) >= 2:
        user_id_1 = waiting_list.pop(0)
        user_id_2 = waiting_list.pop(0)

        chat_sessions[user_id_1] = user_id_2
        chat_sessions[user_id_2] = user_id_1

        bot.send_message(user_id_1, "Partner found! Remember to speak in English with your partner.")
        bot.send_message(user_id_2, "Partner found! Remember to speak in English with your partner.")

# Handle errors
@bot.message_handler(func=lambda message: True)
def handle_errors(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Sorry, I didn't understand that command. Please use one of the available commands.")

# Custom keyboard with swipe telegram options
def create_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="👍 Like"), KeyboardButton(text="👎 Dislike"))
    keyboard.add(KeyboardButton(text="😄 Happy"), KeyboardButton(text="😔 Sad"))
    return keyboard

# Enable custom keyboard for certain messages
@bot.message_handler(func=lambda message: True)
def enable_reply_keyboard(message):
    user_id = message.chat.id
    if user_id in chat_sessions.values():
        bot.send_message(user_id, "How do you feel about this message?", reply_markup=create_reply_keyboard())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        time.sleep(5)  # to introduce a delay
        ret_msg = bot.reply_to(message, "response message")
        print(ret_msg)
        assert ret_msg.content_type == 'text'
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 403 and "bot was blocked by the user" in e.description:
            user_id = message.chat.id
            bot.send_message(user_id, "Sorry, you have blocked my bot. Please press or type /next")
        else:
            raise e
    except Exception as e:
        print(e)

bot.polling(none_stop=True, timeout=123)
