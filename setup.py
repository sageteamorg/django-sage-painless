from setuptools import setup, find_packages

setup(
    name='django-sage-painless',
    packages=find_packages(exclude=['tests*']),
    package_data={'sage_painless/templates': ['*.txt']},
    include_package_data=True,
    version='1.7.0',
    license='GNU',
    description='django package for auto generating projects',
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
        'django-sage-streaming'
    ]
)
