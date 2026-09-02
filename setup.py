from setuptools import setup, find_packages

setup(
    name="antigravity-skills-move",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "antigravity-skills-move=antigravity_skills_move.cli:main",
            "skills-move=antigravity_skills_move.cli:main",
        ],
    },
)
