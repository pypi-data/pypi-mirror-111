'''
    xcross
    ======

    A utility for 1-line builds from the parent host.
'''

import argparse
import collections
import os
import pathlib
import re
import stat
import subprocess
import sys
import uuid

version_info = collections.namedtuple('version_info', 'major minor patch build')

__version_major__ = '0'
__version_minor__ = '1'
__version_patch__ = '5'
__version_build__ = '2021-06-26'
__version_info__ = version_info(major='0', minor='1', patch='5', build='2021-06-26')
__version__ = '0.1.5'

# Create our arguments.
parser = argparse.ArgumentParser(description='Cross-compile C/C++ with a single command.')
# Note: this can take 1 of 3 forms:
#   1). No argument provided, have an empty command.
#   2). Provide a command as a quoted string. This is written to file exactly,
#       so it can then be called locally.
#   3). Provide arguments standard on the command-line, as a list of args.
#       If any special characters are present, it errors out.
parser.add_argument(
    '--target',
    help='''The target triple for the cross-compiled architecture.
This may also be supplied via the environment variable `CROSS_TARGET`.
Ex: `--target=alpha-unknown-linux-gnu`.''',
)
parser.add_argument(
    '--dir',
    help='''The directory to share to the docker image.
This may also be supplied via the environment variable `CROSS_DIR`.
This directory may be an absolute path or relative to
the current working directory. Both the input and output arguments
must be relative to this. Defaults to `/`.
Ex: `--dir=..`''',
)
parser.add_argument(
    '-E',
    '--env',
    action='append',
    help='''Pass through an environment variable to the image.
May be provided multiple times, or as a comma-separated list of values.
If an argument is provided without a value, it's passed through using
the value in the current shell.
Ex: `-E=CXX=/usr/bin/c++,CC=/usr/bin/cc,AR`''',
)
parser.add_argument(
    '--cpu',
    help='''Set the CPU model for the compiler/Qemu emulator.
This may also be supplied via the environment variable `CROSS_CPU`.
A single CPU type may be provided. To enumerate valid CPU types
for the cross compiler, you may run `cc -mcpu=x`, where `x` is an
invalid CPU type. To enumerate valid CPU types for the Qemu emulator,
you may run `run -cpu help`.
Ex: `--cpu=e500mc`''',
)
parser.add_argument(
    '--server',
    help='''Server to fetch container images from.
This may also be supplied via the environment variable `CROSS_SERVER`.
Ex: `--server=docker.io`''',
)
parser.add_argument(
    '--username',
    help='''The username for the container image.
This may also be supplied via the environment variable `CROSS_USERNAME`.
Ex: `--username=ahuszagh`''',
)
parser.add_argument(
    '--repository',
    help='''The repository for the container image.
This may also be supplied via the environment variable `CROSS_REPOSITORY`.
Ex: `--repository=cross`''',
)
parser.add_argument(
    '--image-version',
    help='''The version of the target image.
This may also be supplied via the environment variable `CROSS_VERSION`.
Ex: `--image-version=0.1`''',
)
parser.add_argument(
    '--engine',
    help='''The path or name of the container engine executable.
This may also be supplied via the environment variable `CROSS_ENGINE`.
If not provided or empty, this searches for `docker` then `podman`.
Ex: `--engine=docker`''',
)
parser.add_argument(
    '--non-interactive',
    help='''Disable interactive shells.
This may also be supplied via the environment variable `CROSS_NONINTERACTIVE`.''',
    action='store_true'
)
parser.add_argument(
    '--update-image',
    help='''Update the container on run.
This may also be supplied via the environment variable `CROSS_UPDATE_IMAGE`.''',
    action='store_true'
)
parser.add_argument(
    '--remove-image',
    help='''Remove the image after executing the command.
This may also be supplied via the environment variable `CROSS_REMOVE_IMAGE`.''',
    action='store_true'
)
parser.add_argument(
    '--quiet',
    help='''Silence any warnings when running the image.
This may also be supplied via the environment variable `CROSS_QUIET`.''',
    action='store_true'
)
parser.add_argument(
    '-v', '--verbose',
    help='''Print verbose output.
This may also be supplied via the environment variable `CROSS_VERBOSE`.''',
    action='store_true'
)
parser.add_argument(
    '-V', '--version',
    action='version',
    version=f'%(prog)s {__version__}',
)
base_script_name = '.__ahuszagh_xcross_uuid_'

