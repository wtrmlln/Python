# Описание проекта:
Датасет предоставлен интернет-магазине «Стримчик», который продаёт по всему миру компьютерные игры. В нём указаны исторические данные о продажах игр, оценки пользователей и экспертов, жанры и платформы (например, Xbox или PlayStation).
Необходимо выявить определяющие успешность игры закономерности, с целью спланировать рекламные кампании для потенциально популярных продуктов.

# Описание исходных данных: 
- Name — название игры
- Platform — платформа
- Year_of_Release — год выпуска
- Genre — жанр игры
- NA_sales — продажи в Северной Америке (миллионы проданных копий)
- EU_sales — продажи в Европе (миллионы проданных копий)
- JP_sales — продажи в Японии (миллионы проданных копий)
- Other_sales — продажи в других странах (миллионы проданных копий)
- Critic_Score — оценка критиков (максимум 100)
- User_Score — оценка пользователей (максимум 10)
- Rating — рейтинг от организации ESRB (англ. Entertainment Software Rating Board). Эта ассоциация определяет рейтинг - компьютерных игр и присваивает им подходящую возрастную категорию.

# План анализа:

## 1. Изучение общей информации по датасету

## 2. Подготовка данных:
- Замена названий столбцов (приведение к нижнему регистру)
- Преобразование данных к нужным типам
- Обработка пропусков (при необходимости)

## 3. Анализ данных:
- Описание выпуска количества игр по годам
- Описание продаж в разные года по платформам
- Выделение лидирующих платформ по продажам, выбор нескольких потенциально прибыльных платформ
- Построение "ящика с усами" по глобальным продажам игр в разбивке по платформам
- Описание влияния на продажи отзывов пользователей и критиков внутри одной популярной платформы
- Распределение игр по жанрам
- Составление выводов по предыдущим подпунктам

## 4. Составление портрета пользователя по каждому региону:
- Для пользователя каждого региона необходимо будет определить:
    - Топ-5 самых популярных платформ
    - Топ-5 самых популярных жанров
    - Выявление влияния рейтинга ESRB на продажи по региону
    
## 5. Проверка гипотез:
- **Гипотеза №1:** средние пользовательские рейтинги платформ Xbox One и PC одинаковые
- **Гипотеза №2:** Средние пользовательские рейтинги жанров Action и Sports разные

## 6. Формулирование общего вывода.
