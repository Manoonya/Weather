# Прогноз погоды для маршрута
Обработанные ошибки: 
1. **Пустой ввод:** Если пользователь оставляет поля пустыми, отображается сообщение с восклицательным знаком: "Заполните это поле." 
2. **Некорректный город:** Если город не найден, пользователь увидит: "Город 'введенный пользователем некорректный город' не найден. Введите название города корректно."
3. **Ошибка сети:** Если нет соединения с интернетом, выводится: "Ошибка подключения к серверу. Проверьте сеть."
4. **Проблемы с API:** Если API недоступно или возвращает ошибку, отображается сообщение: "Не удалось получить данные о погоде для города 'введенный пользователем некорректный город'. "
Тестирование: 
1. Проведена проверка работы сервиса на различных сценариях ввода:
   - Корректный ввод.
   - Некорректный ввод.
   - Пустой ввод.
   - Отключённый интернет.
2. Всё работает корректно, ошибки обрабатываются, и пользователю предоставляется информативная обратная связь и качественная визуалиция появившихся ошибок. 
