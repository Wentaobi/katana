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

from twisted.trial import unittest

from buildbot.steps.shell import ShellCommand, SetProperty
from buildbot.process.properties import WithProperties, Properties
from buildbot.process.factory import BuildFactory
from buildbot.sourcestamp import SourceStamp
from buildbot import config
from mock import Mock

class FakeSlaveBuilder:
    slave = None

class FakeBuilderStatus:
    reason = None

class FakeBuilder:
    builder_status = FakeBuilderStatus()
    botmaster = Mock()
    botmaster.master.config.globalFactory = {}

class FakeBuildStatus:
    def __init__(self):
        self.names = []
        self.results = None

    def addStepWithName(self, name, type):
        self.names.append(name)
        return FakeStepStatus()

    def getProperties(self):
        return Properties()

    def setSourceStamps(self, ss_list):
        self.ss_list = ss_list

    def setReason(self, reason):
        self.reason = reason

    def setSubmitted(self, submitted):
        self.submitted = submitted

    def setBuildChainID(self, buildChainID):
        self.buildChainID = buildChainID

    def setBuildRequestIDs(self, brids):
        self.brids = brids

    def setOwners(self, owners):
        self.owners = owners

    def setBlamelist(self, bl):
        self.bl = bl

    def setProgress(self, p):
        self.progress = p


class FakeStepStatus:
    txt = None
    finished = None

    def setText(self, txt):
        self.txt = txt

    def setProgress(self, sp):
        pass


class FakeBuildRequest:
    def __init__(self, reason, sources, buildername):
        self.id = None
        self.reason = reason
        self.sources = sources
        self.buildername = buildername
        self.changes = []
        self.submittedAt = None
        self.buildChainID = None
        self.properties = Properties()

    def mergeSourceStampsWith(self, others):
        return [source for source in self.sources.itervalues()]

    def mergeReasons(self, others):
        return self.reason

def setProperty(propname, value, source='Unknown', runtime=None):
    pass


class TestShellCommandProperties(unittest.TestCase):
    def testCommand(self):
        f = BuildFactory()
        f.addStep(SetProperty(command=["echo", "value"], property="propname"))
        f.addStep(ShellCommand(command=["echo", WithProperties("%(propname)s")]))

        ss = SourceStamp()

        req = FakeBuildRequest("Testing", {ss.repository:ss}, None)

        b = f.newBuild([req])
        b.build_status = FakeBuildStatus()
        b.slavebuilder = FakeSlaveBuilder()
        b.builder = FakeBuilder()
        b.setProperty = setProperty

        # This shouldn't raise an exception
        b.setupBuild(None)


class TestSetProperty(unittest.TestCase):
    def testGoodStep(self):
        f = BuildFactory()
        f.addStep(SetProperty(command=["echo", "value"], property="propname"))

        ss = SourceStamp()

        req = FakeBuildRequest("Testing", {ss.repository:ss}, None)

        b = f.newBuild([req])
        b.build_status = FakeBuildStatus()
        b.slavebuilder = FakeSlaveBuilder()
        b.builder = FakeBuilder()
        b.setProperty = setProperty

        # This shouldn't raise an exception
        b.setupBuild(None)

    def testErrorBothSet(self):
        self.assertRaises(config.ConfigErrors,
                SetProperty, command=["echo", "value"], property="propname", extract_fn=lambda x:{"propname": "hello"})

    def testErrorNoneSet(self):
        self.assertRaises(config.ConfigErrors,
                SetProperty, command=["echo", "value"])
