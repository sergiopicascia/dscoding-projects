# Dependency Management With Python Poetry

When your Python project relies on external packages, you need to make sure you’re using the right version of each package. After an update, a package might not work as it did before the update. A dependency manager like Python **Poetry** helps you specify, install, and resolve external packages in your projects. This way, you can be sure that you always work with the right dependency version on every machine.

While this tutorial focuses on dependency management, Poetry can also help you with [building and packaging](https://python-poetry.org/docs/cli/#build) projects. If you want to share your work, then you can even [publish](https://python-poetry.org/docs/cli/#publish) your Poetry project to the [Python Packaging Index (PyPI)](https://pypi.org/).

# Prerequisites

To complete this tutorial and get the most out of it, you should have a basic understanding of [virtual environments](https://realpython.com/python-virtual-environments-a-primer/), [modules and packages](https://realpython.com/python-modules-packages/), and `[pip](https://realpython.com/what-is-pip/)`.

## Relevant Terminology

If you’ve ever used an `import` statement in one of your Python scripts, then you’ve worked with **modules**. Some of these modules might have been Python files you wrote on your own. Others could have been **built-in** modules, like [datetime](https://realpython.com/python-datetime/). However, sometimes what Python provides isn’t enough. That’s when you might turn to external, packaged modules. When your Python code relies on external modules, you can say that these **packages** are **dependencies** of your project.

### **Python Poetry Installation**

To use Poetry in your command line, you should install it system-wide. If you just want to try it out, then you can install it into a virtual environment using `[pip](https://pypi.org/project/poetry/)`. But you should try this method with caution because Poetry will install its own dependencies, which can conflict with other packages you’re using in your project.

The recommended way to [install Poetry](https://python-poetry.org/docs/#installation) is by using the official `install-poetry` script. You can either download and run this [Python file](https://github.com/python-poetry/poetry/blob/master/install-poetry.py) manually or select your operating system below to use the appropriate command:

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
Retrieving Poetry metadata

# Welcome to Poetry!

This will download and install the latest version of Poetry,
a dependency and package manager for Python.

It will add the `poetry` command to Poetry's bin directory, located at:

/Users/lizzy/.local/bin

You can uninstall at any time by executing this script with the --uninstall option,
and these changes will be reverted.

Installing Poetry (1.5.1): Done

Poetry (1.5.1) is installed now. Great!

You can test that everything is set up by executing:

`poetry --version`
```

In the output, you should see a message that the installation is complete. You can run `poetry --version` in your terminal to see if `poetry` works. This command will display your current Poetry version. If you want to update Poetry, then you can run `poetry self update`.

# **Get Started With Python Poetry**

With Poetry installed, it’s time to see how Poetry works. In this section, you’ll learn how to start a fresh Poetry project and how to add Poetry to an existing project. You’ll also see the project structure and inspect the `pyproject.toml` file.

## **Create a New Poetry Project**

You can create a new Poetry project by using the `new` command and a project name as an argument. In this tutorial, the project is called `generali-poetry`. Create the project, and then move into the newly created directory:

```bash
$ poetry new generali-poetry
Created package generali_poetry in generali-poetry
$ cd generali-poetry
```

By running `poetry new generali-poetry`, you create a new folder named `generali-poetry/`. When you look inside the folder, you’ll see a structure:

```bash
generali-poetry
├── README.md
├── generali_poetry
│   └── __init__.py
├── pyproject.toml
└── tests
    └── __init__.py

3 directories, 4 files
```

To have more control over creating the package name, you can use the `--name` option to name it differently than the project folder:

```bash
$ poetry new generali-poetry --name generalipoetry
```

If you prefer to store your source code in an additional `src/` parent folder, then Poetry lets you stick to that convention by using the `--src` flag:

```bash
$ poetry new --src generali-poetry
$ cd generali-poetry
```

By adding the `--src` flag, you’ve created a folder named `src/`, which contains your `generali_poetry/` directory:

```bash
generali-poetry
├── README.md
├── pyproject.toml
├── src
│   └── generali_poetry
│       └── __init__.py
└── tests
    └── __init__.py
```

## Use the `pyproject.toml` File

The **`pyproject.toml`** file is what is the most important here. This will orchestrate your project and its dependencies. For now, it looks like this:

```bash
$ cat pyproject.toml 
[tool.poetry]
name = "generali-poetry"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "generali_poetry"}]

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

This file isn’t an invention of Poetry. It’s a **configuration file** standard that was defined in PEP 518:

> This PEP specifies how Python software packages should specify what build dependencies they have in order to execute their chosen build system. As part of this specification, a new configuration file is introduced for software packages to use to specify their build dependencies (with the expectation that the same configuration file will be used for future configuration details). ([Source](https://www.python.org/dev/peps/pep-0518/#abstract))
> 

The authors considered a few file formats for the “new configuration file” mentioned in the quote above. In the end, they decided on the **TOML** format, which stands for [Tom’s Obvious Minimal Language](https://toml.io/en/).

You can see three sections in the `pyproject.toml` file. These sections are called **tables**. They contain instructions that tools like Poetry recognize and use for **dependency management** or **build routines**.

If a table name is tool-specific, it must be prefixed with `tool`. By using such a **subtable**, you can add instructions for different tools in your project. In this case, there is only `tool.poetry`.

I recommend using [semantic versioning](https://semver.org) when deciding which version to assign to the project.

In the `[tool.poetry]` subtable, you can store general information about your Poetry project. Your available keys are [defined by Poetry](https://python-poetry.org/docs/pyproject/). While some keys are optional, there are four that you must specify:

1. **`name`**: the name of your package
2. **`version`**: the version of your package, ideally following [semantic versioning](https://semver.org/)
3. **`description`**: a short description of your package
4. **`authors`**: a list of authors, in the format `name <email>`

The subtables `[tool.poetry.dependencies]`  and `[tool.poetry.dev-dependencies]` are used for your dependency management. The important thing is to recognize that there *is* differentiation between package dependencies and development dependencies.

The last table of the `pyproject.toml` file is `[build-system]`. This table defines data that Poetry and other build tools can work with, but as it’s not tool-specific, it doesn’t have a prefix. Poetry created the `pyproject.toml` file with two keys in place:

1. **`requires`**: a list of dependencies that are required to build the package, making this key mandatory
2. **`build-backend`**: the Python object used to perform the build process

When you start a new project with Poetry, this is the `pyproject.toml` file you start with. Over time, you’ll add configuration details about your package and the tools you’re using. As your Python project grows, your `pyproject.toml` file will grow with it. This is particularly true for the subtables `[tool.poetry.dependencies]` and `[tool.poetry.dev-dependencies]`. 

Poetry assumes your package contains a package with the same name as **`tool.poetry.name`** located in the root of your project. If this is not the case, populate **`[tool.poetry.packages](https://python-poetry.org/docs/pyproject/#packages)`** to specify your packages and their locations.

Similarly, the traditional **`MANIFEST.in`** file is replaced by the **`tool.poetry.readme`**, **`tool.poetry.include`**, and**`tool.poetry.exclude`** sections. **`tool.poetry.exclude`** is additionally implicitly populated by your **`.gitignore`**. For full documentation on the project format, see the **[pyproject section](https://python-poetry.org/docs/pyproject/)** of the documentation.

Poetry will require you to explicitly specify what versions of Python you intend to support, and its universal locking will guarantee that your project is installable (and all dependencies claim support for) all supported Python versions.

## Initialising a pre-existing project

Instead of creating a new project, Poetry can be used to ‘initialise’ a pre-populated directory. To interactively create a **`pyproject.toml`** file in directory **`pre-existing-project`**:

```bash
$ cd pre-existing-project
$ poetry init
```

## Using your virtual environment

By default, Poetry creates a virtual environment in **`{cache-dir}/virtualenvs`**. You can change the **`[cache-dir](https://python-poetry.org/docs/configuration/#cache-dir)`** value by editing the Poetry configuration. Additionally, you can use the **`[virtualenvs.in-project](https://python-poetry.org/docs/configuration/#virtualenvsin-project)`** configuration variable to create virtual environments within your project directory.

**External virtual environment management**

Poetry will detect and respect an existing virtual environment that has been externally activated. This is a powerful mechanism that is intended to be an alternative to Poetry’s built-in, simplified environment management.

If you have created a virtual environment with `pyenv`, run the following [command](https://github.com/python-poetry/poetry/issues/651) to let `poetry` recognise it:

```bash
$ poetry config virtualenvs.prefer-active-python true
```

To take advantage of this, simply activate a virtual environment using your preferred method or tooling, before running any Poetry commands that expect to manipulate an environment.

For example, let’s create a `pyenv` virtual environment and then initialise `poetry`.

```bash
$ mkdir generali-poetry
$ cd generali-poetry
$ pyenv virtualenv 3.8 generali-poetry
Looking in links: /var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/tmp27qf22h4
Requirement already satisfied: setuptools in /Users/lizzy/.pyenv/versions/3.8.16/envs/generali-poetry/lib/python3.8/site-packages (56.0.0)
Requirement already satisfied: pip in /Users/lizzy/.pyenv/versions/3.8.16/envs/generali-poetry/lib/python3.8/site-packages (22.0.4)
$ pyenv local generali-poetry
$ python -V
Python 3.8.16
$ poetry init

This command will guide you through creating your pyproject.toml config.

Package name [generali-poetry]:  
Version [0.1.0]:  
Description []:  demo for poetry usage
Author [None, n to skip]:   
expected string or bytes-like object, got 'NoneType'
Author [None, n to skip]:  n
License []:  
Compatible Python versions [^3.8]:  

Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] no
Generated file

[tool.poetry]
name = "generali-poetry"
version = "0.1.0"
description = "demo for poetry usage"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "generali_poetry"}]

[tool.poetry.dependencies]
python = "^3.8"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

Do you confirm generation? (yes/no) [yes]
```

## Specifying dependencies

If you want to add dependencies to your project, you can specify them in the **`tool.poetry.dependencies`** section.

```bash
[tool.poetry.dependencies]
pendulum = "^2.1"
```

As you can see, it takes a mapping of **package names** and **version constraints**.

Poetry uses this information to search for the right set of files in package “repositories” that you register in the **`tool.poetry.source`** section, or on **[PyPI](https://pypi.org/)** by default.

Also, instead of modifying the **`pyproject.toml`** file by hand, you can use the **`add`** command.

```bash
$ poetry add pendulum

Using version ^2.1.2 for pendulum

Updating dependencies
Resolving dependencies... (0.3s)

No dependencies to install or update

Writing lock file
```


It will automatically find a suitable version constraint **and install** the package and sub-dependencies.

Poetry supports a rich **[dependency specification](https://python-poetry.org/docs/dependency-specification/)** syntax, including caret, tilde, wildcard, inequality and **[multiple constraints](https://python-poetry.org/docs/dependency-specification/#multiple-constraints-dependencies)** requirements.

Let’s add also the `requests` dependency.

```bash
$ poetry add requests
Using version ^2.31.0 for requests

Updating dependencies
Resolving dependencies... Downloading https://files.pythonhosted.org/packages/9d/19/59961b522e6757f0c9097e4493fa906031b95b3ebe9360b2c3083561a6b4/certifi-2023.5.7-py3-none-any.wResolving dependencies... (1.7s)

Package operations: 5 installs, 0 updates, 0 removals

  • Installing certifi (2023.5.7)
  • Installing charset-normalizer (3.1.0)
  • Installing idna (3.4)
  • Installing urllib3 (2.0.3)
  • Installing requests (2.31.0)

Writing lock file
```

## Using `poetry run`

To run your script simply use **`poetry run python your_script.py`**.

## Version constraints

In our example, we are requesting the **`pendulum`** package with the version constraint **`^2.1`**. This means any version greater or equal to 2.1.0 and less than 3.0.0 (**`>=2.1.0 <3.0.0`**).

Please read **[Dependency specification](https://python-poetry.org/docs/dependency-specification/)** for more in-depth information on versions, how versions relate to each other, and on the different ways you can specify dependencies.

**How does Poetry download the right files?**

When you specify a dependency in **`pyproject.toml`**, Poetry first takes the name of the package that you have requested and searches for it in any repository you have registered using the **`repositories`** key. If you have not registered any extra repositories, or it does not find a package with that name in the repositories you have specified, it falls back to PyPI.

When Poetry finds the right package, it then attempts to find the best match for the version constraint you have specified.

## Installing dependencies

To install the defined dependencies for your project, just run the **`[install](https://python-poetry.org/docs/cli/#install)`** command.

```bash
poetry install
```

When you run this command, one of two things may happen:

- **Installing without `poetry.lock`**
If you have never run the command before and there is also no **`poetry.lock`** file present, Poetry simply resolves all dependencies listed in your **`pyproject.toml`** file and downloads the latest version of their files.
When Poetry has finished installing, it writes all the packages and their exact versions that it downloaded to the **`poetry.lock`** file, locking the project to those specific versions. You should commit the **`poetry.lock`** file to your project repo so that all people working on the project are locked to the same versions of dependencies.
- **Installing with `poetry.lock`**
This brings us to the second scenario. If there is already a **`poetry.lock`** file as well as a **`pyproject.toml`** file when you run **`poetry install`**, it means either you ran the **`install`** command before, or someone else on the project ran the **`install`** command and committed the **`poetry.lock`** file to the project (which is good).
Either way, running **`install`** when a **`poetry.lock`** file is present resolves and installs all dependencies that you listed in **`pyproject.toml`**, but Poetry uses the exact versions listed in **`poetry.lock`** to ensure that the package versions are consistent for everyone working on your project. As a result you will have all dependencies requested by your **`pyproject.toml`** file, but they may not all be at the very latest available versions (some dependencies listed in the **`poetry.lock`** file may have released newer versions since the file was created). This is by design, it ensures that your project does not break because of unexpected changes in dependencies.

Besides dependencies, Poetry also installs the project itself

## Updating dependencies to their latest versions

As mentioned above, the **`poetry.lock`** file prevents you from automatically getting the latest versions of your dependencies. To update to the latest versions, use the **`update`** command. This will fetch the latest matching versions (according to your **`pyproject.toml`** file) and update the lock file with the new versions. (This is equivalent to deleting the **`poetry.lock`** file and running **`install`** again.)

Poetry will display a **Warning** when executing an install command if **`poetry.lock`** and **`pyproject.toml`** are not synchronized.

For updating your dependencies, Poetry provides different options depending on two scenarios:

1. Update a dependency inside your version constraints.
2. Update a dependency outside your version constraints.

You can find your version constraints in your `pyproject.toml` file. When a new version of a dependency still fulfills your version constraints, you can use the `update` command:

```bash
$ poetry update
```

The `update` command will update all your packages and their dependencies within their version constraints. Afterward, Poetry will update your `poetry.lock` file.

If you want to update one or more specific packages, then you can list them as arguments:

```bash
$ poetry update requests beautifulsoup4
```

With this command, Poetry will search for a new version of `requests` and a new version of `beautifulsoup4` that fulfill the version constraints listed in your `pyproject.toml` file. Then it’ll resolve all dependencies of your project and pin the versions into your `poetry.lock` file. Your `pyproject.toml` file will stay the same because the listed constraints remain valid.

If you want to update a dependency with a version that’s higher than the defined version in the `pyproject.toml` file, you need to adjust the `pyproject.toml` file beforehand. Another option is to run the `add` command with a version constraint or the `latest` tag:

```bash
$ poetry add pytest@latest --dev
```

When you run the `add` command with the `latest` tag, it looks for the latest version of the package and updates your `pyproject.toml` file. Including the `latest` tag or a version constraint is critical in using the `add` command. Without it, you’d get a message that the package is already present in your project. Also, don’t forget to add the `--dev` flag for development dependencies. Otherwise, you’d add the package to your regular dependencies.

After adding a new version, you must run the `install` command you learned about in the section above. Only then are your updates locked into the `poetry.lock` file.

If you’re not sure which version-based changes an update would introduce to your dependencies, you can use the `--dry-run` flag. This flag works for both the `update` and the `add` commands. It displays the operations in your terminal without executing any of them. This way, you can spot version changes safely and decide which update scenario works best for you.

## **Handle poetry.lock**

When you run the `poetry add` command, Poetry automatically updates `pyproject.toml`and pins the resolved versions in the `poetry.lock` file. However, you don’t have to let Poetry do all the work. You can manually add dependencies to the `pyproject.toml` file and lock them afterward.

### **Pin Dependencies in `poetry.lock`**

If you want to [build a web scraper with Python](https://realpython.com/beautiful-soup-web-scraper-python/), then you may want to use [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse your data. Add it to the `tool.poetry.dependencies` table in the `pyproject.toml` file:

```bash
# generali-poetry/pyproject.toml (Excerpt)

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.31.0"
beautifulsoup4 = "4.10.0"
```

By adding `beautifulsoup4 = "4.10.0"`, you’re telling Poetry that it should install exactly this version. When you add a requirement to the `pyproject.toml` file, it’s not installed yet. As long as there’s no `poetry.lock` file present in your project, you can run `poetry install`after manually adding dependencies, because Poetry looks for a `poetry.lock` file first. If it doesn’t find one, Poetry resolves the dependencies listed in the `pyproject.toml` file.

As soon as a `poetry.lock` file is present, Poetry will rely on this file to install dependencies. Running only `poetry install` would trigger a warning that both files are out of sync and would produce an error because Poetry wouldn’t know of any `beautifulsoup4` versions in the project yet.

To pin manually added dependencies from your `pyproject.toml` file to `poetry.lock`, you must first run the `poetry lock` command:

```bash
$ poetry lock
Updating dependencies
Resolving dependencies... 
Downloading https://files.pythonhosted.org/packages/49/37/673d6490efc51ec46d198c75903d99de59ba
ffdd47aea3d071b80a9e4e89/soupsieve-2.4.1-py3-none-any.whResolving dependencies... (1.5s)

Writing lock file
```

By running `poetry lock`, Poetry processes all dependencies in your `pyproject.toml` file and locks them into the `poetry.lock` file. And Poetry doesn’t stop there. When you run `poetry lock`, Poetry also recursively traverses and locks all dependencies of your direct dependencies.

**Note:** The `poetry lock` command also updates your existing dependencies if newer versions that fit your version constraints are available . If you don’t want to update any dependencies that are already in the `poetry.lock` file, then you have to add the `--no-update` option to the `poetry lock` command:

```bash
$ poetry lock --no-update
Resolving dependencies... (0.1s)
```

In this case, Poetry only resolves the new dependencies but leaves any existing dependency versions inside the `poetry.lock` file untouched.

To use the newly added dependencies, don’t forget to run `poetry install`.

## **Use an Existing `requirements.txt` File**

Sometimes you have projects that already have a `requirements.txt` file. Take a look at the `requirements.txt` file of this [Python web scraper](https://realpython.com/beautiful-soup-web-scraper-python/):

```bash
$ cat requirements.txt
beautifulsoup4==4.9.3
certifi==2020.12.5
chardet==4.0.0
idna==2.10
requests==2.25.1
soupsieve==2.2.1
urllib3==1.26.4
```

With the `[cat` utility](https://en.wikipedia.org/wiki/Cat_(Unix)), you can read a file and write the content to the **standard output**. In this case, it shows the dependencies of the web scraper project. Once you’ve created the Poetry project with `poetry init`, you can combine the `cat` utility with the `poetry add` command:

```bash
$ poetry add `cat requirements.txt`
Creating virtualenv rp-require-0ubvZ-py3.9 in ~/Library/Caches/pypoetry/virtualenvs

Updating dependencies
Resolving dependencies... Downloading https://files.pythonhosted.org/packages/19/c7/fa589626997dd07bd87d9269342ccb74b1720384a4d739a1872bd84fbe68/chardet-4.0.0-py2.py3-none-any.Resolving dependencies... Downloading https://files.pythonhosted.org/packages/5e/a0/5f06e1e1d463903cf0c0eebeb751791119ed7a4b3737fdc9a77f1cdfb51f/certifi-2020.12.5-py2.py3-none-Resolving dependencies... Downloading https://files.pythonhosted.org/packages/5e/a0/5f06e1e1d463903cf0c0eebeb751791119ed7a4b3737fdc9a77f1cdfb51f/certifi-2020.12.5-py2.py3-none-Resolving dependencies... (2.0s)

Package operations: 1 install, 6 updates, 1 removal

  • Removing charset-normalizer (3.1.0)
  • Updating certifi (2023.5.7 -> 2020.12.5)
  • Installing chardet (4.0.0)
  • Updating idna (3.4 -> 2.10)
  • Updating soupsieve (2.4.1 -> 2.2.1)
  • Updating urllib3 (2.0.3 -> 1.26.4)
  • Updating beautifulsoup4 (4.10.0 -> 4.9.3)
  • Updating requests (2.31.0 -> 2.25.1)

Writing lock file
```

When a requirements file is straightforward like this, using `poetry add` and `cat` can save you some manual work.

Sometimes `requirements.txt` files are a bit more complicated, however. In those cases, you can either execute a test run and see how it turns out or add requirements by hand to the `[tool.poetry.dependencies]` table in the `pyproject.toml` file. To see if the structure of your `pyproject.toml` is valid, you can run `poetry check` afterward.

### **Create `requirements.txt` From `poetry.lock`**

In some situations, you must have a `requirements.txt` file. For cases like this, Poetry provides the `[export`command](https://python-poetry.org/docs/cli/#export). If you have a Poetry project, you can create a `requirements.txt` file from your `poetry.lock` file:

```bash
$ poetry export --output requirements.txt
```

Using the `poetry export` command in this way creates a `requirements.txt` file that includes [hashes](https://pip.pypa.io/en/stable/cli/pip_install/#hash-checking-mode) and [environment markers](https://www.python.org/dev/peps/pep-0508/#environment-markers). This means that you can be sure to work with very strict requirements that resemble the content of your `poetry.lock` file. If you also want to include your development dependencies, you can add `--dev` to the command. To see all available options, you can check `poetry export --help`.

## **Command Reference**

This tutorial has introduced you to Poetry’s dependency management. Along the way, you’ve used some of Poetry’s command-line interface (CLI) commands:

| Poetry Command | Explanation |
| --- | --- |
| $ poetry --version | Show the version of your Poetry installation. |
| $ poetry new | Create a new Poetry project. |
| $ poetry init | Add Poetry to an existing project. |
| $ poetry run | Execute the given command with Poetry. |
| $ poetry add | Add a package to pyproject.toml and install it. |
| $ poetry update | Update your project’s dependencies. |
| $ poetry install | Install the dependencies. |
| $ poetry show | List installed packages. |
| $ poetry lock | Pin the latest version of your dependencies into poetry.lock. |
| $ poetry lock --no-update | Refresh the poetry.lock file without updating any dependency version. |
| $ poetry check | Validate pyproject.toml. |
| $ poetry config --list | Show the Poetry configuration. |
| $ poetry env list | List the poetry virtual environments of your project. |
| $ poetry export | Export poetry.lock to other formats. |

You can check out the [Poetry CLI documentation](https://python-poetry.org/docs/cli/) to learn more about the commands above and the other commands Poetry offers. You can also run `poetry --help` to see information right in your terminal!

# for Testing

Besides `pytest` and its requirements, Poetry also installs the project itself. This way, you can import `rp_poetry` into your tests right away:

`# tests/test_rp_poetry.py

from rp_poetry import __version__

def test_version():
    assert __version__ == "0.1.0"`

With your project’s package installed, you can import `rp_poetry` into your tests and check for the `__version__` string. With `pytest` installed, you can use the `poetry run` command to execute the tests:

`$ poetry run pytest
========================= test session starts ==========================
platform darwin -- Python 3.9.1, pytest-5.4.3, py-1.10.0, pluggy-0.13.1
rootdir: /Users/philipp/Real Python/rp-poetry
collected 1 item

tests/test_rp_poetry.py .                                        [100%]

========================== 1 passed in 0.01s ===========================`

Your current test is running successfully, so you can confidently continue coding. However, if you look closely at line 3, something looks a bit odd. It says `pytest-5.4.3`, not `5.2` like stated in the `pyproject.toml` file. Good catch!

To recap, the `pytest` dependency in your `pyproject.toml` file looks like this:

`# rp_poetry/pyproject.toml (Excerpt)

[tool.poetry.dev-dependencies]
pytest = "^5.2"`

The caret (`^`) in front of `5.2` has a specific meaning, and it’s one of the [versioning constraints](https://python-poetry.org/docs/dependency-specification/#version-constraints)that Poetry provides. It means that Poetry can install any version that matches the leftmost non-zero digit of the version string. This means that using `5.4.3` is allowed. Version `6.0`wouldn’t be allowed.

A symbol like the caret will become important when Poetry tries to resolve the dependency versions. If there are only two requirements, this isn’t too hard. The more dependencies you declare, the more complicated it gets. Let’s see how Poetry handles this by installing new packages into your project.

To explicitly tell Poetry that a package is a development dependency, you run `poetry add`with the `--dev` option. You can also use a shorthand `-D` option, which is the same as `--dev`:

`$ poetry add black -D`
