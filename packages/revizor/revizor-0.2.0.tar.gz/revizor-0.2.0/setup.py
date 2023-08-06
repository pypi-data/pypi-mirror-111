# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['revizor']

package_data = \
{'': ['*'], 'revizor': ['model/*']}

install_requires = \
['flair>=0.8.0,<0.9.0', 'razdel>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'revizor',
    'version': '0.2.0',
    'description': 'Ecommerce product title recognition package',
    'long_description': '# revizor [![Test & Lint](https://github.com/bureaucratic-labs/revizor/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/bureaucratic-labs/revizor) [![codecov](https://codecov.io/gh/bureaucratic-labs/revizor/branch/main/graph/badge.svg?token=YHND3N25LI)](https://codecov.io/gh/bureaucratic-labs/revizor)\n\nThis package solves task of splitting product title string into components, like `type`, `brand`, `model` and `vendor_code`.  \nImagine classic named entity recognition, but recognition done on product titles.\n\n## Install\n\n`revizor` requires python **3.8+** version **on Linux or macOS**, Windows **isn\'t supported** now, but contributions are welcome.\n\n```bash\n$ pip install revizor\n```\n\n## Usage\n\n```python\nfrom revizor.tagger import ProductTagger\n\ntagger = ProductTagger()\nproduct = tagger.predict("Смартфон Apple iPhone 12 Pro 128 gb Gold (CY.563781.P273)")\n\nassert product.type == "Смартфон"\nassert product.brand == "Apple"\nassert product.model == "iPhone 12 Pro"\nassert product.vendor_code == "CY.563781.P273"\n```\n\n## Boring numbers\n\nActually, just output from flair training log:\n```\nCorpus: "Corpus: 138959 train + 15440 dev + 51467 test sentences"\nResults:\n- F1-score (micro) 0.8843\n- F1-score (macro) 0.8766\n\nBy class:\nVENDOR_CODE    tp: 9893 - fp: 1899 - fn: 3268 - precision: 0.8390 - recall: 0.7517 - f1-score: 0.7929\nBRAND          tp: 47977 - fp: 2335 - fn: 514 - precision: 0.9536 - recall: 0.9894 - f1-score: 0.9712\nMODEL          tp: 35187 - fp: 11824 - fn: 9995 - precision: 0.7485 - recall: 0.7788 - f1-score: 0.7633\nTYPE           tp: 25044 - fp: 637 - fn: 443 - precision: 0.9752 - recall: 0.9826 - f1-score: 0.9789\n```\n\n## Dataset\n\nModel was trained on automatically annotated corpus. Since it may be affected by DMCA, we\'ll not publish it.  \nBut we can give hint on how to obtain it, don\'t we?  \nDataset can be created by scrapping any large marketplace, like goods, yandex.market or ozon.  \nWe extract product title and table with product info, then we parse brand and model strings from product info table.  \nNow we have product title, brand and model. Then we can split product title by brand string, e.g.:\n\n```python\nproduct_title = "Смартфон Apple iPhone 12 Pro 128 Gb Space Gray"\nbrand = "Apple"\nmodel = "iPhone 12 Pro"\n\nproduct_type, product_model_plus_some_random_info = product_title.split(brand)\n\nproduct_type # => \'Смартфон\'\nproduct_model_plus_some_random_info # => \'iPhone 12 Pro 128 Gb Space Gray\'\n```\n\n## License\n\nThis package is licensed under MIT license.\n',
    'author': 'Dima Veselov',
    'author_email': 'd.a.veselov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bureaucratic-labs/revizor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
