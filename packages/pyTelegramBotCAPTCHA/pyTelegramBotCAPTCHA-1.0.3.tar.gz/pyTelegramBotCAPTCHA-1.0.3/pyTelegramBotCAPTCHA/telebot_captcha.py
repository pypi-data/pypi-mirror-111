# -*- coding: utf-8 -*-
import os
import random
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Tuple, List, Optional
from threading import Timer

try:
    import ujson as json
except:
    import json

from captcha.image import ImageCaptcha
from PIL import Image
from telebot import TeleBot, types


_base_path = Path(__file__).parent.absolute()
_fonts_path = _base_path / "data" / "fonts"
_captcha_saves = (Path(".") / ".captcha-saves").parent.absolute()
_fonts = []

MIN_TIMEOUT = 30
MAX_TIMEOUT = 600
CODE_LENGTH = 8

digits = "1234567890"
hexdigits = digits + "ABCDEF"

languages = None 
with (_base_path / "data" / "languages.json").open("r",encoding='utf-8') as f:

    languages = json.loads(f.read())

class Captcha(types.JsonDeserializable, types.JsonSerializable):
    @classmethod
    def de_json(cls, json_str):
        if not json_str: return None
        obj = json.loads(json_str)
        obj['chat'] = types.Chat(**obj['chat'])
        obj['user'] = types.User(**obj['user'])
        return cls(**obj)

    def __init__(self, chat: types.Chat, user: types.User, language: str, timeout: float, 
            only_digits: bool, add_noise: bool, bot: TeleBot=None, **kwargs) -> None:
        """
        The Captcha object. Do not call this function yourself. 
        Use `captcha_manager.send_random_captcha(...)` instead
        """
        self._solved = False
        if not bot:
            # Loaded from file
            self.chat = chat
            self.user = user
            self.language = language
            self.previous_tries = kwargs["previous_tries"]
            self.correct_code = kwargs["correct_code"]
            text = languages[self.language]["text"].replace("#USER", _user_link(self.user))
            self.text = text if self.previous_tries == 0 else languages[self.language]["try_again"]
            self.users_code = kwargs["users_code"]
            self.message_id = kwargs["message_id"]
            self.date = kwargs["date"]
            self._timeout = timeout
            self._timeout_thread = None
            self._captcha_id = kwargs["captcha_id"]
            
            self._only_digits = only_digits
            self._add_noise = add_noise

            self.image = None
            self.reply_markup = None

        else:
            # Initialized by `CaptchaManager.send_random_captcha()`
            self._captcha_id = f"{CaptchaManager._bot_id}={chat.id}={user.id}"
            self._timeout_thread = None
            self._timeout = timeout
            self._only_digits = only_digits
            self._add_noise = add_noise
            
            self.chat = chat
            self.user = user
            self.users_code = ""
            self.language = language
            self.previous_tries = 0

            self.text = languages[self.language]["text"].replace("#USER", _user_link(self.user))
            self.correct_code, self.image = _random_codeimage(self._only_digits, self._add_noise)
            self.reply_markup = _code_input_markup(user_id=user.id, language=language, only_digits=only_digits)

            m = self.message_id = bot.send_photo(
                chat_id=self.chat.id, 
                photo=self.image,
                caption=self.text,
                reply_markup=self.reply_markup,
                parse_mode="HTML"
            )
            self.message_id = m.message_id
            self.date = m.date
            self._save_file()

    @property
    def incorrect_digits(self) -> int:
        """
        How many (hex)digits do not match?
        """
        users_code = self.users_code.ljust(CODE_LENGTH, "x")
        count = 0
        for i, d in enumerate(users_code):
            if self.correct_code[i] != d: count += 1
        return count
    
    @property
    def solved(self) -> bool:
        """
        Did the user solve the captcha?
        It does NOT matter if he solved it correct!
        """
        return self._solved


    def to_json(self):
        chat_dict = {
            "id": self.chat.id,
            "type": self.chat.type,
            "title": self.chat.title,
            "username": self.chat.username
        }

        json_dict = {
            "chat": chat_dict,
            "user": types.User.to_dict(self.user),
            "language": self.language,
            "users_code": self.users_code,
            "correct_code": self.correct_code,
            "message_id": self.message_id,
            "timeout": self._timeout,
            "date": self.date,
            "captcha_id": self._captcha_id,
            "only_digits": self._only_digits,
            "add_noise": self._add_noise,
            "previous_tries": self.previous_tries
        }
        return json.dumps(json_dict)

    def _continue_timeout(self):
        if self._timeout and CaptchaManager._handlers["on_timeout"]:
            now = datetime.now().timestamp()
            exec_at = self.date + self._timeout
            if now >= exec_at:
                self._timeout_thread = Timer(interval=1, 
                    function=CaptchaManager._handlers["on_timeout"], args=[self])
            else:
                self._timeout_thread = Timer(interval=exec_at-now, 
                    function=CaptchaManager._handlers["on_timeout"], args=[self])
            self._timeout_thread.start()

    def _refresh(self, bot: TeleBot, only_digits=False, add_noise=True, timeout=None) -> None:
        new_code, new_image = _random_codeimage(only_digits, add_noise)
        self._timeout = timeout
        self.date = datetime.now().timestamp()
        self.image = new_image
        self.correct_code = new_code
        self.users_code = ""
        self.text = languages[self.language]["try_again"]
        
        self.reply_markup = _code_input_markup(self.user.id, "en", only_digits)

        bot.edit_message_media(
            types.InputMediaPhoto(self.image, self.text, "HTML"), 
            self.chat.id, self.message_id, reply_markup=self.reply_markup
        )

        self._save_file()
        
    def _save_file(self):
        if not os.path.exists(str(_captcha_saves)):
            os.mkdir(_captcha_saves)
        filename = self._captcha_id + ".json"
        filepath = _captcha_saves / filename
        with open(filepath, "w+",encoding="utf8") as f:
            f.write(self.to_json())
    
    def _delete_file(self):
        filename = self._captcha_id + ".json"
        filepath = _captcha_saves / filename
        if filepath.exists():
            filepath.unlink()

    def _update(self, bot: TeleBot, callback: types.CallbackQuery):
        btn = callback.data.split("=")[2]
        if (btn == "BACK"):
            self.users_code = self.users_code[:-1]
        else:
            self.users_code = (self.users_code + btn)[:CODE_LENGTH]

        if not self.reply_markup:
            self.reply_markup = callback.message.reply_markup
        try:
            bot.edit_message_caption(
                caption=self.text + f"<pre>{self.users_code}</pre>",
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=self.reply_markup,
                parse_mode="HTML"
                
            )
            self._save_file()
        except: pass


