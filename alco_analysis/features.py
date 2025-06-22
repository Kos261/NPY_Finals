import numpy as np
import unidecode, re


def cut_KPPSP_in_city_names(df):
    #Aleksandrów Kujawski i Różno Parcele są razem nie wiedzieć czemu ale dobra
    df["Miejscowość"] = df["Nazwa KP/M PSP"].apply(lambda x: " ".join(x.split()[2:]))
    df = df.drop(["Nazwa KP/M PSP","Nazwa KW PSP"], axis=1)
    return df

def clean_city_names(txt):
    """Zdejmuje polskie znaki, spacje, zamienia na lower-case
       i odcina dopiski w nawiasie."""
    txt = unidecode.unidecode(str(txt)).lower().strip()
    # np. "Adamów (siedleckie)" -> "adamow"
    return re.sub(r"\s*\(.*\)$", "", txt)

def norm_city(txt):
    return unidecode.unidecode(str(txt)).lower().strip()

def norm_woj(txt):
    return (str(txt)
            .replace("WOJ.", "")
            .replace("WOJ", "")
            .strip()
            .upper())

def split_cities(raw):
    # rozdziel po przecinku lub średniku
    parts = re.split(r'[;,]', str(raw))
    return [norm_city(p) for p in parts if p.strip()]

def take_first_city(df):
    tmp = df.copy()
    # print(tmp.head(5))
    tmp['city'] = tmp['city'].apply(lambda x: split_cities(x)[0])
    return tmp

def dms_to_decimal(coord):
    import re
    match = re.match(r"(\d+)°(\d+)'?([NSEW])", coord.strip())
    if not match:
        return None
    degrees, minutes, direction = match.groups()
    decimal = float(degrees) + float(minutes) / 60
    if direction in ['W', 'S']:
        decimal = -decimal
    decimal = round(decimal,4)
    return decimal