def error(message, code=126, show_help=True):
    '''Print message, help, and exit on error.'''

    sys.stderr.write(f'error: {message}.\n')
    if show_help:
        parser.print_help()
    sys.exit(code)

def print_verbose(message, verbose):
    '''Print a message if verbose logging is on.'''

    if verbose:
        print(message)

def get_current_dir():
    return pathlib.PurePath(os.getcwd())

def get_parent_dir(args):
    directory = args.dir or get_current_dir().root
    return pathlib.PurePath(os.path.realpath(directory))

def validate_username(username):
    return re.match('^[A-Za-z0-9_-]*$', username)

def validate_repository(repository):
    return re.match('^[A-Za-z0-9_-]+$', repository)

def validate_target(target):
    return re.match('^[A-Za-z0-9._-]+$', target)

def get_image(args):
    '''Format the image parameters to a string.'''

    target = args.target
    if args.image_version:
        target = f'{target}-{args.image_version}'
    image = f'{args.repository}:{target}'
    if args.username:
        image = f'{args.username}/{image}'
    if args.server:
        image = f'{args.server}/{image}'
    return image

def escape_single_quote(string):
    '''Escape a single quote in a string to be quoted.'''

    # We want to quote here, but we want to make sure we don't have
    # any injections, so we escpae single quotes inside, the only
    # character which is read in a single-quoted string.

    # Since escaping quotes inside single-quotes doesn't work...
    # we use that string concatenation works for adjacent values.
    # 'aaa''bbb' is the same as 'aaabbb', so 'aaa'\''bbb' works as
    # "aaa\'bbb"
    escaped = string.replace("'", "'\\''")
    return f"'{escaped}'"

def normpath(args):
    '''Normalize our arguments for paths on Windows.'''

    if os.name != 'nt':
        return

    # We want to be very... lenient here.
    # Backslash characters are **generally** not valid
    # in most cases, except for paths on Windows.
    #
    # Only change the value if:
    #   1. The path exists
    #   2. The path contains backslashes (IE, isn't a simple command).
    #   3. The path is relative to the parent dir shared to Docker.
    parent_dir = get_parent_dir(args)
    current_dir = get_current_dir()
    for index in range(len(args.command)):
        value = args.command[index]
        if '\\' in value and os.path.exists(value):
            path = pathlib.PureWindowsPath(os.path.realpath(value))
            if path.is_relative_to(parent_dir):
                relative = os.path.relpath(path, start=current_dir)
                posix = pathlib.PurePath(relative).as_posix()
                # Quote the path, to avoid valid paths with variable
                # substitution from occurring. `${a}bc` is a valid path
                # on Windows, believe it or not.
                args.command[index] = escape_single_quote(posix)

def format_command(args):
    '''Format a list of commands normalized to be executed in the shell.'''

    if not args.command:
        # Use the default entrypoint, `/bin/bash` if we have no args.
        return '/bin/bash'
    elif len(args.command) == 1:
        # This could still be a path, but we allow any escape characters here.
        normpath(args)
        return args.command[0]

    # Now need to validate our arguments: are any control characters
    # incorrectly present? We're pretty expansive here, since we can't
    # tell the difference between `( 'hello)'` and `( hello)` with
    # `["(", hello)"]`. So, just error if we have any potentially grammatical
    # character.
    if any(re.search('[;\'\"\n\\$!(){}`]', i) for i in args.command):
        error('Invalid control characters present: use a quoted string instead', show_help=False)

    # Normalize the paths inside, in case we have Windows-style paths.
    normpath(args)

    # Have more than 1 value. We might have spaces inside.
    # We need to escape these spaces, if present.
    # We know there's no special characters, or quotes,
    # so this is very simple to do:
    quoted = []
    for parameter in args.command:
        if ' ' in parameter:
            quoted.append(f'"{parameter}"')
        else:
            quoted.append(parameter)
    return ' '.join(quoted)

def image_command(args, relpath):
    '''Create the image command from the argument list.'''

    # Need to change to the proper directory, then export
    # any useful environment variables, etc. We first
    # inject the binary dir to the path, then add
    # any CPU model, if we're using it, and then
    # go to the CWD and work from there.
    command = ['export PATH="/opt/bin/":"$PATH"']
    if args.cpu:
        command.append(f'export CPU={escape_single_quote(args.cpu)}')
    command.append(f'cd /src/{escape_single_quote(relpath)}')
    command.append(format_command(args))
    return '\n'.join(command)