class CaptchaManager:
    _handlers = {"on_correct": None, "on_not_correct": None, "on_timeout": None}
    _bot_id = None

    def __init__(self, bot_id: int, default_language: str="en", default_timeout: float=None, fonts: List=None, code_length: int=8) -> None:
        """
        The Captcha Manager

        fonts=['/path/to/A.ttf', '/path/to/B.ttf']
        You can put as many fonts as you like. But be aware of your memory, all of
        the fonts are loaded into your memory, so keep them a lot, but not too
        many.

        :param bot_id: the user_id of your bot `bot.get_me().id`
        :param default_language: language to be used if not defined in `send_random_captcha`
        :param default_timeout: timeout to be useed if not defined in `send_random_captcha`
        :param fonts: fonts to be used to generate CAPTCHA images. (.ttf)
        :param code_length: the lenght of the code. must be between 4-12 chars
        """
        global CODE_LENGTH
        if not (4 <= code_length <= 12):
            raise ValueError("The Code lenghth must be between 4 and 12.")
        CODE_LENGTH = code_length

        self.__class__._bot_id = bot_id
        if default_language.lower() not in languages.keys():
            raise NotImplementedError (f"The Language '{default_language}' is not implemented yet")
        self.default_language = default_language.lower()

        if default_timeout and not MIN_TIMEOUT <= default_timeout <= MAX_TIMEOUT:
            raise ValueError(f"`default_timeout` must be between {MIN_TIMEOUT} and {MAX_TIMEOUT} seconds or `None`")
        self.default_timeout = default_timeout

        global _fonts
        _fonts = fonts or _fonts

        if not fonts:
            for f in os.listdir(_fonts_path):
                if f.endswith(".ttf") and not f.startswith("."):
                    _fonts.append(str(_fonts_path / f))

        self.captchas: Dict[str, Captcha] = {}
        if os.path.exists(_captcha_saves):
            saved_captchas = os.listdir(_captcha_saves)
            for f in saved_captchas:
                if f.endswith(".json") and not f.startswith("."):
                    if f.startswith(f"{self._bot_id}="):
                        filepath = _captcha_saves / f
                        with filepath.open("r") as f:
                            json_str = f.read()
                            captcha = Captcha.de_json(json_str)
                            self.captchas[captcha._captcha_id] = captcha

    def send_random_captcha(self, bot: TeleBot, chat: types.Chat, user: types.User, language: str=None, 
            only_digits: bool=False, add_noise: bool=True, timeout: float=None) -> Captcha:
        """
        sends a randomly generated captcha into your chat.
        :param bot: your TeleBot instance
        :param chat: the chat (chat not chat_id)
        :param user: the user who must solve the captcha (user not user_id)
        :param language: the language to use for the captcha
        :param only_digits: using only digits or hexdigits
        :param add_noise: add noise to the image
        :param timeout: timeout must be at least 30 and maximum 600 seconds or `None`
        :return: the generated Captcha object
        """
        language = (language or self.default_language).lower()
        if language not in languages.keys():
            raise NotImplementedError (f"The Language '{language}' is not implemented yet")

        timeout = timeout or self.default_timeout

        captcha = Captcha(chat, user, language, timeout, only_digits, add_noise, bot)
        if captcha._captcha_id in self.captchas.keys():
            old_captcha: Captcha = self.captchas.pop(captcha._captcha_id)
            if (old_captcha._timeout_thread):
                old_captcha._timeout_thread.cancel()
            self.delete_captcha(bot, old_captcha)
        
        if timeout and self._handlers["on_timeout"]:
            if not MIN_TIMEOUT <= timeout <= MAX_TIMEOUT:
                raise ValueError(f"`timeout` must be between {MIN_TIMEOUT} and {MAX_TIMEOUT} seconds or `None`")
            captcha._timeout_thread = Timer(interval=timeout, function=self._handlers["on_timeout"], args=[captcha])
            captcha._timeout_thread.start()
            captcha._save_file()
            
        self.captchas[captcha._captcha_id] = captcha
        return captcha

    def restrict_chat_member(self, bot: TeleBot, chat_id: int, user_id: int) -> bool:
        """
        Set all permissions of a chat member to `False`.
        :param bot: your TeleBot instance
        :param chat_id: the Chat ID
        :param user_id: the User ID
        :retrun: True on sucess
        """
        return bot.restrict_chat_member(chat_id, user_id,
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False)
    
    def unrestrict_chat_member(self, bot: TeleBot, chat_id: int, user_id: int):
        """
        Set all permissions of a chat member to `True` which removes the restriction.
        :param bot: your TeleBot instance
        :param chat_id: the Chat ID
        :param user_id: the User ID
        :retrun: True on sucess
        """
        return bot.restrict_chat_member(chat_id, user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True)

    def update_captcha(self, bot: TeleBot, callback: types.CallbackQuery) -> None:
        """
        updates the captcha if a user has pressed a button. if submit is pressed the captcha gets checked
        :param bot: your TeleBot instance
        :param callback: the CallbackQuery
        """
        if not callback.data.startswith("?cap="): return

        user_id, btn = int(callback.data.split("=")[1]), callback.data.split("=")[2]
        captcha_id = f"{self.__class__._bot_id}={callback.message.chat.id}={user_id}"
        captcha: Captcha = self.captchas[captcha_id]

        if captcha.user.id != callback.from_user.id:
            bot.answer_callback_query(callback.id, text=languages[captcha.language]["wrong_user"])
            return
        
        if btn == "OK":
            if len(captcha.users_code) < CODE_LENGTH:
                bot.answer_callback_query(callback.id,text=languages[captcha.language]["notfull"], show_alert=True)
            else:
                user_id = int(callback.data.split("=")[1])
                captcha_id = f"{self.__class__._bot_id}={callback.message.chat.id}={user_id}"
                if (captcha_id in self.captchas):
                    self._check_captcha(self.captchas[captcha_id])
        else:
            captcha._update(bot, callback)
        
        bot.answer_callback_query(callback.id)
    
    def refresh_captcha(self, bot: TeleBot, captcha: Captcha, 
            only_digits: Optional[bool]=None, add_noise: Optional[bool]=None, timeout: Optional[float]=None) -> None:
        
        if captcha._timeout_thread is not None:
            captcha._timeout_thread.cancel()
        
        # Default settings to previous settings if not set again
        if only_digits is None: only_digits = captcha._only_digits
        if add_noise is None: add_noise = captcha._add_noise
        if timeout is None: timeout = captcha._timeout or self.default_timeout

        captcha._refresh(bot, only_digits, add_noise, timeout)
        if timeout:
            if not MIN_TIMEOUT < timeout < MAX_TIMEOUT:
                raise ValueError(f"`timeout` must be between {MIN_TIMEOUT} and {MAX_TIMEOUT} seconds or `None`")
            captcha._timeout_thread = Timer(interval=timeout, 
                function=self._handlers["on_timeout"], args=[captcha])
            captcha._timeout_thread.start()
            captcha._save_file()
        captcha._solved = False

    def delete_captcha(self, bot: TeleBot, captcha: Captcha) -> None:
        #self.captchas.pop(captcha._captcha_id)
        captcha._delete_file()
        try: bot.delete_message(captcha.chat.id, captcha.message_id)
        except: pass
        del captcha

    def on_captcha_correct(self, function):
        """
        Captcha correct decorator.
        This decorator can be used to decorate functions that must handle correct solved Captchas.

        Example:

        captcha_manager = CaptchaManager()

        # Handles correct solved Captchas
        @captcha_manager.captcha_correct
        def on_captcha_correct(captcha):
            bot.send_message(captcha.chat.id, captcha.user.first_name + ' solved the Captcha!')
        
        """
        def wrapper(*args, **kwargs):
            rv = function(*args, **kwargs)
            return rv
        self.__class__._handlers["on_correct"] = wrapper
        return wrapper
    
    def on_captcha_not_correct(self, function):
        """
        Captcha not correct decorator.
        This decorator can be used to decorate functions that must handle wrong solved Captchas.

        Example:

        captcha_manager = CaptchaManager()

        # Handles wrong solved Captchas
        @captcha_manager.captcha_not_correct
        def on_captcha_not_correct(captcha):
            bot.send_message(captcha.chat.id, captcha.user.first_name + ' failed the Captcha!')
        
        """
        def wrapper(*args, **kwargs):
            rv = function(*args, **kwargs)
            return rv
        self.__class__._handlers["on_not_correct"] = wrapper
        return wrapper

    def on_captcha_timeout(self, function):
        """
        Captcha timeout decorator.

        This decorator can be used to decorate functions that must handle Captchas 
        that have not been solved in a given time.
        Its recommended to check if the captcha has been solved (captcha.solved)
        before doing anything else, because threading is asynchronous.


        Example:

        bot = telebot.TeleBot(<Token>)
        captcha_manager = CaptchaManager()

        # Handles timed out Captchas
        @captcha_manager.on_captcha_timeout
        def on_captcha_timeout(captcha):
            if not captcha.solved:
                bot.send_message(captcha.chat.id, captcha.user.first_name + ' did not solve the Captcha!')

        Attention: You have to start the timeout handler at the end of your script 
        (above bot.polling())

        captcha_manager.start_timeout_handler()
        bot.polling()
        
        """
        def wrapper(*args, **kwargs):
            rv = function(*args, **kwargs)
            return rv
        self.__class__._handlers["on_timeout"] = wrapper
        for captcha in self.captchas.values():
            if (captcha._timeout):
                captcha._continue_timeout()
        return wrapper

    def _check_captcha(self, captcha: Captcha):
        is_correct = captcha.users_code == captcha.correct_code
        if (captcha._timeout_thread):
            captcha._timeout_thread.cancel()
            captcha._timeout_thread = None
        captcha.previous_tries += 1
        if is_correct:
            if (self._handlers["on_correct"]):
                self._handlers["on_correct"](captcha)
        else:
            if (self._handlers["on_not_correct"]):
                self._handlers["on_not_correct"](captcha)
        captcha._solved = True


