
# [Telegram Bot](https://t.me/english_prus_bot) для изучения английского языка      

## Описание
Этот Telegram бот создан для русскоговорящих пользователей, желающих улучшить свои знания английского языка. Бот включает мощные инструменты для учеников и администратора (учителя), что делает процесс обучения эффективным и организованным.

### Уникальные особенности:
- **Интервальное повторение:** Адаптивное интервальное повторение помогает запоминать слова быстрее.
- **Грамматические тесты:** Регулярные тесты помогают закрепить грамматические знания.
- **Напоминания:** Пользователи могут устанавливать персонализированные напоминания для занятий.
- **Поддержка администратора:** Учителя могут управлять процессом обучения через административную панель и получать уведомления о ключевых событиях.
- **Режим Hard Mode для изучения слов:** Экспериментальный режим, добавленный для более сложного изучения слов, что делает обучение более интенсивным.

## Основные функции для учеников
- **Изучение слов с интервальным повторением.**
- **Youglish ссылки:** Встроенный построитель ссылок для Youglish позволяет пользователям легко просматривать произношение слов в реальном контексте.
- **Тесты по грамматике.**
- **Напоминания о занятиях.**
- **Статистика по изучению слов:** Возможность отслеживать прогресс по каждой теме:
  - Для изучения сегодня.
  - Всего слов в теме.
  - В активном изучении.
  - Изучено.
  - % правильных ответов.

## Функции для администратора/учителя
Административная панель предоставляет следующие возможности:
- **Добавление сетов слов:** Создание наборов слов для учеников.
- **Добавление тестов по грамматическим темам.**
- **Индивидуальная настройка:** Добавление и удаление слов для отдельных учеников.
- **Просмотр статистики учеников:** Прогресс учеников доступен в виде графиков.
- **Общая статистика по боту:** Отчеты по активности пользователей за различные периоды.
- **Детальная информация по каждому ученику:** Имя, Telegram username, ID, количество баллов, дата регистрации, время напоминаний, часовой пояс.
- **Удаление пользователей.**
- **Планирование рассылок.**
- **Уведомления:**
  - При запуске и остановке бота.
  - О регистрации новых пользователей.
  - О добавлении учеником новых слов.
  - О прохождении учеником упражнений по грамматике с отображением статистики.

## Планы по улучшению
- [ ] Сделать наиболее изученные слова более приоритетными в изучении.

## Технологический стек
Бот построен на современных технологиях:
- **Python 3.11 slim**
- **Aiogram 3.13.1** — асинхронная работа с Telegram API.
- **Aiosqlite 0.20.0** и **Asyncpg 0.29.0** — работа с базами данных (SQLite и PostgreSQL).
- **Redis 5.1.1** — хранение состояний и кэш.
- **APScheduler 3.10.4** — планирование задач.
- **Environs 11.0.0** — управление конфиденциальной информацией.

---

  # Telegram Bot for Learning English
[Try](https://t.me/english_prus_bot)
## Description
This Telegram bot is designed for Russian-speaking users who want to improve their English language skills. The bot provides powerful tools for both students and administrators (teachers), making the learning process effective and organized.

### What makes this bot unique?
- **Spaced repetition:** Adaptive spaced repetition helps users memorize words faster.
- **Grammar tests:** Regular tests help reinforce grammar knowledge.
- **Reminders:** Users can set personalized reminders to study.
- **Administrator support:** Teachers can manage the learning process through an admin panel and receive notifications about key events.
- **Hard Mode for Vocabulary Learning:** An experimental mode for a more challenging word study experience.

## Key Features for Students
- **Word learning with spaced repetition.**
- **Youglish Links:** Built-in link builder to Youglish allows users to view word pronunciation in real-life context.
- **Grammar tests.**
- **Study reminders.**
- **Word learning statistics:** Users can track their progress for each topic:
  - Words to study today.
  - Total words in the topic.
  - Actively learning.
  - Words learned.
  - % correct answers.
  

## Features for Administrator/Teacher/Tutor
The admin panel provides the following features:
- **Adding word sets:** Create word sets for students to learn.
- **Adding grammar tests.**
- **Individual customization:** Add and remove specific words for individual students.
- **View students statistics:** Track student progress via charts.
- **General bot usage statistics:** Reports on user activity over various time periods.
- **Detailed user information:** Name, Telegram username, ID, score points (awarded for completing tasks), registration date, reminder times, and time zone.
- **User deletion.**
- **Planning broadcasts:** Send scheduled messages to users.
- **Notifications:**
  - Bot start/stop notifications.
  - New user registration notifications.
  - Notifications when a student adds new words for learning.
  - Notifications with statistics when a student completes a grammar exercise.

## Planned Improvements
- [ ] Make the most learned words a priority in the study process.

## Tech Stack
This bot is built using modern technologies:
- **Python 3.11 slim**
- **Aiogram 3.13.1** — asynchronous Telegram API.
- **Aiosqlite 0.20.0** and **Asyncpg 0.29.0** — asynchronous databases (SQLite and PostgreSQL).
- **Redis 5.1.1** — state storage and caching.
- **APScheduler 3.10.4** — scheduling tasks like sending notifications.
- **Environs 11.0.0** — secure environment variable management.
