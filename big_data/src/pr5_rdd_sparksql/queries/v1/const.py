politicians_tuple = (
    # USA
    ("Джо", "Байден"),
    ("Камала", "Харрис"),
    ("Дональд", "Трамп"),
    ("Барак", "Обама"),
    ("Хиллари", "Клинтон"),
    # Europe
    ("Ангела", "Меркель"),  # Germany
    ("Эммануэль", "Макрон"),  # France
    ("Борис", "Джонсон"),  # UK
    ("Владимир", "Путин"),  # Russia
    ("Джузеппе", "Конте"),  # Italy
    ("Педро", "Санчес"),  # Spain
    ("Марк", "Рютте"),  # Netherlands
    ("Метте", "Фредериксен"),  # Denmark
    ("Стефан", "Лёфвен"),  # Sweden
    ("Марианна", "Тиссен"),  # Belgium
    ("Лео", "Варадкар"),  # Ireland
    ("Матеуш", "Моравецкий"),  # Poland
)
politicians = {x.lower() for p in politicians_tuple for x in p}
