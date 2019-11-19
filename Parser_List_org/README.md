# Тестовое задание:
Спарсить отзывы с сайта.
https://http://www.list-org.com 

Юридическое наименование, Руководитель, Дата регистрации, Статус, ИНН, КПП, ОГРН.

На вход передается ссылка типа:
https://http://www.list-org.com/company/4868135

Parser
Simple parser to get reviews from bookmaker-ratings.
Depends on:

- python 3.6
- selenium==3.141.0
- urllib3==1.25.7


`pip install -r requirements.txt`

example:

`python Parcer_list_org.py https://http://www.list-org.com/company/4868135`

Pay your attention
`path = "C:\chromedriver.exe"`
