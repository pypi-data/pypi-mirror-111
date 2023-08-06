# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_physics']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.6.0', 'pymunk>=6.0.0,<7.0.0']

entry_points = \
{'manim.plugins': ['manim_physics = manim_physics']}

setup_kwargs = {
    'name': 'manim-physics',
    'version': '0.2.1',
    'description': 'Support physics simulation',
    'long_description': '# manim-physics (Under Active Development)\n## Introduction\nThis is a 2D physics simulation plugin that allows you to generate complicated scenes in various branches of Physics such as rigid mechanics, electromagnetism, wave etc.\n\nContributors: [**pdcxs**](https://github.com/pdcxs), [**Matheart**](https://github.com/Matheart), [**Iced-Tea3**](https://github.com/Iced-Tea3)\n\n## Installation\nFollow this guide: https://docs.manim.community/en/stable/installation/plugins.html?highlight=plugin. \n\n**Warnings: Please do not directly clone the github repo! The repo is still under development and it is not a stable version, download manim-physics through pypi.**\n\n## Usage\nIn order to use `rigid_mechanics.py`, you should be familiar with pymunk. You could check [the official documentation](http://www.pymunk.org/en/latest/pymunk.html) of pymunk for reference. There is also a good [Youtube tutorial](https://youtu.be/pRk---rdrbo ) to let you better understand pymunk.\n\n## Contribution Guidelines\nThe manim-physics plugin contains objects that are classified into **several main branches**, now including rigid mechanics simulation, electromagnetism and wave. \n\nIf you want to add more objects to the plugin, The classes of the objects should be placed in the python file of corresponding branch, for example, `wave.py`, and place it under the folder src\\manim_physics. The tests of objects should be named as `test_thefilename.py` such as `test_wave.py`, with some documentation, so the maintainer of this repo could ensure that it runs as expected.\n\n## A simple Example \n\n```py\n# use a SpaceScene to utilize all specific rigid-mechanics methods\nclass TestScene(SpaceScene):\n    def construct(self):\n        circle = Circle().set_fill(RED, 1).shift(RIGHT)\n        ground = Line(LEFT*4,RIGHT*4,color=GREEN).shift(DOWN*3.5)\n        self.add(circle,ground)\n\n        self.make_rigid_body(circle) # Mobjects will move with gravity\n        self.make_static_body(ground) # Mobjects will stay in place\n        self.wait(10)\n        # during wait time, the circle would move according to the simulate updater\n```\n\nhttps://user-images.githubusercontent.com/47732475/124072981-1519b580-da74-11eb-8f36-12652bfc80e0.mp4\n\n\n## Other beautiful animations based on manim-physics\n\n\nhttps://user-images.githubusercontent.com/47732475/124342625-baa96200-dbf7-11eb-996a-1f27b3625602.mp4\n\nhttps://user-images.githubusercontent.com/47732475/124344045-c0587500-dc02-11eb-8fd6-afc1e5c658bb.mp4\n\n\n\nhttps://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4\n\n## Changelog\n### **v0.2.1 2021.07.03**\n#### New objects\n- **Electromagnetism**: Charge, ElectricField, Current, CurrentMagneticField, BarMagnet, and BarMagnetField\n- **Wave**: LinearWave, RadialWave, StandingWave\n\n#### Bugfixes\n- Fix typo\n\n#### Improvements\n- Simplify rigid-mechanics\n\n### **v0.2.0 2021.07.01**\n#### Breaking Changes\nObjects in the manim-physics plugin are classified into several **main branches** including rigid mechanics simulation, electromagnetism and wave.',
    'author': 'Matheart',
    'author_email': 'waautomationwong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Matheart/manim-physics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
