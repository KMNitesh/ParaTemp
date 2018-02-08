"""
Contains a class for containing multiple replica Universes in a single object.

This module defines a class that will contain Universes for each replica in a
replica exchange simulation.
While each replica can be defined individually, this adds a convenient
container for logically similar trajectories and allows easy iteration over
and access to the individual replica Universes.
"""

########################################################################
#                                                                      #
# This  was written by Thomas Heavey in 2018.                          #
#        theavey@bu.edu     thomasjheavey@gmail.com                    #
#                                                                      #
# Copyright 2018 Thomas J. Heavey IV                                   #
#                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");      #
# you may not use this file except in compliance with the License.     #
# You may obtain a copy of the License at                              #
#                                                                      #
#    http://www.apache.org/licenses/LICENSE-2.0                        #
#                                                                      #
# Unless required by applicable law or agreed to in writing, software  #
# distributed under the License is distributed on an "AS IS" BASIS,    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or      #
# implied.                                                             #
# See the License for the specific language governing permissions and  #
# limitations under the License.                                       #
#                                                                      #
########################################################################

import collections
import errno
import glob
import numpy as np
import os
import six
from .coordinate_analysis import Universe
from . import get_temperatures, exceptions


def find_nearest_idx(array, value):
    return (np.abs(array - value)).argmin()


class PTUniverse(collections.Sequence):

    def __init__(self, topology, base_folder,
                 trajs=None, traj_glob='*.xtc',
                 temps='TOPO/temperatures.dat'):
        # TODO document this
        self.base_folder = os.path.abspath(base_folder)
        self._top = self._fn(topology)
        self._trajs = self._get_trajs(trajs, traj_glob)
        self._temps = self._get_temps(temps)
        if len(self._temps) != len(self._trajs):
            raise ValueError(
                'len of temps ({}) not same'.format(len(self._temps)) +
                ' as len of trajs ({})'.format(len(self._trajs)))
        self._trajs.sort()
        self._trajs.sort(key=len)
        # TODO find more sure way to match temp to trajectory
        self.universes = np.array(
            [Universe(self._top, t, temp=self._temps[i])
             for i, t in enumerate(self._trajs)])

    def _fn(self, path):
        # TODO document this
        if os.path.isfile(path):
            return os.path.abspath(path)
        elif os.path.isfile(os.path.join(self.base_folder, path)):
            return os.path.abspath(os.path.join(self.base_folder, path))
        else:
            raise OSError(errno.ENOENT,
                          '{} not found here or under base_folder'.format(path))

    def _get_temps(self, temps):
        # TODO document this
        if isinstance(temps, six.string_types):
            return get_temperatures(self._fn(temps))
        else:
            return np.array(temps)

    def _get_trajs(self, trajs, traj_glob):
        # TODO document this
        if trajs is not None:
            return [self._fn(t) for t in trajs]
        elif isinstance(traj_glob, six.string_types):
            g1 = glob.glob(traj_glob)
            g2 = glob.glob(os.path.join(self.base_folder, traj_glob))
            if g1:
                return [self._fn(t) for t in g1]
            elif g2:
                return [self._fn(t) for t in g2]
            else:
                raise OSError(errno.ENOENT,
                              '{} did not seem to lead'.format(traj_glob) +
                              ' to any files here or under base_folder')
        else:
            raise exceptions.InputError((trajs, traj_glob),
                                        'use trajs or traj_glob '
                                        'to find trajectory files')

    def __getitem__(self, i):
        # TODO document this
        if isinstance(i, int):
            if i > len(self) - 1:
                raise IndexError(
                    'index {} is '.format(i) +
                    'larger than the number of replicas present')
            return self.universes[i]
        if isinstance(i, six.string_types) or isinstance(i, float):
            return self.universes[find_nearest_idx(self._temps, float(i))]

    def __len__(self):
        # TODO document this
        return len(self.universes)

    def keys(self):
        # TODO document this
        # TODO possibly change precision based on spread of temperatures
        # (tenths might not always be precise enough for large systems)
        return ('{:.1f}'.format(t) for t in self._temps)

    def values(self):
        # TODO document this
        return self.universes

    def items(self):
        # TODO document this
        return zip(self.keys(), self.values())
