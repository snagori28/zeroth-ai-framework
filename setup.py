from setuptools import setup, find_packages

setup(
    name='zeroth',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'neo4j',
        'openai',
        'fastapi',
        'uvicorn',
        'pydantic'
    ],
    entry_points={
        'console_scripts': [
            'zeroth=cli_interface:main',
            'zeroth-api=api_interface:app'
        ]
    },
)
