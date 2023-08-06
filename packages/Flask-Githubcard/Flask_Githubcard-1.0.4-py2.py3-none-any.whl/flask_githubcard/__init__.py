# -*- coding: utf-8 -*-
"""
flask_githubcard
:author: Jiang Wei <qq804022023@gmail.com>
:copyright: © 2021 Jiang Wei
:license: Apache Software License, see LICENSE for more details.
"""

from flask import current_app, url_for, Markup, Flask, Blueprint
import requests

SHIELDS_THEME = 'social'
GITHUB_STAR = f'https://img.shields.io/github/stars/weijiang1994/Blogin?style={SHIELDS_THEME}'
GITHUB_FORK = f'https://img.shields.io/github/forks/weijiang1994/Blogin?style={SHIELDS_THEME}'
GITHUB_WATCHER = f'https://img.shields.io/github/watchers/weijiang1994/Blogin?style={SHIELDS_THEME}'

USER_API = 'https://api.github.com/users/weijiang1994'
REPO_API = 'https://api.github.com/repos/weijiang1994/Blogin'


class _GithubCard(object):

    def __init__(self, theme):
        self.theme = theme

    @staticmethod
    def init_css(bootstrap=None, fontawesome=None, theme='default'):
        if bootstrap is None:
            bootstrap = url_for('githubcard.static', filename=f'css/bootstrap.min.{theme}.css')
        if fontawesome is None:
            # fontawesome = url_for('githubcard.static', filename='css/font-awesome.min.css')
            fontawesome = 'https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css'
        return Markup('''
        <link rel="stylesheet" href="%s"> \n <link rel="stylesheet" href="%s">
        <style>
            .mr-1{
                padding-right: 3px;
            }
            \n
            .avatar-s{
                width: 50px;
                height: 50px;
            }
        </style>
        ''' % (bootstrap, fontawesome))

    @staticmethod
    def init_js(jquery=None, bootstrap=None):
        if jquery is None:
            jquery = url_for('githubcard.static', filename='js/jquery-3.6.0.min.js')
        if bootstrap is None:
            bootstrap = url_for('githubcard.static', filename='js/bootstrap.min.js')
        return Markup(f'''
        <script src="{jquery}"></script>\n<script src="{bootstrap}"></script>
        ''')

    @staticmethod
    def generate_card(theme='default'):
        username = current_app.config.get('GITHUB_USERNAME', 'weijiang1994')
        repo_name = current_app.config.get('GITHUB_REPO', 'Blogin')

        user_api = USER_API.replace('weijiang1994', username)
        repo_api = REPO_API.replace('Blogin', repo_name).replace('weijiang1994', username)
        star = GITHUB_STAR.replace('weijiang1994', username).replace('Blogin', repo_name)
        fork = GITHUB_FORK.replace('weijiang1994', username).replace('Blogin', repo_name)
        watcher = GITHUB_WATCHER.replace('weijiang1994', username).replace('Blogin', repo_name)

        if theme == 'darkly':
            star = star.replace('social', 'flat-square')
            fork = fork.replace('social', 'flat-square')
            watcher = watcher.replace('social', 'flat-square')
        try:
            watcher = requests.get(watcher, timeout=30)
            star = requests.get(star, timeout=30)
            fork = requests.get(fork, timeout=30)
            user_info = requests.get(user_api, timeout=30)
            repo_info = requests.get(repo_api, timeout=30)
            avatar = user_info.json()['avatar_url']
            repo_desc = repo_info.json()['description']
            return Markup(f'''
                        <div class="card mb-3 mt-2">
                            <div class="card-header p-2 f-17">
                                <strong><i class="fa fa-github mr-1"></i>Github</strong>
                        </div>
                        <div  class="card-body p-2 f-15">
                            <div style="border-bottom: 1px solid rgba(58,10,10,0.19); margin-bottom: 5px;padding-bottom: 3px;" class="d-flex">
                                <a href="https://github.com/{username}/" target="_blank"><img class="avatar-s mr-1" id="githubAvatar" alt="avatar" src="{avatar}"></a>
                            <div class="ml-2 flex-grow-1">
                                <h5 class="mb-0"><b>{repo_name}</b></h5>
                                <small id="repoDesc">{repo_desc}</small>
                            </div>
                                <a class="btn btn-sm btn-light h-25 align-content-end" id="githubStar" href="https://github.com/{username}/{repo_name}" target="_blank">Star</a>
                            </div>
                            <div id="shield-svg" class="text-left pr-1 d-flex">
                                <div class="mr-1">
                                    {star.text}
                                </div>
                                <div class="mr-1">
                                    {fork.text}
                                </div>
                                <div class="mr-1">
                                    {watcher.text}
                                </div>
                            </div>
                        </div>
                    </div>
                    ''')
        except:
            return Markup(f'''
                                    <div class="card mb-3 mt-2">
                                        <div class="card-header p-2 f-17">
                                            <strong><i class="fa fa-github mr-1"></i>Github</strong>
                                    </div>
                                    <div  class="card-body p-2 f-15">
                                        <div style="border-bottom: 1px solid rgba(58,10,10,0.19); margin-bottom: 5px;padding-bottom: 3px;" class="d-flex">
                                            <a href="https://github.com/weijiang1994/" target="_blank"><img class="avatar-s mr-1" id="githubAvatar" alt="avatar" src="https://2dogz.cn/accounts/avatar/%E6%B8%85%E6%B0%B44.jpg"></a>
                                        <div class="ml-2 flex-grow-1">
                                            <h5 class="mb-0"><b>Blogin</b></h5>
                                            <small id="repoDesc">github信息获取失败,可能是网络原因或者请求受到了限制.</small>
                                        </div>
                                            <a class="btn btn-sm btn-light h-25 align-content-end" id="githubStar" href="https://github.com/weijiang1994/Blogin" target="_blank">Star</a>
                                        </div>
                                        <div id="shield-svg" class="text-left pr-1 d-flex">
                                            <div class="mr-1">
                                                {star.text}
                                            </div>
                                            <div class="mr-1">
                                                {fork.text}
                                            </div>
                                            <div class="mr-1">
                                                {watcher.text}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                ''')

    def get_raw_data(self):
        username = current_app.config.get('GITHUB_USERNAME', 'weijiang1994')
        repo_name = current_app.config.get('GITHUB_REPO', 'Blogin')

        user_api = USER_API.replace('weijiang1994', username)
        repo_api = REPO_API.replace('Blogin', repo_name).replace('weijiang1994', username)
        star = GITHUB_STAR.replace('weijiang1994', username).replace('Blogin', repo_name)
        fork = GITHUB_FORK.replace('weijiang1994', username).replace('Blogin', repo_name)
        watcher = GITHUB_WATCHER.replace('weijiang1994', username).replace('Blogin', repo_name)

        if self.theme == 'darkly':
            star = star.replace('social', 'flat-square')
            fork = fork.replace('social', 'flat-square')
            watcher = watcher.replace('social', 'flat-square')
        try:
            watcher = requests.get(watcher, timeout=30)
            star = requests.get(star, timeout=30)
            fork = requests.get(fork, timeout=30)
            user_info = requests.get(user_api, timeout=30)
            repo_info = requests.get(repo_api, timeout=30)
            avatar = user_info.json()['avatar_url']
            repo_desc = repo_info.json()['description']
            return {
                'tag': 1,
                'watcher': watcher.text,
                'star': star.text,
                'fork': fork.text,
                'avatar': avatar,
                'repo_desc': repo_desc
            }
        except:
            return {
                'tag': 0,
                'info': 'Connection timeout, please check your network.'
            }


class GithubCard(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['githubcard'] = _GithubCard
        app.context_processor(self.context_processor)

        app.config.setdefault('GITHUB_STAR', GITHUB_STAR)
        app.config.setdefault('GITHUB_FORK', GITHUB_FORK)
        app.config.setdefault('GITHUB_WATCHER', GITHUB_WATCHER)
        app.config.setdefault('USER_API', USER_API)
        app.config.setdefault('REPO_API', REPO_API)

        blueprint = Blueprint('githubcard', __name__,
                              static_folder='static',
                              static_url_path='/githubcard' + app.static_url_path)
        app.register_blueprint(blueprint)
        self.root_path = blueprint.root_path

    @staticmethod
    def context_processor():
        return {
            'githubcard': current_app.extensions['githubcard']
        }

    def create(self, theme='default'):
        return current_app.extensions['githubcard'](theme)
