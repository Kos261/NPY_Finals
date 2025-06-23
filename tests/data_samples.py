import pandas as pd

data = {
    "Miejscowość": [
        "Adamów (siedleckie)",
        "Adamów (zamojskie)",
        "Adamówka",
        "Aleksandrów",
        "Aleksandrów Kujawski",
        "Aleksandrów Łódzki",
        "Alwernia",
        "Andrespol",
        "Andrychów",
        "Andrzejewo",
    ],
    "Długość": [
        "22°15'E",
        "23°10'E",
        "22°42'E",
        "19°59'E",
        "18°42'E",
        "19°19'E",
        "19°32'E",
        "19°37'E",
        "19°20'E",
        "22°12'E",
    ],
    "Szerokość": [
        "51°45'N",
        "50°36'N",
        "50°16'N",
        "51°16'N",
        "52°53'N",
        "51°49'N",
        "50°04'N",
        "51°44'N",
        "49°52'N",
        "52°50'N",
    ],
}

df_cities = pd.DataFrame(data)