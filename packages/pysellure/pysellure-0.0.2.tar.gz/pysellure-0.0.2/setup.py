import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Python/Selenium/Allure methods'
LONG_DESCRIPTION = long_description

setuptools.setup(
    name='pysellure',
    version=VERSION,
    author='Dmitry Vinogradov',
    author_email='dvinogradov@htsts.ru',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=['python', 'selenium', 'allure', 'autotesting'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
