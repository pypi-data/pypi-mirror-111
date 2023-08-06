# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s2terminal_lex_rank_summarizer']

package_data = \
{'': ['*']}

install_requires = \
['Janome>=0.4.1,<0.5.0',
 'fire>=0.4.0,<0.5.0',
 'numpy>=1.21.0,<2.0.0',
 'sumy>=0.8.1,<0.9.0',
 'tinysegmenter>=0.4,<0.5']

entry_points = \
{'console_scripts': ['lex-rank-summarizer = '
                     's2terminal_lex_rank_summarizer.main:main']}

setup_kwargs = {
    'name': 's2terminal-lex-rank-summarizer',
    'version': '0.1.2',
    'description': 'This is a CLI tool that uses LexRank to translate sentences in 3 lines.',
    'long_description': '# LexRank Summarizer\n<a href="https://hub.docker.com/r/s2terminal/lex-rank-summarizer"><img src="https://img.shields.io/docker/cloud/build/s2terminal/lex-rank-summarizer.svg" alt="dockerhub"/></a> [![PyPI version](https://badge.fury.io/py/s2terminal-lex-rank-summarizer.svg)](https://badge.fury.io/py/s2terminal-lex-rank-summarizer?style=flat-square&logo=appveyor)\n\nThis is a CLI tool that uses LexRank to translate sentences in 3 lines.\n\n## Usage\n### Docker\n```\n$ docker run --rm s2terminal/lex-rank-summarizer \\\n  \'メロスは激怒した。必ず、かの邪智暴虐の王を除かなければならぬ と決意した。メロスには政治がわからぬ。メロスは、村の牧人である。笛を吹き、羊と遊んで暮して来た。けれども邪悪に対しては、人一倍に敏感であっ た。きょう未明メロスは村を出発し、野を越え山越え、十里はなれた此のシラクスの市にやって来た。メロスには父も、母も無い。女房も無い。十六の、 内気な妹と二人暮しだ。この妹は、村の或る律気な一牧人を、近々、花婿として迎える事になっていた。結婚式も間近かなのである。メロスは、それゆえ 、花嫁の衣裳やら祝宴の御馳走やらを買いに、はるばる市にやって来たのだ。先ず、その品々を買い集め、それから都の大路をぶらぶら歩いた。\'\n```\n\n```\nメロスは激怒した。\nメロスは、村の牧人である。\nきょう未明メロスは村を出発し、野を越え山越え、十里はなれた此のシラクスの市にやって来た。\n```\n\n### Python\n```\n$ pip install s2terminal-lex-rank-summarizer\n$ lex-rank-summarizer \\\n  \'メロスは激怒した。必ず、かの邪智暴虐の王を除かなければならぬ と決意した。メロスには政治がわからぬ。メロスは、村の牧人である。笛を吹き、羊と遊んで暮して来た。けれども邪悪に対しては、人一倍に敏感であっ た。きょう未明メロスは村を出発し、野を越え山越え、十里はなれた此のシラクスの市にやって来た。メロスには父も、母も無い。女房も無い。十六の、 内気な妹と二人暮しだ。この妹は、村の或る律気な一牧人を、近々、花婿として迎える事になっていた。結婚式も間近かなのである。メロスは、それゆえ 、花嫁の衣裳やら祝宴の御馳走やらを買いに、はるばる市にやって来たのだ。先ず、その品々を買い集め、それから都の大路をぶらぶら歩いた。\'\n```\n\n## Development\n```\n$ docker-compose up\n```\n\nand use [VS Code Remote Container](https://code.visualstudio.com/docs/remote/containers)\n\n```\n$ docker-compose exec app poetry run lex-rank-summarizer \'おはよう。こんにちは。こんばんは。\'\n```\n\n### Testing\n```\n$ docker-compose exec app poetry run pytest\n```\n\n## License\n[MIT](LICENSE)\n\n## References\n- [Python: LexRankで日本語の記事を要約する \\- け日記](https://ohke.hateblo.jp/entry/2018/11/17/230000)\n- [図書カード：走れメロス](https://www.aozora.gr.jp/cards/000035/card1567.html)\n',
    'author': 's2terminal',
    'author_email': 'suzuki.sh@s2terminal.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s2terminal/lex-rank-summarizer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
