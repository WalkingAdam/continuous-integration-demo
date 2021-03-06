# contains bunch of buggy examples taken from:
# https://hackernoon.com/10-common-security-gotchas-in-python-and-how-to-avoid-them-e19fbe265e03
import pickle
import subprocess
import base64
import re
import flask


# Input injection
def transcode_file(request, filename):
    command = 'ffmpeg -i "{source}" output_file.mpg'.format(source=filename)
    subprocess.call(command, shell=True)  # a bad idea!


# Assert statements
def permission_check(request, user):
    if not user.is_admin:
        raise PermissionError()
    # assert user.is_admin, 'user does not have access
    # secure code...


# Pickles
class RunBinSh:
    def __reduce__(self):
        return (subprocess.Popen, (('/bin/sh',),))


def import_urlib_version(version):
    if not re.match("^[\d.]+$", version):
        raise PermissionError()
    exec("import urllib%s as urllib" % version)


@flask.app.route('/')
def index():
    module = flask.request.args.get("module")
    import_urlib_version(module)


print(base64.b64encode(pickle.dumps(RunBinSh())))
