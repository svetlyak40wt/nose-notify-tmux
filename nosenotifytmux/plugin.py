# -*- coding: utf-8 -*-
"""
nosenotifytmux.plugin
~~~~~~~~~~~~~~~~~

Nose plugin implementation.

:copyright: 2011-2012, Alexander Artemenko <svetlyak.40wt@gmail.com>
:license: BSD, see doc/LICENSE for more details.
"""

import os
import subprocess
import atexit

from nose.plugins import Plugin


class NotifyPlugin(Plugin):
    """Enable Tmux notifications."""
    name = 'tmux'
    _total_tests = 0
    _progress = 0
    _finalized = False

    def begin(self):
        """Optionaly displays the start message."""
        if self.pane is not None:
            subprocess.call('tmux rename-window -t {pane} testing'.format(pane=self.pane), shell=True)
            subprocess.call('tmux set-option -t {pane} window-status-bg {color} | grep ignore'.format(pane=self.pane, color=self.progress_color), shell=True)

        atexit.register(self.finalize)

    def finalize(self, result=None):
        """Display success or failure message."""

        if self._finalized:
            return

        if self.pane is not None:
            if result is None:
                subprocess.call('tmux rename-window -t {pane} interrupted'.format(pane=self.pane), shell=True)
                subprocess.call('tmux set-option -t {pane} -u window-status-bg | grep ignore'.format(pane=self.pane), shell=True)
            else:
                if result.wasSuccessful():
                    subprocess.call('tmux rename-window -t {pane} done > /dev/null'.format(pane=self.pane), shell=True)
                    subprocess.call('tmux set-option -t {pane} -u window-status-bg | grep ignore'.format(pane=self.pane), shell=True)
                else:
                    subprocess.call('tmux rename-window -t {pane} failed'.format(pane=self.pane), shell=True)
                    subprocess.call('tmux set-option -t {pane} window-status-bg {color} | grep ignore'.format(pane=self.pane, color=self.error_color), shell=True)

        self._finalized = True

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

    def prepareTest(self, test):
        self._total_tests += test.countTestCases()
        return test