def find_container_engine(args):
    '''Find the container engine binary (docker or podman) if one isn't provided.'''

    print_verbose('Finding container engine...', args.verbose)
    for engine in ['docker', 'podman']:
        print_verbose(f'Trying to find engine {engine}...', args.verbose)
        try:
            code = subprocess.call([engine, '-v'], **args.subprocess_devnull)
            if code == 0:
                print_verbose(f'Found engine {engine}.', args.verbose)
                return engine
        except OSError as error:
            if error.errno != os.errno.ENOENT:
                raise

    error('Could not find docker or podman')

def engine_type(args):
    '''Determine the container engine type.'''

    print_verbose('Finding container engine type...', args.verbose)
    try:
        devnull = subprocess.DEVNULL
        pipe = subprocess.PIPE
        proc = subprocess.Popen([args.engine, '-v'], stdin=devnull, stdout=pipe, stderr=pipe)
        stdout, stderr = proc.communicate()
        if stdout:
            print_verbose(stdout.decode("utf-8"), args.verbose)
        if stderr:
            error(f'Got error when probing engine type of "{stderr.decode("utf-8")}"', show_help=False)
        if b'docker' in stdout.lower():
            print_verbose('Found docker container engine type.', args.verbose)
            return 'docker'
        elif b'podman' in stdout.lower():
            print_verbose('Found podman container engine type.', args.verbose)
            return 'podman'
        error(f'Unrecognized engine type, got "{stderr.decode("utf-8")}"', show_help=False)
    except OSError as err:
        if err.errno == errno.ENOENT:
            error(f'Unable to find command {args.engine}', code=err.errno, show_help=False)
        raise

def validate_arguments(args):
    '''Validate the parsed arguments.'''

    # Normalize our arguments.
    args.target = args.target or os.environ.get('CROSS_TARGET')
    args.dir = args.dir or get_current_dir().root
    args.cpu = args.cpu or os.environ.get('CROSS_DIR')
    args.cpu = args.cpu or os.environ.get('CROSS_CPU')
    if args.server is None:
        args.server = os.environ.get('CROSS_SERVER')
    if args.server is None:
        args.server = 'docker.io'
    if args.username is None:
        args.username = os.environ.get('CROSS_USERNAME')
    if args.username is None:
        args.username = 'ahuszagh'
    args.repository = args.repository or os.environ.get('CROSS_REPOSITORY')
    args.repository = args.repository or 'cross'
    args.non_interactive = args.non_interactive or bool(os.environ.get('CROSS_NONINTERACTIVE', False))
    args.update_image = args.update_image or bool(os.environ.get('CROSS_UPDATE_IMAGE', False))
    args.quiet = args.quiet or bool(os.environ.get('CROSS_QUIET', False))
    args.remove_image = args.remove_image or bool(os.environ.get('CROSS_REMOVE_IMAGE', False))
    args.subprocess_devnull = {}
    if not args.verbose:
        args.subprocess_devnull['stdin'] = subprocess.DEVNULL
        args.subprocess_devnull['stdout'] = subprocess.DEVNULL
        args.subprocess_devnull['stderr'] = subprocess.DEVNULL

    # Find dependent arguments.
    args.engine = args.engine or os.environ.get('CROSS_ENGINE')
    args.engine = args.engine or find_container_engine(args)
    args.engine_type = engine_type(args)

    # Validate our arguments.
    if args.quiet and args.verbose:
        error('Cannot have both verbose and quiet output.')
    if args.target is None or not validate_target(args.target):
        error('Must provide a valid target')
    if args.username is None or not validate_username(args.username):
        error('Must provide a valid Docker Hub username')
    if args.repository is None or not validate_repository(args.repository):
        error('Must provide a valid Docker Hub repository')

