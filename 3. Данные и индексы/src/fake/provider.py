import importlib
from importlib import util
from faker import Faker

LOCALES = [
    "az_AZ",
    "cs_CZ",
    "da_DK",
    "de_AT",
    "de_DE",
    "el_GR",
    "en_GB",
    "en_PH",
    "en_US",
    "es_ES",
    "fa_IR",
    "fi_FI",
    "fil_PH",
    "fr_CH",
    "fr_FR",
    "he_IL",
    "hr_HR",
    "hu_HU",
    "hy_AM",
    "id_ID",
    "it_IT",
    "ja_JP",
    "ko_KR",
    "nl_NL",
    "no_NO",
    "pl_PL",
    "pt_BR",
    "pt_PT",
    "ro_RO",
    "ru_RU",
    "sk_SK",
    "sv_SE",
    "th_TH",
    "tl_PH",
    "tr_TR",
    "uk_UA",
    "zh_CN",
    "zh_TW",
]

PROVIDERS = (
    "faker.providers.person",
    "faker.providers.company",
    "faker.providers.job",
    "faker.providers.phone_number",
)


def fake(locale=None):

    ff = Faker()

    for provider in PROVIDERS:
        local_provider = ".".join((provider, locale or ""))
        if util.find_spec(local_provider):
            module = importlib.import_module(local_provider)
        else:
            module = importlib.import_module(provider)

        ff.add_provider(module.Provider)

    return ff
