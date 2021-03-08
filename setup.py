from setuptools import find_packages, setup


setup(
    name="pythology",
    packages=find_packages(include=['pythology']),
    version="1.0.0",
    description="Library dedicated to epidemiological compartmental modeling",
    author="Wallace Correa de Moura Filho",
    author_email='wallacecmf@poli.ufrj.br',
    license="MIT",
    install_requires=['numpy'],
    python_requires='>=3.8',
    url=''
)