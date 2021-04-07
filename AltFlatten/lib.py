# coding=utf-8
"""
AltFlatten version 1.1.0

Copyrights(c) 2021 altnoi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""
import maya.OpenMaya as om
import maya.cmds as cmds


class flattenLib(object):
    def __init__(self):
        self.base_standby = False
        self.is_area_limited = False
        self.error_message = ""
        self.vertex = [om.MVector(), om.MVector(), om.MVector()]
        self.vector = [om.MVector(), om.MVector()]
        self.tgt_vector = om.MVector()
        self.coefficient = []

    def setup_base(self):
        status = self.set_base_vertex()
        if status == 0:
            self.create_base_vector()
            self.base_standby = True

    def set_base_vertex(self):
        self.reset_status(False)
        selected_vertexes = cmds.ls(selection=True, fl=True)
        if len(selected_vertexes) != 3:
            self.error_message = "Error: Vertex counts wrong!!!"
            return -1
        else:
            for i in range(len(selected_vertexes)):
                position = cmds.pointPosition(selected_vertexes[i], world=True)
                self.vertex[i] = om.MVector(position[0], position[1], position[2])
            return 0

    def move_target_vertex(self):
        self.reset_status(self.base_standby)
        if self.base_standby:
            cmds.undoInfo(openChunk=True)
            selected_vertexes = cmds.ls(selection=True, fl=True)
            for i in range(len(selected_vertexes)):
                cmds.select(clear=True)
                position = cmds.pointPosition(selected_vertexes[i], world=True)
                position_vectored = om.MVector(position[0], position[1], position[2])
                self.origin_to_starts(position_vectored)
                forward_pos = self.calc_forward_position(position_vectored)
                cmds.select(selected_vertexes[i])
                cmds.move(forward_pos.x, forward_pos.y, forward_pos.z)
            cmds.undoInfo(closeChunk=True)
        else:
            self.error_message = "Setup base first!!!"

    def calc_forward_position(self, original_pos):
        self.set_coefficient()
        if self.justify_coefficient():
            s, t = self.linsolve()
            if self.is_area_limited and not self.is_inside(s, t):
                return original_pos
            pos = self.vector[0] * s + self.vector[1] * t + self.vertex[0]
            return pos
        else:
            return original_pos

    def create_base_vector(self):
        self.vector[0] = self.vertex[1] - self.vertex[0]
        self.vector[1] = self.vertex[2] - self.vertex[0]

    def origin_to_starts(self, start_vector):
        self.tgt_vector = start_vector - self.vertex[0]

    def set_coefficient(self):
        """
        Too long to explain this comment. See documentation.
        :return:
        """
        self.coefficient = []
        self.coefficient.append(self.vector[0].x ** 2 + self.vector[0].y ** 2 + self.vector[0].z ** 2)
        self.coefficient.append(self.vector[0].x * self.vector[1].x
                                + self.vector[0].y * self.vector[1].y
                                + self.vector[0].z * self.vector[1].z)
        self.coefficient.append((self.vector[0].x * self.tgt_vector.x
                                + self.vector[0].y * self.tgt_vector.y
                                + self.vector[0].z * self.tgt_vector.z))
        self.coefficient.append(self.vector[0].x * self.vector[1].x
                                + self.vector[0].y * self.vector[1].y
                                + self.vector[0].z * self.vector[1].z)
        self.coefficient.append(self.vector[1].x ** 2 + self.vector[1].y ** 2 + self.vector[1].z ** 2)
        self.coefficient.append((self.vector[1].x * self.tgt_vector.x
                                + self.vector[1].y * self.tgt_vector.y
                                + self.vector[1].z * self.tgt_vector.z))

    def justify_coefficient(self):
        """
        Zero div対策
        :return:
        """
        if self.coefficient[0] == 0:
            self.error_message = "Some vertex cannot solve, move a bit and try again"
            return False
        if self.coefficient[0] * self.coefficient[4] - self.coefficient[1] * self.coefficient[3] == 0:
            self.error_message = "Some vertex cannot solve, move a bit and try again"
            return False
        return True

    def linsolve(self):
        t = ((self.coefficient[0] * self.coefficient[5]) - (self.coefficient[2] * self.coefficient[3])) \
            / ((self.coefficient[0] * self.coefficient[4]) - (self.coefficient[1] * self.coefficient[3]))

        s = (self.coefficient[2] / self.coefficient[0]) - (t * (self.coefficient[1] / self.coefficient[0]))
        return [s, t]

    def is_inside(self, s, t):
        if (0 < s < 1) & (0 < t < 1) &(0 < 1-s-t < 1):
            return True
        return False

    def reset_status(self, is_standby):
        self.base_standby = is_standby
        self.error_message = ""
        self.tgt_vector = []
