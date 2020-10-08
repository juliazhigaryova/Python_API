import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy

# Илья, у меня возникли вопросы, помогите, пожалуйста, разобраться:
# 1.не очень получилось сделать список пользователей,почему-то такая реализация не работает,
# выдает 404, не понимаю, почему(enc_password я убрала)?
# 2. в методе user_parse не работают сразу два response.follow  - для подписчиков и подписок,
# не понримаю, почему и как тогда сделать сразу два запроса?

class InstacomSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = ['julia.developer', 'julia.zhigareva']
    insta_pwd = ['#PWD1', '#PWD2']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    followers = 'followers/'  # Пользователь, у которого собираем посты. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = 'eddbde960fed6bde675388aac39a3657'  # hash для получения данных по постах с главной страницы
    followers_hash = 'c76146de99bb02f6415203be841dd25a'  # hash для получения данных по постах с главной страницы
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        for user in self.insta_login:
                for pwd in self.insta_pwd:
                    yield scrapy.FormRequest(  # заполняем форму для авторизации
                        self.inst_login_link,
                        method='POST',
                        callback=self.user_parse,
                        formdata={'username': user, 'enc_password': pwd},
                        headers={'X-CSRFToken': csrf_token}
                    )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.insta_login}',
                callback=self.get_followings,
                cb_kwargs={'username': self.insta_login}
            )
            yield response.follow(
                f'/{self.insta_login}',
                callback=self.get_followers,
                cb_kwargs={'username': self.insta_login}
            )


    def user_followers_parse(self, response: HtmlResponse, user_id, username):
        j_data = json.loads(response.text)
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for user in followers:  # Перебираем подписчиков, собираем данные
            item = InstaparserItem(
                follower_id=user['node']['id'],
                user_id=user_id,
                photo=user['node']['profile_pic_url'],
                name=user['node']['full_name'],
                user_name=username,
                is_follower='true'
            )
            yield item  # В пайплайн


    def user_followings_parse(self, response: HtmlResponse, user_id, username):
        j_data = json.loads(response.text)
        followings = j_data.get('data').get('user').get('edge_follow').get('edges')
        for user in followings:  # Перебираем подписки, собираем данные
            item = InstaparserItem(
                following_id=user['node']['id'],
                user_id=user_id,
                photo=user['node']['profile_pic_url'],
                name=user['node']['full_name'],
                user_name=username,
                is_follower='false'
            )
            yield item  # В пайплайн

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text):
        matched = re.search(
            r'(\"id\":\"\d+\")', text
        ).group()
        s = matched.split(':')
        return int(s[1].strip('"'))


    def get_followers(self, response: HtmlResponse,username):

        user_id = self.fetch_user_id(response.text)
        variables = {'id': user_id,
                     'include_reel': 'true',
                     'fetch_mutual': 'true',
                     'first': 24}
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id}
        )

    def get_followings(self,response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text)
        variables = {'id': user_id,
                     'include_reel': 'true',
                     'fetch_mutual': 'false',
                     'first': 24}
        url_followings = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(variables)}'
        yield response.follow(
            url_followings,
            callback=self.user_followings_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id}
        )
