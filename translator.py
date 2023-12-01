from deep_translator import (
    GoogleTranslator,
)


def translate(text:str = "Hello there"):
    en_translator = GoogleTranslator(source="auto", target="en")
    en_translate = en_translator.translate(text=text)
    print("🇬🇧", en_translate)

    uz_translator = GoogleTranslator(source="auto", target="uz")
    uz_translate = uz_translator.translate(text=text)
    print("🇺🇿", uz_translate)
    return {"en": en_translate, "uz": uz_translate}

if __name__ == "__main__":
    translate("Hello there")
