#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'Catgirl-Dungeon',
        version = '1.0.dev1',
        description = '',
        long_description = 'Catgirl-Dungeon',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = '',

        url = '',
        project_urls = {},

        scripts = [],
        packages = [],
        namespace_packages = [],
        py_modules = [
            'JSONParser',
            'model.Rarity',
            'model.character.Character',
            'model.character.CharacterLoadout',
            'model.character.DynamicStat',
            'model.character.ExperienceStat',
            'model.database.DBItemBuilder',
            'model.database.DBSkillBuilder',
            'model.database.DatabaseFetcher',
            'model.effect.Effect',
            'model.effect.EffectTag',
            'model.effect.EffectType',
            'model.effect.EffectsList',
            'model.item.Item',
            'model.item.ItemSlot',
            'model.item.ItemTag',
            'model.openworld.Tile',
            'model.skill.Skill',
            'model.skill.SkillTag',
            'model.visualentity.ButtonEntity',
            'model.visualentity.CombatEnemyEntity',
            'model.visualentity.DrawingEntity',
            'model.visualentity.ImageEntity',
            'model.visualentity.Tag',
            'model.visualentity.TextEntity',
            'model.visualentity.TransparentButtonEntity',
            'model.visualentity.VisualEntity',
            'openWorld',
            'repository.ItemRepository',
            'util.IllegalArgumentException',
            'util.InvalidOperationException'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
