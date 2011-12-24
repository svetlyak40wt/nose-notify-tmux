# -*- coding: utf-8 -*-
"""
nosenotifytmux.plugin
~~~~~~~~~~~~~~~~~

Nose plugin implementation.

:copyright: 2011, Alexander Artemenko <svetlyak.40wt@gmail.com>
:license: BSD, see doc/LICENSE for more details.
"""

import subprocess
from nose.plugins import Plugin


class NotifyPlugin(Plugin):
    """Enable Tmux notifications."""
    name = 'tmux'

    def begin(self):
        """Optionaly displays the start message."""
        subprocess.call('tmux rename-window testing', shell=True)

    def finalize(self, result=None):
        """Display success or failure message."""
        if result.wasSuccessful():
            subprocess.call('tmux rename-window done', shell=True)
            subprocess.call('tmux window-status-bg %s' % self.normal_color, shell=True)
        else:
            subprocess.call('tmux rename-window failed', shell=True)
            subprocess.call('tmux window-status-bg %s' % self.error_color, shell=True)

    def options(self, parser, env):
        super(NotifyPlugin, self).options(parser, env)
        parser.add_option('--normal-color',
                          action='store',
                          dest='normal_color',
                          default='green')
        parser.add_option('--error-color',
                          action='store',
                          dest='error_color',
                          default='red')
        options, args = parser.parse_args()
        self.error_color = options.error_color
        self.normal_color = options.normal_color

