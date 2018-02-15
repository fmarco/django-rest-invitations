from setuptools import setup, find_packages


setup(
    name='django-rest-invitations',
    version='0.1.0',
    author='Marco Federighi',
    author_email='federighi.marco@gmail.com',
    url='http://github.com/fmarco/django-rest-invitations',
    description='Create a set of REST API endpoints to handle invitations',
    packages=find_packages(),
    keywords=['django', 'invitation', 'django-allauth', 'invite', 'rest', 'django-rest-framework', 'drf', 'invitations'],
    zip_safe=False,
    install_requires=[
        'djangorestframework>=3.7.7',
        'django-invitations==1.9.2'
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