def _code_input_markup(user_id: int, language: str, only_digits: bool) -> types.InlineKeyboardMarkup:
    values = {}
    for char in (digits if only_digits else hexdigits):
        values[char] = {"callback_data": f"?cap={user_id}={char}"}
    return _quick_markup({**values,
        languages[language]["back"]: {"callback_data": f"?cap={user_id}=BACK"},
        languages[language]["submit"]: {"callback_data": f"?cap={user_id}=OK"}
    }, 5 if only_digits else 4)
  
def _quick_markup(values, row_width=4) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    buttons = []
    for text, kwargs in values.items():
        buttons.append(types.InlineKeyboardButton(text=text, **kwargs))
    markup.add(*buttons)
    return markup

def _random_code(chars):
    length = CODE_LENGTH
    code = ""
    while length > 0:
        if length >= len(chars):
            code += "".join(random.sample(chars, len(chars)))
            length -= len(chars)
        else:
            code += "".join(random.sample(chars, length))
            length = 0
    return code

def _random_codeimage(only_digits: bool=False, add_noise: bool=True) -> Tuple:
    image = ImageCaptcha(300, 128, _fonts, [48, 42, 54])
    code = _random_code(digits if only_digits else hexdigits)
    image = image.generate_image(code)

    if add_noise:
        image = _add_noise(image)
    return (code, image)

def _add_noise(im: Image.Image, mean=12, sigma=48) -> Image.Image:
    for x in range(im.size[0]):
        for y in range (im.size[1]):
            r, g, b = im.getpixel((x, y))
            im.putpixel((x, y), (
                int(min(max(0, r + random.normalvariate(mean,sigma)), 255)),
                int(min(max(0, g + random.normalvariate(mean,sigma)), 255)),
                int(min(max(0, b + random.normalvariate(mean,sigma)), 255)),
            ))
    return im

def _escape(text: str) -> str:
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt"}
    for old, new in chars.items(): text = text.replace(old, new)
    return text

def _user_link(user: types.User, include_id: bool=False) -> str:
    name = _escape(user.first_name)
    return f"<a href='tg://user?id={user.id}'>{name}</a>" + (f" (<pre>{user.id}</pre>)" if include_id else "")

