from setuptools import setup, find_packages

setup(
    name='django-sage-painless',
    packages=find_packages(exclude=['tests*']),
    package_data={'sage_painless/templates': ['*.txt']},
    include_package_data=True,
    version='1.10.0',
    description='django package for auto generating projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sage Team',
    author_email='mail@sageteam.org',
    url='https://github.com/sageteam-org/django-sage-painless',
    download_url='https://github.com/sageteam-org/django-sage-painless/archive/refs/tags/1.5.0.tar.gz',
    keywords=['django', 'python', 'generate', 'code generator'],
    install_requires=[
        'Django',
        'django-redis',
        'redis',
        'drf-yasg',
        'django-seed',
        'Faker',
        'autopep8',
        'django-sage-encrypt',
        'django-sage-streaming',
        'tox',
        'coverage'
    ]
)
