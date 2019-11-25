import os
import sys
import warnings

from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'konlpy',
    'lexrankr',
    'tensorflow',
]

# if os.name == "nt":
#     warnings.warn("See http://konlpy.org/en/v0.4.4/install/#id2 to properly install konlpy.", RuntimeWarning)
# elif sys.version_info < (3, ):
#     requirements.append('jpype1')
# else:
#     requirements.append('jpype1-py3')

setup(
    name="sentiment-analysis",
    version="0.0.2",
    license="MIT",
    author="Philip Kim",
    author_email="philip@mysterico.com",
    url="https://github.com/Mysterico/sentiment_analysis",
    description="Sentiment analysis for paragraph or sentence",
    packages=find_packages(exclude=['setup', 'test']),
    keywords=['nlp', 'korean'],
    python_requires='>=3',
    package_data = {
        'data' : [
            'sentiment_data_ko.xlsx'
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)