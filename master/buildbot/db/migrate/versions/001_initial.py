# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from __future__ import with_statement

import os
import cPickle
from twisted.persisted import styles
from buildbot.util import json
import sqlalchemy as sa
from migrate.changeset import constraint

metadata = sa.MetaData()

last_access = sa.Table('last_access', metadata,
    sa.Column('who', sa.String(256), nullable=False),
    sa.Column('writing', sa.Integer, nullable=False),
    sa.Column('last_access', sa.Integer, nullable=False),
)

changes_nextid = sa.Table('changes_nextid', metadata,
    sa.Column('next_changeid', sa.Integer),
)

changes = sa.Table('changes', metadata,
    sa.Column('changeid', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('author', sa.String(255), nullable=False),
    sa.Column('comments', sa.String(1024), nullable=False),
    sa.Column('is_dir', sa.SmallInteger, nullable=False),
    sa.Column('branch', sa.String(255)),
    sa.Column('revision', sa.String(255)),
    sa.Column('revlink', sa.String(256)),
    sa.Column('when_timestamp', sa.Integer, nullable=False),
    sa.Column('category', sa.String(255)),
)

change_links = sa.Table('change_links', metadata,
    sa.Column('changeid', sa.Integer, nullable=False),
    sa.Column('link', sa.String(1024), nullable=False),
)

change_files = sa.Table('change_files', metadata,
    sa.Column('changeid', sa.Integer, nullable=False),
    sa.Column('filename', sa.String(1024), nullable=False),
)

change_properties = sa.Table('change_properties', metadata,
    sa.Column('changeid', sa.Integer, nullable=False),
    sa.Column('property_name', sa.String(256), nullable=False),
    sa.Column('property_value', sa.String(1024), nullable=False),
)

schedulers = sa.Table("schedulers", metadata,
    sa.Column('schedulerid', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('name', sa.String(128), nullable=False),
    sa.Column('state', sa.String(1024), nullable=False),
)

scheduler_changes = sa.Table('scheduler_changes', metadata,
    sa.Column('schedulerid', sa.Integer),
    sa.Column('changeid', sa.Integer),
    sa.Column('important', sa.SmallInteger),
)

scheduler_upstream_buildsets = sa.Table('scheduler_upstream_buildsets', metadata,
    sa.Column('buildsetid', sa.Integer),
    sa.Column('schedulerid', sa.Integer),
    sa.Column('active', sa.SmallInteger),
)

sourcestamps = sa.Table('sourcestamps', metadata,
    sa.Column('id', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('branch', sa.String(256)),
    sa.Column('revision', sa.String(256)),
    sa.Column('patchid', sa.Integer),
)

patches = sa.Table('patches', metadata,
    sa.Column('id', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('patchlevel', sa.Integer, nullable=False),
    sa.Column('patch_base64', sa.Text, nullable=False),
    sa.Column('subdir', sa.Text),
)

sourcestamp_changes = sa.Table('sourcestamp_changes', metadata,
    sa.Column('sourcestampid', sa.Integer, nullable=False),
    sa.Column('changeid', sa.Integer, nullable=False),
)

buildsets = sa.Table('buildsets', metadata,
    sa.Column('id', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('external_idstring', sa.String(256)),
    sa.Column('reason', sa.String(256)),
    sa.Column('sourcestampid', sa.Integer, nullable=False),
    sa.Column('submitted_at', sa.Integer, nullable=False),
    sa.Column('complete', sa.SmallInteger, nullable=False, server_default=sa.DefaultClause("0")),
    sa.Column('complete_at', sa.Integer),
    sa.Column('results', sa.SmallInteger),
)

buildset_properties = sa.Table('buildset_properties', metadata,
    sa.Column('buildsetid', sa.Integer, nullable=False),
    sa.Column('property_name', sa.String(256), nullable=False),
    sa.Column('property_value', sa.String(1024), nullable=False),
)

buildrequests = sa.Table('buildrequests', metadata,
    sa.Column('id', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('buildsetid', sa.Integer, nullable=False),
    sa.Column('buildername', sa.String(length=255), nullable=False),
    sa.Column('priority', sa.Integer, nullable=False, server_default=sa.DefaultClause("0")),
    sa.Column('claimed_at', sa.Integer, server_default=sa.DefaultClause("0")),
    sa.Column('claimed_by_name', sa.String(length=255)),
    sa.Column('claimed_by_incarnation', sa.String(length=256)),
    sa.Column('complete', sa.Integer, server_default=sa.DefaultClause("0")),
    sa.Column('results', sa.SmallInteger),
    sa.Column('submitted_at', sa.Integer, nullable=False),
    sa.Column('complete_at', sa.Integer),
)

builds = sa.Table('builds', metadata,
    sa.Column('id', sa.Integer, autoincrement=False, primary_key=True),
    sa.Column('number', sa.Integer, nullable=False),
    sa.Column('brid', sa.Integer, nullable=False),
    sa.Column('start_time', sa.Integer, nullable=False),
    sa.Column('finish_time', sa.Integer),
)

def test_unicode(migrate_engine):
    """Test that the database can handle inserting and selecting Unicode"""
    # set up a subsidiary MetaData object to hold this temporary table
    submeta = sa.MetaData()
    submeta.bind = migrate_engine

    test_unicode = sa.Table('test_unicode', submeta,
        sa.Column('u', sa.Unicode(length=100)),
        sa.Column('b', sa.LargeBinary),
    )
    test_unicode.create()

    # insert a unicode value in there
    u = u"Frosty the \N{SNOWMAN}"
    b='\xff\xff\x00'
    ins = test_unicode.insert().values(u=u, b=b)
    migrate_engine.execute(ins)

    # see if the data is intact
    row = migrate_engine.execute(sa.select([test_unicode])).fetchall()[0]
    assert type(row['u']) is unicode
    assert row['u'] == u
    assert type(row['b']) is str
    assert row['b'] == b

    # drop the test table
    test_unicode.drop()

def import_changes(migrate_engine):
    # get the basedir from the engine - see model.py if you're wondering
    # how it got there
    basedir = migrate_engine.buildbot_basedir

    # strip None from any of these values, just in case
    def remove_none(x):
        if x is None: return u""
        elif isinstance(x, str):
            return x.decode("utf8")
        else:
            return x

    # if we still have a changes.pck, then we need to migrate it
    changes_pickle = os.path.join(basedir, "changes.pck")
    if not os.path.exists(changes_pickle):
        migrate_engine.execute(changes_nextid.insert(),
                next_changeid=1)
        return

    #if not quiet: print "migrating changes.pck to database"

    # 'source' will be an old b.c.changes.ChangeMaster instance, with a
    # .changes attribute.  Note that we use 'r', and not 'rb', because these
    # pickles were written using the old text pickle format, which requires
    # newline translation
    with open(changes_pickle,"r") as f:
        source = cPickle.load(f)
    styles.doUpgrade()

    #if not quiet: print " (%d Change objects)" % len(source.changes)

    # first, scan for changes without a number.  If we find any, then we'll
    # renumber the changes sequentially
    have_unnumbered = False
    for c in source.changes:
        if c.revision and c.number is None:
            have_unnumbered = True
            break
    if have_unnumbered:
        n = 1
        for c in source.changes:
            if c.revision:
                c.number = n
                n = n + 1

    # insert the changes
    for c in source.changes:
        if not c.revision:
            continue
        try:
            values = dict(
                    changeid=c.number,
                    author=c.who,
                    comments=c.comments,
                    is_dir=c.isdir,
                    branch=c.branch,
                    revision=c.revision,
                    revlink=c.revlink,
                    when_timestamp=c.when,
                    category=c.category)
            values = dict([ (k, remove_none(v)) for k, v in values.iteritems() ])
        except UnicodeDecodeError, e:
            raise UnicodeError("Trying to import change data as UTF-8 failed.  Please look at contrib/fix_changes_pickle_encoding.py: %s" % str(e))

        migrate_engine.execute(changes.insert(), **values)

        # NOTE: change_links is not populated, since it is deleted in db
        # version 20.  The table is still created, though.

        # sometimes c.files contains nested lists -- why, I do not know!  But we deal with
        # it all the same - see bug #915. We'll assume for now that c.files contains *either*
        # lists of filenames or plain filenames, not both.
        def flatten(l):
            if l and type(l[0]) == list:
                rv = []
                for e in l:
                    if type(e) == list:
                        rv.extend(e)
                    else:
                        rv.append(e)
                return rv
            else:
                return l
        for filename in flatten(c.files):
            migrate_engine.execute(change_files.insert(),
                    changeid=c.number,
                    filename=filename)

        for propname,propvalue in c.properties.properties.items():
            encoded_value = json.dumps(propvalue)
            migrate_engine.execute(change_properties.insert(),
                    changeid=c.number,
                    property_name=propname,
                    property_value=encoded_value)

    # update next_changeid
    max_changeid = max([ c.number for c in source.changes if c.revision ] + [ 0 ])
    migrate_engine.execute(changes_nextid.insert(),
            next_changeid=max_changeid+1)

    #if not quiet:
    #    print "moving changes.pck to changes.pck.old; delete it or keep it as a backup"
    os.rename(changes_pickle, changes_pickle+".old")

def add_constraints(migrate_engine):
    metadata = sa.MetaData()
    metadata.bind = migrate_engine

    schedulers_tbl = sa.Table('schedulers', metadata, autoload=True)
    changes_tbl = sa.Table('changes', metadata, autoload=True)
    buildrequests_tbl = sa.Table('buildrequests', metadata, autoload=True)
    buildsets_tbl = sa.Table('buildsets', metadata, autoload=True)
    scheduler_changes_tbl = sa.Table('scheduler_changes', metadata, autoload=True)
    scheduler_upstream_buildsets_tbl = sa.Table('scheduler_upstream_buildsets', metadata, autoload=True)
    change_files_tbl = sa.Table('change_files', metadata, autoload=True)
    change_links_tbl = sa.Table('change_links', metadata, autoload=True)
    change_properties_tbl = sa.Table('change_properties', metadata, autoload=True)
    sourcestamp_changes_tbl = sa.Table('sourcestamp_changes', metadata, autoload=True)
    builds_tbl = sa.Table('builds', metadata, autoload=True)
    buildset_properties_tbl = sa.Table('buildset_properties', metadata, autoload=True)
    sourcestamps_tbl = sa.Table('sourcestamps', metadata, autoload=True)
    patches_tbl = sa.Table('patches', metadata, autoload=True)

    cons = constraint.ForeignKeyConstraint([scheduler_changes_tbl.c.schedulerid], [schedulers_tbl.c.schedulerid])
    cons.create()
    cons = constraint.ForeignKeyConstraint([scheduler_upstream_buildsets_tbl.c.schedulerid], [schedulers_tbl.c.schedulerid])
    cons.create()
    cons = constraint.ForeignKeyConstraint([change_files_tbl.c.changeid], [changes_tbl.c.changeid])
    cons.create()
    cons = constraint.ForeignKeyConstraint([change_links_tbl.c.changeid], [changes_tbl.c.changeid])
    cons.create()
    cons = constraint.ForeignKeyConstraint([change_properties_tbl.c.changeid], [changes_tbl.c.changeid])
    cons.create()
    cons = constraint.ForeignKeyConstraint([sourcestamp_changes_tbl.c.changeid], [changes_tbl.c.changeid])
    cons.create()
    cons = constraint.ForeignKeyConstraint([builds_tbl.c.brid], [buildrequests_tbl.c.id])
    cons.create()
    cons = constraint.ForeignKeyConstraint([buildset_properties_tbl.c.buildsetid], [buildsets_tbl.c.id])
    cons.create()
    cons = constraint.ForeignKeyConstraint([buildrequests_tbl.c.buildsetid], [buildsets_tbl.c.id])
    cons.create()
    cons = constraint.ForeignKeyConstraint([sourcestamps_tbl.c.patchid], [patches_tbl.c.id])
    cons.create()
    cons = constraint.ForeignKeyConstraint([sourcestamp_changes_tbl.c.sourcestampid], [sourcestamps_tbl.c.id])
    cons.create()
    cons = constraint.ForeignKeyConstraint([buildsets_tbl.c.sourcestampid], [sourcestamps_tbl.c.id])
    cons.create()

def upgrade(migrate_engine):
    metadata.bind = migrate_engine

    # do some tests before getting started
    test_unicode(migrate_engine)

    # create the initial schema
    metadata.create_all()

    # and import some changes
    import_changes(migrate_engine)

    add_constraints(migrate_engine)
