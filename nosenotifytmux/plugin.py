# -*- coding: utf-8 -*-
"""
nosenotifytmux.plugin
~~~~~~~~~~~~~~~~~

Nose plugin implementation.

:copyright: 2011, Alexander Artemenko <svetlyak.40wt@gmail.com>
:license: BSD, see doc/LICENSE for more details.
"""

import os
import subprocess
from functools import partial
from nose.plugins import Plugin


class NotifyPlugin(Plugin):
    """Enable Tmux notifications."""
    name = 'tmux'
    _total_tests = 0
    _progress = 0

    def begin(self):
        """Optionaly displays the start message."""
        if self.pane is not None:
            subprocess.call('tmux rename-window -t {pane} testing'.format(pane=self.pane), shell=True)
            subprocess.call('tmux set-option -t {pane} window-status-bg {color} | grep blah'.format(pane=self.pane, color=self.progress_color), shell=True)

    def finalize(self, result=None):
        """Display success or failure message."""
        if self.pane is not None:
            if result.wasSuccessful():
                subprocess.call('tmux rename-window -t {pane} done'.format(pane=self.pane), shell=True)
                subprocess.call('tmux set-option -t {pane} -u window-status-bg | grep blah'.format(pane=self.pane), shell=True)
            else:
                subprocess.call('tmux rename-window -t {pane} failed'.format(pane=self.pane), shell=True)
                subprocess.call('tmux set-option -t {pane} window-status-bg {color} | grep blah'.format(pane=self.pane, color=self.error_color), shell=True)

    def configure(self, options, conf):
        super(NotifyPlugin, self).configure(options, conf)
        self.pane = os.environ.get('TMUX_PANE')

    def options(self, parser, env):
        super(NotifyPlugin, self).options(parser, env)
        parser.add_option('--progress-color',
                          action='store',
                          dest='progress_color',
                          default='blue')
        parser.add_option('--error-color',
                          action='store',
                          dest='error_color',
                          default='red')
        options, args = parser.parse_args()
        self.progress_color = options.progress_color
        self.error_color = options.error_color

    def stopTest(self, test):
        self._progress += 1
        if self.pane is not None:
            subprocess.call(
                'tmux rename-window -t {pane} "testing {progress}%"'.format(
                    progress=100 * self._progress / self._total_tests,
                    pane=self.pane
                ),
                shell=True
            )

    def prepareTestLoader(self, loader):
        """Insert ourselves into loader calls to count tests.

        The top-level loader call often returns lazy results, like a LazySuite.
        This is a problem, as we would destroy the suite by iterating over it
        to count the tests. Consequently, we monkeypatch the top-level loader
        call to do the load twice: once for the actual test running and again
        to yield something we can iterate over to do the count.

        Stolen from nose-progressive.
        """
        def capture_suite(orig_method, *args, **kwargs):
            """Intercept calls to the loader before they get lazy.

            Re-execute them to grab a copy of the possibly lazy suite, and
            count the tests therein.

            """
            self._total_tests += orig_method(*args, **kwargs).countTestCases()
            return orig_method(*args, **kwargs)

        # TODO: If there's ever a practical need, also patch loader.suiteClass
        # or even TestProgram.createTests. createTests seems to be main top-
        # level caller of loader methods, and nose.core.collector() (which
        # isn't even called in nose) is an alternate one.
        if hasattr(loader, 'loadTestsFromNames'):
            loader.loadTestsFromNames = partial(capture_suite,
                                                loader.loadTestsFromNames)
        return loader

