from setuptools import setup, find_packages

setup(
    name='zeroth',
    version='0.1',
    packages=find_packages(include=["core"]),
    py_modules=["cli_interface", "api_interface", "config"],
    install_requires=[
        'neo4j',
        'openai',
        'fastapi',
        'uvicorn',
        'pydantic',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'zeroth=cli_interface:main',
            'zeroth-api=api_interface:app'
        ]
    },
)
