from setuptools import setup, find_packages

setup(
    name="trading_bot_ultimate",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ccxt",
        "python-dotenv",
        "pytest",
        "pytest-asyncio",
        "pytest-cov"
    ],
)
