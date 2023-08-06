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
    'version': '0.2.0',
    'description': 'Support physics simulation',
    'long_description': '# manim-physics (Under Active Development)\n## Introduction\nThis is a 2D physics simulation plugin that allows you to generate complicated scenes in various branches of Physics such as rigid mechanics, electromagnetism, wave etc.\n\nContributors: [**pdcxs**](https://github.com/pdcxs), [**Matheart**](https://github.com/Matheart)\n\n## Installation\nFollow this guide: https://docs.manim.community/en/stable/installation/plugins.html?highlight=plugin. \n\n**Warnings: Please do not directly clone the github repo! The repo is still under development and it is not a stable version, download manim-physics through pypi.**\n\n## Usage\nIn order to use `rigid_mechanics.py`, you should be familar with pymunk. You could check [the official documentation](http://www.pymunk.org/en/latest/pymunk.html) of pymunk for reference. There is also a good [Youtube tutorial](https://youtu.be/pRk---rdrbo ) to let you better understand pymunk.\n\n## Contribution Guidelines\nThe manim-physics plugin contains objects that are classified into **several main branches**, now including rigid mechanics simulation, electromagnetism and wave. \n\nIf you want to add more objects to the plugin, The classes of the objects should be placed in the python file of corresponding branch, for example, `wave.py`, and place it under the folder src\\manim_physics. The tests of objects should be named as `test_thefilename.py` such as `test_wave.py`, with some documentation, so the maintainer of this repo could ensure that it runs as expected.\n\n## A simple Example \n\n```py\nclass OneObjectsFalling(Scene):\n    def construct(self):\n        space = Space(dt = 1 / self.camera.frame_rate) \n        # space is the basic unit of simulation (just like scene)\n        # you can add rigid bodies, shapes and joints to it \n        # and then step them all forward together through time\n        self.add(space)\n\n        circle = Circle().shift(UP).set_fill(RED, 1).shift(DOWN + RIGHT)\n        circle.body = pymunk.Body() # add a rigid body to the circle\n        circle.body.position = \\\n            circle.get_center()[0], \\\n            circle.get_center()[1]\n        circle.shape = pymunk.Circle(\n            body = circle.body,\n            radius = circle.width / 2\n        ) # set the shape of the circle in pymunk\n        circle.shape.elasticity = 0.8\n        circle.shape.density = 1\n        circle.angle = 0\n\n        ground = Rectangle(width = 8, height = 0.1, color = GREEN).set_fill(GREEN, 1)\n        ground.shift(3.5*DOWN)\n        ground.body = space.space.static_body \n        # static body means the object keeps stationary even after collision\n        ground.shape = pymunk.Segment(ground.body, (-4, -3.5), (4, -3.5), 0.1)\n        ground.shape.elasticity = 0.99\n        ground.shape.friction = 0.8\n        self.add(ground)\n\n        self.add(circle)\n        space.add_body(circle)\n        space.add_body(ground)\n\n        space.add_updater(step)\n        circle.add_updater(simulate)\n        self.wait(10)\n        # during wait time, the circle would move according to the simulate updater\n```\n\nhttps://user-images.githubusercontent.com/47732475/124072981-1519b580-da74-11eb-8f36-12652bfc80e0.mp4\n\n\n## Other beautiful animations based on manim-physics\n\nhttps://user-images.githubusercontent.com/47732475/123754200-38febf00-d8ed-11eb-937a-b93bc490f85a.mp4\n\n\n\nhttps://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4\n',
    'author': 'Matheart',
    'author_email': 'waautomationwong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
