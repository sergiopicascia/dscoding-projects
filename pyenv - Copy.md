# Managing multiple Python versions with pyenv

<aside>
📗 Resources

https://github.com/pyenv/pyenv

[https://realpython.com/intro-to-pyenv/](https://realpython.com/intro-to-pyenv/)

</aside>

# Why?

- contributing to a project that supports multiple versions of python and being able to test it using different versions
- trying new python versions without messing up the development environment

**And why pyenv?**

- `pyenv` is a wonderful tool for managing multiple Python versions.
- Using `pyenv` is also a great way to [install pre-release versions of Python](https://realpython.com/python-pre-release/) so that you can test them for bugs

## ****Why Not Use System Python?****

“System Python” is the Python that comes installed on your operating system. If you’re on Mac or Linux, then by default, when you type `python` in your terminal, you get a nice [Python REPL](https://realpython.com/python-repl/).

### **How to know which python is installed on my pc?**

**(macOS / Unix version)**

1. open the terminal
2. Either do one of these two things:
    1. `ls -ls /usr/bin/python*` or/and `ls -ls /opt/homebrew/bin/python*` directly from the root
    2. go under the directory `/usr/bin` (here there are all the python installations), then type `python` and press `tab` to inspect all the matches in the directory

If `/usr/bin/` does not contain `python` installations, then check where they are with the command `whereis python`.

**(Windows)**

[https://stackoverflow.com/questions/53312590/how-can-i-check-all-the-installed-python-versions-on-windows](https://stackoverflow.com/questions/53312590/how-can-i-check-all-the-installed-python-versions-on-windows)

### **Motivations for avoiding using system python**

1. Each time a package is installed, you interfere with system installations; moreover, you could not be the administrator of your computer, thus no possibility of running `sudo`. To install a package into your system Python, you have to run `sudo pip install`. That’s because you’re installing the Python package globally, which is a real problem if another user comes along and wants to install a slightly older version of the package.
2. Difficulties at managing dependencies. One common way this problem presents itself is a popular and stable package suddenly misbehaving on your system. After hours of troubleshooting and Googling, you may find that you’ve installed the wrong version of a [dependency](https://realpython.com/courses/managing-python-dependencies/), and it’s ruining your day.
3. System python could be too old for your liking. And updating it could mess up dependencies with system commands and functioning.

## Package Manager

The next logical place to look is package managers. Programs such as `apt`, `yum`, `brew`, or `port` are typical next options. After all, this is how you install most [packages](https://realpython.com/python-modules-packages/) to your system. Unfortunately, you’ll find some of the same problems using a package manager.

By default, package managers tend to install their packages into the global system space instead of the user space.

## What do we want?

1. Install Python in your user space
2. Install multiple versions of Python
3. Specify the exact Python version you want
4. Switch between the installed versions

## `pyenv` is the solution to our problem

`[pyenv](https://github.com/pyenv/pyenv)` lets you do all of these things and more. 

<aside>
⚠️ **Note:** `pyenv` did not originally support Windows. However, there appears to be some basic support with the [pyenv-win](https://github.com/pyenv-win/pyenv-win) project that recently became active. If you use Windows, feel free to check it out.

</aside>

# Installing `pyenv`

1. First, install some OS dependencies. Depending on the operating system you are using, you need to install what is missing by default. Check the [docs](https://devguide.python.org/getting-started/setup-building/index.html#build-dependencies) to follow  instructions for installing dependencies. Here we will see specific dependencies for `pyenv`.  *For Windows users: it is likely you will have all the dependencies installed by default.*

**Ubuntu/Debian**

```bash
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```

**Fedora/CentOS/RHEL**

```bash
$ sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite \
sqlite-devel openssl-devel xz xz-devel libffi-devel
```

**macOS**

```bash
$ brew install openssl readline sqlite3 xz zlib
```

If running Mojave, run also

```bash
$ sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target
```

1. Install `pyenv`. After you’ve installed the build dependencies, you’re ready to install `pyenv` itself. I recommend using the [pyenv-installer project](https://github.com/pyenv/pyenv-installer):

```bash
$ curl https://pyenv.run | bash
```

This will install `pyenv` along with a few plugins that are useful:

1. **`pyenv`**: The actual `pyenv` application
2. **`pyenv-virtualenv`**: Plugin for `pyenv` and virtual environments
3. **`pyenv-update`**: Plugin for updating `pyenv`
4. **`pyenv-doctor`**: Plugin to verify that `pyenv` and build dependencies are installed
5. **`pyenv-which-ext`**: Plugin to automatically lookup system commands

At the end of the run, you should see something like this:

```bash
WARNING: seems you still have not added 'pyenv' to the load path.

Load pyenv automatically by adding
the following to ~/.bashrc:

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

The output will be based on your shell. But you should follow the instructions to add `pyenv`to your path and to initialize `pyenv`/`pyenv-virtualenv` auto completion. Once you’ve done this, you need to reload your shell:

```bash
$ exec "$SHELL" # Or just restart your terminal
```

That’s it. You now have `pyenv` and four useful plugins installed.

# First `pyenv` use case: installing Python

You have many versions of Python to choose from. If you wanted to see all the available [CPython](https://realpython.com/cpython-source-code-guide/) 3.6 through 3.8, you can do this:

```bash
$ pyenv install --list | grep " 3\.[6789]"
3.7.0
3.7-dev
3.7.1
3.7.2
[...]
3.7.16
3.8.0
3.8-dev
3.8.1
[...]  
3.8.15
3.8.16
3.9.0
3.9-dev
3.9.1
[...]
3.9.15
3.9.16
```

Once you find the version you want, you can install it with a single command:

```bash
$ pyenv install -v 3.9
python-build: use openssl@1.1 from homebrew
python-build: use readline from homebrew
/var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/python-build.20230614093257.38423 ~
Downloading Python-3.9.16.tar.xz...
-> https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tar.xz
/var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/python-build.20230614093257.38423/
 Python-3.9.16 /var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/python-build.20230614093257.38423 ~
Installing Python-3.9.16...
[...]
Successfully installed pip-22.0.4 setuptools-58.1.0
/var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/python-build.20230614093257.38423 ~
~
Installed Python-3.9.16 to /Users/lizzy/.pyenv/versions/3.9.16
```

On macOS, it is necessary that the python version is compatible by the current operating system.

You can test if your current python installation works properly by running tests with the following code:

```bash
$ python -m test
== CPython 3.7.9 (default, Jan 8 2023, 15:31:19) [Clang 14.0.0 (clang-1400.0.29.202)]
== Darwin-22.5.0-arm64-arm-64bit little-endian
== cwd: /private/var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/test_python_86729
== CPU count: 8
== encodings: locale=UTF-8, FS=utf-8
0:00:00 load avg: 1.88 Run tests sequentially
[...]
```

## Where does `pyenv` install Python versions?

As mentioned before, `pyenv` works by building Python from source. Each version that you have installed is located nicely in your `pyenv` root directory:

```bash
$ ls ~/.pyenv/versions/
3.7.9	3.9.16
```

All of your versions will be located here. This is handy because removing these versions is trivial:

```bash
$ rm -rf ~/.pyenv/versions/3.9.16
```

Of course `pyenv` also provides a command to uninstall a particular Python version:

```bash
$ pyenv uninstall 3.9.16
```

Lastly, you can check what versions of Python you have available:

```bash
$ pyenv versions
* system (set by /Users/lizzy/.pyenv/version)
  3.7.9
  3.9.16
```

The `*` indicates that the `system` Python version is active currently. You’ll also notice that this is set by a file in your root `pyenv` directory. This means that, by default, you are still using your system Python:

```bash
$ python3 -V
Python 3.11.4
```

If you try to confirm this using `which`, you’ll see this:

```bash
$ which python3
/Users/lizzy/.pyenv/shims/python3
```

This might be surprising, but this is how `pyenv` works. `pyenv` inserts itself into your `[PATH](https://realpython.com/add-python-to-path/)` and from your OS’s perspective *is* the executable that is getting called. If you want to see the actual path, you can run the following:

```bash
$ pyenv which python3
/opt/homebrew/bin/python3
```

# Switching Python global version

With the `global` command, you can change the default Python installation/version to use.

If, for example, you wanted to use version 3.7.9, which is one of the versions installed in `pyenv`, then you can use the `global` command:

```bash
$ pyenv global 3.7.9
$ python -V
Python 3.7.9

$ pyenv versions
	system
* 3.7.9 (set by /Users/lizzy/.pyenv/version)
  3.9.16
```

If you ever want to go back to the system version of Python as the default, you can run this:

```bash
$ pyenv global system
$ python3 -V
Python 3.11.4
```

It could happen that you have to use `python3` instead of `python` when trying to call your python system version: this is because the name for the python command which is set in the `PATH` environment variables can be different for different versions of python. However, `pyenv` versions shall always be called with the simple `python` command.

You can now switch between different versions of Python with ease. This is just the beginning. If you have many versions that you want to switch between, typing these commands consistently is tedious. This section goes over the basics, but a better workflow is described in working with multiple environments (we’ll se later).

# `pyenv` commands

`pyenv` offers many commands. You can see a complete list of all available commands with this:

```bash
$ pyenv commands
activate
commands
completions
deactivate
...
virtualenvs
whence
which
```

This outputs all command names. Each command has a `--help` flag that will give you more detailed information. For example, if you wanted to see more information on the `shims`command you could run the following:

```bash
$ pyenv shims --help
Usage: pyenv shims [--short]

List existing pyenv shims
```

The help message describes what the command is used for and any options you can use in conjunction with the command.

| Command | Example | Description | Flags | Flags description |
| --- | --- | --- | --- | --- |
| install | $ pyenv install 3.9 | This command can be used to install a specific version of Python. | -l/--list | Lists all available Python versions for installation |
|  |  |  | g/--debug | Builds a debug version of Python |
|  |  |  | v/--verbose | Verbose mode: print compilation status to stdout |
| versions | $ pyenv versions | Displays all currently installed Python versions |  |  |
| version | $ pyenv version | Displays the selected installed Python version |  |  |
| which | $ pyenv which pip | This command allows you to see the full path to the executable (for example, pip) pyenv is running |  |  |
| global | $ pyenv global 3.7.9 | Sets the global Python version. |  |  |
| local | $ pyenv local 3.9.16 | Sets an application-specific Python version. This command creates a .python-version file in your current directory. If you have pyenvactive in your environment, this file will automatically activate this version for you. |  |  |
| shell | $ pyenv shell 3.8.16 | Sets a shell-specific Python version. This command activates the version specified by setting the PYENV_VERSION environment variable. This command overwrites any applications or global settings you may have. If you want to deactivate the version, you can use the --unset flag. |  |  |

# How It Works

At a high level, pyenv intercepts Python commands using shim executables injected into your `PATH`, determines which Python version has been specified by your application, and passes your commands along to the correct Python installation.

## Understanding PATH

When you run a command like `python` or `pip`, your operating system searches through a list of directories to find an executable file with that name. This list of directories lives in an environment variable called `PATH`, with each directory in the list separated by a colon:

`/usr/local/bin:/usr/bin:/bin`

Directories in `PATH` are searched from left to right, so a matching executable in a directory at the beginning of the list takes precedence over another one at the end. In this example, the `/usr/local/bin` directory will be searched first, then `/usr/bin`, then `/bin`.

## Understanding Shims

pyenv works by inserting a directory of *shims* at the front of your `PATH`:

`$(pyenv root)/shims:/usr/local/bin:/usr/bin:/bin`

Through a process called *rehashing*, pyenv maintains shims in that directory to match every Python command across every installed version of Python—`python`, `pip`, and so on.

Shims are lightweight executables that simply pass your command along to pyenv. So with pyenv installed, when you run, say, `pip`, your operating system will do the following:

- Search your `PATH` for an executable file named `pip`
- Find the pyenv shim named `pip` at the beginning of your `PATH`
- Run the shim named `pip`, which in turn passes the command along to pyenv

## Understanding Python version selection

When you execute a shim, pyenv determines which Python version to use by reading it from the following sources, in this order:

1. The `PYENV_VERSION` environment variable (if specified). You can use the `[pyenv shell](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-shell)` command to set this environment variable in your current shell session.
2. The application-specific `.python-version` file in the current directory (if present). You can modify the current directory's `.python-version`file with the `[pyenv local](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local)` command.
3. The first `.python-version` file found (if any) by searching each parent directory, until reaching the root of your filesystem.
4. The global `$(pyenv root)/version` file. You can modify this file using the `[pyenv global](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-global)` command. If the global version file is not present, pyenv assumes you want to use the "system" Python (see below).

A special version name "`system`" means to use whatever Python is found on `PATH` after the shims `PATH` entry (in other words, whatever would be run if Pyenv shims weren't on `PATH`). Note that Pyenv considers those installations outside its control and does not attempt to inspect or distinguish them in any way. So e.g. if you are on MacOS and have OS-bundled Python 3.8.9 and Homebrew-installed Python 3.9.12 and 3.10.2 -- for Pyenv, this is still a single "`system`" version, and whichever of those is first on `PATH` under the executable name you specified will be run.

`[pyenv which <command>](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-which)` displays which real executable would be run when you invoke `<command>` via a shim. E.g. if you have 3.3.6, 3.2.1 and 2.5.2 installed of which 3.3.6 and 2.5.2 are selected and your system Python is 3.2.5, `pyenv which python2.5` should display `$(pyenv root)/versions/2.5.2/bin/python2.5`, `pyenv which python3` -- `$(pyenv root)/versions/3.3.6/bin/python3` and `pyenv which python3.2` -- path to your system Python due to the fall-through (see below).

Shims also fall through to anything further on `PATH` if the corresponding executable is not present in any of the selected Python installations. This allows you to use any programs installed elsewhere on the system as long as they are not shadowed by a selected Python installation.

## Locating Pyenv-provided Python installations

Once pyenv has determined which version of Python your application has specified, it passes the command along to the corresponding Python installation.

Each Python version is installed into its own directory under `$(pyenv root)/versions`.

For example, you might have these versions installed:

- `$(pyenv root)/versions/2.7.8/`
- `$(pyenv root)/versions/3.4.2/`
- `$(pyenv root)/versions/pypy-2.4.0/`

As far as Pyenv is concerned, version names are simply directories under`$(pyenv root)/versions`.

# Specifying the Python version

You saw there are different levels of python version specification:

- shell
- local
- global
- system

The first of these options that `pyenv` can find is the option it will use.

Here is an example showing how to work with this tree.

Let’s suppose we wanted to work with python 3.7.9: first, let’s change the version and then let’s check if the operation succeded.

```bash
$ pyenv global 3.7.9
$ pyenv versions
  system
* 3.7.9 (set by /Users/lizzy/.pyenv/version)
  3.8.16
  3.9.16
```

`pyenv` will use 3.7.9 as python version. It even indicates the location of the file it found. That file does indeed exist, and you can list its contents:

```bash
$ cat ~/.pyenv/version
3.7.9
```

Now, let’s create another file, named `.python-version` , with `local`:

```bash
$ pyenv local 3.9.16
```

Let’s check the version situation:

```bash
$ pyenv versions
  system
  3.7.9
  3.8.16
* 3.9.16 (set by /Users/lizzy/teaching/generali/.python-version)
```

You can see now that pyenv gives the priority to the local version. What happened here is that a file `.python-version` was created in the directory in which we are at the moment we launch `pyenv local` 

```bash
$ ls -a
.  ..  .python-version
$ cat .python-version
3.9.16
```

Here again, `pyenv` indicates how it would resolve our `python` command. This time it comes from `~/.python-version`. Note that the searching for `.python-version` is recursive:

```bash
$ mkdir subdirectory
$ cd subdirectory
$ ls -a # Notice no .python-version file
. ..
$ pyenv versions
	system
  3.7.9
  3.8.16
* 3.9.16 (set by /Users/lizzy/teaching/generali/.python-version)
```

Even though there isn’t a `.python-version` in `subdirectory`, the version is still set to `3.9.16` because `.python-version` exists in a parent directory. 

To deactivate a local python version, just delete the `.python-version` file or run the command `pyenv local --unset` .

Finally, you can set the Python version with `shell`:

```bash
$ pyenv shell 3.7.9
$ pyenv versions
	system
* 3.7.9 (set by PYENV_VERSION environment variable)
  3.8.16
  3.9.16
```

All this did is set the `$PYENV_VERSION` environment variable:

```bash
$ echo $PYENV_VERSION
3.7.9
```

To deactivate a shell python version, run the command `pyenv shell --unset` .

# Virtual environments with `pyenv`

Virtual environments and `pyenv` are a match made in heaven. `pyenv` has a wonderful plugin called `[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)` that makes working with multiple Python version *and* multiple virtual environments a breeze. If you’re wondering what the difference is between `pyenv`, `pyenv-virtualenv`, and tools like `virtualenv` or `venv`, then don’t worry. You’re not alone.

Here’s what you need to know:

- **pyenv** manages multiple versions of Python itself.
- **virtualenv/venv** manages virtual environments for a specific Python version.
- **pyenv-virtualenv** manages virtual environments for across varying versions of Python.

If you’re a die-hard `virtualenv` or `venv` user, don’t worry: `pyenv` plays nicely with either. In fact, you can keep the same workflow you’ve had if you’d prefer, though I think `pyenv-virtualenv` makes for a nicer experience when you’re switching between multiple environments that require different Python versions.

The good news is that since you used the `pyenv-installer` script to install `pyenv`, you already have `pyenv-virtualenv` installed and ready to go.

Test you installation using 

```bash
$ eval "$(pyenv virtualenv-init -)"
```

## Creating a virtual environment

Creating a virtual environment is a single command:

```bash
$ pyenv virtualenv <python_version> <environment_name>
```

Technically, the `<python_version>` is optional, but you should consider always specifying it so that you’re certain of what Python version you’re using.

The `<environment_name>` is just a name for you to help keep your environments separate. A good practice is to name your environments the same name as your project. For example, if you were working on `myproject` and wanted to develop against Python 3.7.9, you would run this:

```bash
$ pyenv virtualenv 3.7.9 project-venv
```

The output includes messages that show a couple of extra [Python packages](https://realpython.com/python-modules-packages/) getting installed, namely `[wheel](https://realpython.com/python-wheels/)`, `[pip](https://realpython.com/what-is-pip/)`, and `setuptools`. This is strictly for convenience and just sets up a more full featured environment for each of your virtual environments.

## **Activating Your Virtual Environment**

To activate a virtual environment, we will set the local version of python to the virtual environment version.

```bash
$ pyenv versions                     
  system
  3.7.9
  3.7.9/envs/project-venv
  3.8.16
  3.9.16
* project-venv --> /Users/lizzy/.pyenv/versions/3.7.9/envs/project-venv (set by /Users/lizzy/teaching/generali/project/.python-version)
$ pyenv local project-venv
$ ls -a
.		..		.python-version
$ cat .python-version 
project-venv
```

When you enter a directory having a local `pyenv` virtual environment, it will be automatically activated. If you exit the directory, the virtual environment will be automatically deactivated. This is exactly the behaviour we expect from local python versions. Indeed, a new file `.python-version` is created with the string `project-venv` in it referring to the `project-venv` `pyenv` version.

You can manually activate/deactivate your Python versions with this:

```bash
$ pyenv activate <environment_name>
$ pyenv deactivate
```

The above is what `pyenv-virtualenv` is doing when it enters or exits a directory with a `.python-version` file in it.

## Removing your virtual environment

With `pyenv` is really easy to create and destroy virtual environments. The command `uninstall` can be used also to remove virtual environments. Remember: virtual environments are stored in `pyenv` as if they were individual python versions.

```bash
$ pyenv versions
  system
  3.7.9
  3.7.9/envs/project
  3.8.16
* 3.9.16 (set by /Users/lizzy/teaching/generali/.python-version)
  project --> /Users/lizzy/.pyenv/versions/3.7.9/envs/project
$ pyenv uninstall project
pyenv: remove /Users/lizzy/.pyenv/versions/project? [y|N] y
pyenv-virtualenv: remove /Users/lizzy/.pyenv/versions/3.7.9/envs/project? (y/N) y
$ pyenv versions
  system
  3.7.9
  3.8.16
* 3.9.16 (set by /Users/lizzy/teaching/generali/.python-version)
```

## **Working With Multiple Environments**

Putting everything you’ve learned together, you can work effectively with multiple environments. Let’s assume you have the following versions installed, and you have activated the global version 3.7.9:

```bash
$ pyenv versions 
  system
* 3.7.9 (set by /Users/lizzy/.pyenv/version)
  3.7.9/envs/project-venv
  3.8.16
  3.9.16
  project-venv --> /Users/lizzy/.pyenv/versions/3.7.9/envs/project-venv
```

Now you want to work on two different, aptly named, projects:

1. **project** supports Python 3.7.9 and 3.8.16.
2. **project2** supports Python 3.8.16 and experiments with 3.9.16.

You can see that, by default, you are using the system Python, which is indicated by the `*` in the `pyenv versions` output. We have created a virtual environment for the first project before.

Now, create a second project having a virtual environment equipped with python 3.8.

```bash
$ pyenv virtualenv 3.8 project2-venv
Looking in links: /var/folders/1l/m4r3dj_n0lzbdq7sjh0mbr8c0000gp/T/tmpgcomur07
Requirement already satisfied: setuptools in /Users/lizzy/.pyenv/versions/3.8.16/envs/project2/lib/python3.8/site-packages (56.0.0)
Requirement already satisfied: pip in /Users/lizzy/.pyenv/versions/3.8.16/envs/project2/lib/python3.8/site-packages (22.0.4)
$ pyenv local project2-venv
$ ls -a
.               ..              .python-version
$ pyenv which python
/Users/lizzy/.pyenv/versions/project2-venv/bin/python
```

Let’s try switching project and the respective environments. Suppose we are outside every project we have just created:

```bash
$ ls
project
project2
$ python -V
Python 3.7.9
```

Now, as you `cd` between the projects, your environments will automatically activate:

```bash
$ cd project
$ project python -V
Python 3.7.9
$ cd ../project2
$ project2 python -V
Python 3.8.16
```

No more remembering to activate environments: you can switch between all your projects, and `pyenv` will take care of automatically activating the correct Python versions *and* the correct virtual environments.

## **Activating Multiple Versions Simultaneously**

As described in the example above, `project2` uses features in 3.8. Suppose you wanted to ensure that your code still works on Python 3.7. If you try running `python3.7`, you’ll get this:

```bash
$ cd project2
$ python3.7 -V
pyenv: python3.7: command not found

The `python3.7' command exists in these Python versions:
  3.7.9
  3.7.9/envs/project-venv
  project-venv
```

`pyenv` informs you that, while Python 3.7 is not available in the current active environment, it is available in other environments. `pyenv` gives you a way to activate multiple environments at once using a familiar command:

```bash
pyenv local project2-venv 3.7
```

This indicates to `pyenv` that you would like to use the virtual environment `project2` as the first option. So if a command, for example `python`, can be resolved in both environments, it will pick `project2-venv` before `3.7`. Let’s see what happens if you run this:

```bash
$ python3.7 -V            
Python 3.7.9
```

Here, `pyenv` attempts to find the `python3.7` command, and because it finds it in an environment that is active, it allows the command to execute.

Suppose that in the above example, you’ve found a compatibility problem with your library and would like to do some local testing. The testing requires that you install all the dependencies. You should follow the steps to create a new environment:

```bash
$ pyenv virtualenv 3.7 project2-tmp
$ pyenv local project2-tmp
```

Once you’re satisfied with your local testing, you can easily switch back to your default environment:

```bash
$ pyenv local project2 3.7
```