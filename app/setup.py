from setuptools import setup, find_packages

setup(
    name='agent-connect-app',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.0.3',
        'flask_session==0.4.0',
        'flask_wtf==0.15.1',
        'pymongo==4.7.2',
        'python-dotenv==1.0.1',
        'Werkzeug==2.0.3',
        'pandas==1.3.4',
        'gunicorn==20.1.0',
    ],
    entry_points={
        'console_scripts': [
            'run=app.run:main',
        ],
    },
)
