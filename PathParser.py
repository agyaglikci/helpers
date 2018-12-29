#!/usr/bin/python

import os

class PathParser(object):

    def __init__(self, template):
        self.path_parse_indices = {}
        prev_section = ""
        for section_index, section in enumerate(template):
            if section == prev_section:
                self.path_parse_indices[section][1] = section_index
            else:
                self.path_parse_indices[section] = [section_index] * 2
            prev_section = section


    def get_feature(self, path, key):
        path_parts = path.split('/')
        if key in self.path_parse_indices:
            if self.path_parse_indices[key][0] == self.path_parse_indices[key][1]:
                return path_parts[self.path_parse_indices[key][0]]
            else:
                return "_".join([path_parts[i] for i in range(self.path_parse_indices[key][0], self.path_parse_indices[key][1])])
