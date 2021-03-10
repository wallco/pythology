from setuptools import find_packages, setup


setup(
    name="pythology",
    packages=find_packages(include=['pythology']),
    version="1.0.3",
    description="Library dedicated to epidemiological compartmental modeling",
    long_description="""Pythology is a scientific python package with the purpose of simplifying the implementation
                        of epidemiological compartmental models.
                        
                        Using object-oriented concepts, users can build each compartment and each transfer rate between compartments
                        in a much more high-level way than implementing the model by hand, only needing to specify each of these elements' characteristics.
                        
                        Thus, the package aims to eliminate the need for advanced mathematical 
                        knowledge and allow the user to focus more on the conceptual and biological aspect with freedom
                        to explore more model and parameter possibilities.""",
    long_description_content_type="text/plain",
    author="Wallace Correa de Moura Filho",
    author_email='wallacecmf@poli.ufrj.br',
    license="MIT",
    install_requires=['numpy', 'matplotlib', 'scipy'],
    python_requires='>=3.8',
    url=''
)