from setuptools import setup, find_packages


setup(
    name='django-rest-invitations',
    version='0.1.2',
    author='Marco Federighi',
    author_email='federighi.marco@gmail.com',
    url='http://github.com/fmarco/django-rest-invitations',
    description='Create a set of REST API endpoints to handle invitations',
    packages=find_packages(),
    keywords=['django', 'invitation', 'django-allauth', 'invite', 'rest', 'django-rest-framework', 'drf', 'invitations'],
    zip_safe=False,
    install_requires=[
        'djangorestframework>=3.10',
        'django-invitations==1.9.3'
    ],
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)