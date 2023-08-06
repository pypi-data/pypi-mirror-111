# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import git
import shutil
import re
from datetime import datetime

import click


def rename_dir(name, dr, hist):
    for root, dirs, files in os.walk(dr):
        if root == '.':
            p_dir = os.path.join(root, name)
            shutil.move(
                os.path.join(root, 'algus'), p_dir, copy_function=shutil.copytree)
            rename_dir(name, p_dir, hist)
            break

        for d in dirs:
            if d == '__pycache__' or d == '.git':
                shutil.rmtree(os.path.join(root, d))
                continue
            new_d = None
            if 'algus' in d:
                new_d = os.path.join(root, d.replace('algus', name))
            elif 'Algus' in d:
                new_d = os.path.join(root, d.replace('algus', name.capitalize()))
            if new_d:
                hist['dir_changed'] += 1
                shutil.move(
                    os.path.join(root, d), new_d, copy_function=shutil.copytree)
                d = new_d
            else:
                d = os.path.join(root, d)
            rename_dir(name, d, hist)

        for f in files:
            if f == __file__ or (not f.endswith('.py') and not f.endswith('.rst') and not f.endswith('.html')):
                continue
            hist['files'] += 1
            new_f = None
            if 'algus' in f:
                new_f = os.path.join(root, f.replace('algus', name))
            elif 'Algus' in f:
                new_f = os.path.join(root, f.replace('Algus', name.capitalize()))
            if new_f:
                hist['f_changed'] += 1
                shutil.move(os.path.join(root, f), new_f, copy_function=shutil.copy2)
                f = new_f
            else:
                f = os.path.join(root, f)
            cr = 'Copyright ' + str(datetime.today().year) + ' Rumma & Ko Ltd'
            with open(f, 'r+') as f:
                try:
                    c = f.read()
                    content = c.replace('algus', name).replace('Algus', name.capitalize())
                    content = re.sub(r'Copyright [0-9]{4} Rumma & Ko Ltd', cr, content)
                    content = re.sub(r'Copyright [0-9]{4}-[0-9]{4} Rumma & Ko Ltd', cr, content)
                    f.seek(0)
                    f.write(content)
                    f.truncate()
                    if content != c:
                        hist['edited'] += 1
                except UnicodeDecodeError as e:
                    print(f, e)

@click.command()
@click.argument('projectname')
@click.pass_context
def startproject(ctx, projectname):
    """

    Start a new Lino project/application.

    Takes one mandatory agrument `projectname` which is essentially the
    application name.

    """
    hist = dict(dir_changed=0, f_changed=0, files=0, edited=0)

    algus_backup = False
    if "algus" in os.listdir():
        print("Creating backup for lino_algus...")
        shutil.move(os.path.join('.', 'algus'), os.path.join('.', 'algus_bak'), copy_function=shutil.copytree)
        algus_backup = True

    print("Fetching project template...")
    git.Git().clone('https://gitlab.com/lino-framework/algus')

    print(f"Creating project lino_{projectname} from lino_algus...")
    rename_dir(projectname, '.', hist)

    print(f"Renamed {hist['dir_changed']} directories and {hist['f_changed']} files.")
    print(f"Found {hist['files']} files and modified {hist['edited']} files.")
    if algus_backup:
        print("Restoring lino_algus...")
        shutil.move(os.path.join('.', 'algus_bak'), os.path.join('.', 'algus'), copy_function=shutil.copytree)
    print("Done.")
