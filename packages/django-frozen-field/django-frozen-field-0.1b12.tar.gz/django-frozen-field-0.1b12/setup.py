# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frozen']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0']

setup_kwargs = {
    'name': 'django-frozen-field',
    'version': '0.1b12',
    'description': 'Django model field used to store snapshot of data.',
    'long_description': '# Django Frozen Field\n\nDjango model custom field for storing a frozen snapshot of an object.\n\n## Principles\n\n* Behaves like a `ForeignKey` but the data is detached from the related object\n* Transparent to the client - it looks like the original object\n* The frozen object cannot be edited\n* The frozen object cannot be saved\n* Works even if original model is updated or deleted\n\n### Why not use DRF / Django serializers?\n\nThis library has one specific requirement that makes using the existing\nsolutions hard - to be able to decouple the frozen data from the model, such\nthat it can be altered or even deleted, and the data can still be used. We use\nthe model itself once, when we first save the data - from that point on the\nfield has no dependency on the original model, using intermediate dynamic\ndataclasses that represent the model as it was when the data was saved. This\npackage does reference a lot of the principles in both DRF and Django itself -\nand the structure of the serialized data is similar to that exported from the\nqueryset serializer.\n\n### Why not just store frozen data as JSON and be done with it?\n\nThis is probably a good / safe option for most codebases coming to the freezing\nof data for the first time, and we have a lot of ephemeral data stored in\n`JSONField` fields ourselves. However, migrating an existing project from\n`ForeignKey` to `JSONField`, along with all references to the data, templates,\netc., is painful. This package is designed to make the migration from \'fresh\' to\n\'frozen\' as simple as possible.\n\n## Package internals\n\nThe package includes three core modules, `serializers`, `models`, and `fields`,\nthat together control the serialization process.\n\n#### `frozen.models`\n\nThis module contains the engine of the package, which is a `FrozenObjectMeta`\ndataclass that is responsible for parsing Django model attributes, extracting\ndata and and creating the dynamic dataclasses used to represent a Django Model.\n\nYou should not need to use this module in your application.\n\n#### `frozen.serializers`\n\nThis module contains the `freeze_object` and `unfreeze_object` functions that\nare responsible for marshalling the serialized data between a Django Model\ninstance, a dynamic dataclass, and the serialized JSON..\n\nOn first save:\n\n    model >> dataclass >> dict\n\nOn first refresh:\n\n    dict >> dataclass\n\nOn subsequent saves:\n\n    dataclass >> dict\n\nYou should not need to use this module in your application.\n\n#### `frozen.fields`\n\nThis module contains the `FrozenObjectField` itself - it is the only part of the\npackage that should need to use yourself.\n\n#### Evolution of `FrozenObjectField`\n\nThe easiest way to understand why the field is structured as it is is to follow\nthe history:\n\n1. The first implementation serialized just non-related object fields (i.e.\n   excluded `ForeignKey` and `OneToOneField` attrs)\n1. The `include` and `exclude` arguments were added to control which fields were\n   serialized\n1. The `select_related` argument was added to enable the serialization of\n   top-level related objects (`ForeignKey` / `OneToOneField`)\n1. The `select_properties` argument was added to enable the serialization of\n   simple model properties (`@property`)\n1. Support was added for ORM-style paths (using the `__` delimiter) to enable\n   deep serialization beyond the top-level\n1. The `converters` argument was added to enable fine-tuning of the\n   deserialization process.\n\n## Usage\n\nA frozen field can be declared like a `ForeignKey`:\n\n```python\nclass Profile(Model):\n\n    address = FrozenObjectField(\n        Address,                         # The model being frozen\n        include=[],                      # defaults to all\n        exclude=["line_2"],              # defaults to none\n        select_related=[]                # add related fields\n        select_properties=["attr_name"]  # add model properties\n        converters={"field_name": func}  # custom deserializer\n    )\n\n...\n\n>>> profile.address = Address.objects.get(...)\n>>> profile.address\n"29 Acacia Avenue"\n>>> profile.save()\n>>> type(profile.address)\nAddress\n# When fetched from the db, the property becomes a frozen instance\n>>> profile.refresh_from_db()\n>>> type(profile.address)\ntypes.FrozenAddress\n>>> profile.address.id\n1\n>>> profile.address.line_1\n"29 Acacia Avenue"\n>>> profile.address.since\ndatetime.date(2011, 6, 4)\n>>> dataclasses.asdict(profile.address)\n{\n    "_meta": {\n        "pk": 1,\n        "model": "Address",\n        "frozen_at": "2021-06-04T18:10:30.549Z",\n        "fields": {\n            "id": "django.db.models.AutoField",\n            "line_1": "django.db.models.CharField",\n            "since": "django.db.models.DateField"\n        },\n        "properties": ["attr_name"]\n    },\n    "id": 1,\n    "line_1": "29 Acacia Avenue",\n    "since": "2011-06-04T18:10:30.549Z"\n    "attr_name": "hello"\n}\n>>> profile.address.json_data()\n{\n    "id": 1,\n    "line_1": "29 Acacia Avenue",\n    "since": "2011-06-04T18:10:30.549Z",\n    "attr_name": "hello"\n}\n>>> profile.address.id = 2\nFrozenInstanceError: cannot assign to field \'id\'\n>>> profile.address.save()\nAttributeError: \'FrozenAddress\' object has no attribute \'save\'\n```\n\n### Controlling serialization\n\nBy default only top-level attributes of an object are frozen - related objects\n(`ForeignKey`, `OneToOneField`) are ignored. This is by design - as deep\nserialization of recursive relationships can get very complex very quickly, and\na deep serialization of an object tree is not recommended. This library is\ndesigned for the simple \'freezing\' of basic data. The recommended pattern is to\nflatten out the parts of the object tree that you wish to record. You can\ncontrol which top-level fields are included in the frozen data using the\n`include` and `exclude` arguments. Note that these are mutually exclusive - by\ndefault both are an empty list, which results in all top-level non-related\nattributes being serialized. If `included` is not empty, then *only* the fields\nin the list are serialized. If `excluded` is not empty then all fields *except*\nthose in the list are serialized.\n\nThat said, there is support for related object capture using the\n`select_related` argument.\n\nThe `select_properties` argument can be used to add model properties (e.g.\nmethods decorated with `@property`) to the serialization. NB this currently does\nno casting of the value when deserialized (as it doesn\'t know what the type is),\nso if your property is a date, it will come back as a string (isoformat). If you\nwant it to return a `date` you will want to use converters.\n\nThe `converters` argument is used to override the default conversion of the JSON\nback to something more appropriate. A typical use case would be the casting of a\nproperty which has no default backing field to use. In this case you could use\nthe builtin Django `parse_date` function\n\n```python\nfield = FrozenObjectField(\n    Profile,\n    include=[],\n    exclude=[],\n    select_related=[],\n    select_properties=["date_registered"],\n    converters={"date_registered": parse_date}\n)\n```\n\n## How it works\n\nThe internal wrangling of a Django model to a JSON string is done using dynamic\ndataclasses, created on the fly using the `dataclasses.make_dataclass` function.\nThe new dataclass contains one fixed property, `meta`, which is itself an\ninstance of a concrete dataclass, `FrozenObjectMeta`. This ensures that each\nserialized blob contains enought original model field metadata to be able to\ndeserialize the JSONField back into something that resembles the original. This\nis required because the process of serializing the data as JSON will convert\ncertain unsupported datatypes (e.g. `Decimal`, `float`, `date`, `datetime`,\n`UUID`) to string equivalents, and in order to deserialize these values we need\nto know what type the original value was. This is very similar to how Django\'s\nown `django.core.serializers` work.\n\n#### Running tests\n\nThe tests use `pytest` as the test runner. If you have installed the `poetry`\nevironment, you can run them using:\n\n```\n$ poetry run pytest\n```\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-frozen-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