def docker_command(args, parent_dir, relpath):
    '''Create the docker command to invoke.'''

    # Process our environment variables.
    # We don't need to escape these, since we aren't
    # using a shell. For example, `VAR1="Some Thing"`
    # and `VAR1=Some Thing` will both be passed correctly.
    args.env = args.env or []
    env = [item for e in args.env for item in e.split(',')]

    # Process our subprocess call.
    # We need to escape every custom argument, so we
    # can ensure the args are properly passed if they
    # have spaces. We use single-quotes for the path,
    # and escape any characters and use double-quotes
    # for the command, to ensure we avoid any malicious
    # escapes. This allows us to have internal `'` characters
    # in our commands, without actually providing a dangerous escape.
    command = [args.engine, 'run', '--tty', '--name', args.image_name]
    if not args.non_interactive:
        command.append('--interactive')
    for var in env:
        command += ['--env', var]
    if args.quiet:
        command += ['--env', 'QUIET=1']
    # Docker by default uses root as the main user.
    # We therefore want to map to the current user.
    if args.engine_type == 'docker' and os.name == 'posix':
        euid = os.geteuid()
        command += ['--user', f'{euid}:{euid}']
    command += ['--volume', f'{parent_dir}:/src']
    command.append(get_image(args))

    # Now need to add the remaining arguments, the passed command over.
    script = f'/src/{relpath}/{args.script_name}'
    command += ['bash', script]

    return command

def process_args(argv=None):
    '''Parse arguments to the script.'''

    args, unknown = parser.parse_known_args(argv)
    args.command = unknown
    args.script_name = f'{base_script_name}{uuid.uuid4().hex}'
    args.image_name = args.script_name[3:]
    return args

def has_image(args):
    '''Check if a given image exists locally.'''

    devnull = subprocess.DEVNULL
    image = get_image(args)
    print_verbose(f'Finding if image {image} exists locally...', args.verbose)
    code = subprocess.call([args.engine, 'image', 'inspect', image], **args.subprocess_devnull)
    return code == 0

def pull_image(args):
    '''Pull the latest version of the image'''

    devnull = subprocess.DEVNULL
    image = get_image(args)
    kwds = {}
    print_verbose(f'Pulling image {image}...', args.verbose)
    if args.quiet:
        kwds = { 'stderr': devnull, 'stdout': devnull }
    code = subprocess.call([args.engine, 'pull', image], **kwds)
    if code != 0:
        error('Unable to pull image', code, show_help=False)

def remove_stopped_container(args):
    '''Remove the stopped container.'''

    # Don't care if this fails.
    print_verbose(f'Remove stopped container...', args.verbose)
    subprocess.call([args.engine, 'rm', args.image_name], **args.subprocess_devnull)

def remove_image(args):
    '''Pull the latest version of the image'''

    devnull = subprocess.DEVNULL
    image = get_image(args)
    print_verbose(f'Remove image {image} from local storage...', args.verbose)
    code = subprocess.call([args.engine, 'rmi', image], **args.subprocess_devnull)
    if code != 0:
        error('Unable to remove image', code, show_help=False)

def main(argv=None):
    '''Entry point'''

    # Parse and validate command-line options.
    args = process_args(argv)
    validate_arguments(args)

    # Update the image, if required.
    if args.update_image or not has_image(args):
        pull_image(args)

    # Normalize our paths here.
    parent_dir = get_parent_dir(args)
    current_dir = get_current_dir()
    if not os.path.isdir(parent_dir):
        error('`dir` is not a directory')
    if not current_dir.is_relative_to(parent_dir):
        error('`dir` must be a parent of the current working directory')
    relpath = current_dir.relative_to(parent_dir).as_posix()

    # Try to write the command to a script,
    # Do not use `exists` or `isfile`, then open, since
    # it could be written in between the time it was queried
    # and then written. We don't actually care enough to use
    # mkstemp, and since we create the file only if it doesn't
    # exist, in practice it's identical to mkstemp.
    print_verbose('Writing script to file...', args.verbose)
    open_flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        command = image_command(args, relpath)
        fd = os.open(args.script_name, open_flags)
        with os.fdopen(fd, 'w', newline='\n') as file:
            file.write(command)
    except OSError as err:
        if err.errno == errno.EEXIST:
            error(f'file {args.script_name} already exists. if you believe this is an error, delete {args.script_name}', show_help=False)
        else:
            # Unexpected error.
            raise

    # Create our docker command and call the script.
    print_verbose('Entering image and calling command...', args.verbose)
    try:
        code = subprocess.call(
            docker_command(args, parent_dir, relpath),
            shell=False,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    finally:
        print_verbose('Removing temporary files...', args.verbose)
        # Guarantee we cleanup the script afterwards.
        os.remove(args.script_name)
        remove_stopped_container(args)

        # Update the image, if required.
        if args.remove_image:
            remove_image(args)

    sys.exit(code)
