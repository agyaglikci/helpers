#!/usr/bin/python

import os

class PathParser(object):

    def __init__(self, template):
        self.path_parse_indices = {}
        self.num_parts_in_path = 0;
        prev_section = ""
        for section_index, section in enumerate(template):
            if section == prev_section:
                self.path_parse_indices[section][1] = section_index
            else:
                self.path_parse_indices[section] = [section_index, section_index]
            prev_section = section
            self.last_section_index = section_index

        self.num_parts_in_path = len(self.path_parse_indices.keys())
        print self.path_parse_indices


    def get_feature(self, path, key):
        path_parts = path.split('/')
        if key in self.path_parse_indices:
            if len(path_parts) > self.path_parse_indices[key][1]:
                return "_".join([path_parts[i] for i in range(self.path_parse_indices[key][0], self.path_parse_indices[key][1]+1)])
            else:
                print "path cannot be parsed",
                return False
        else:
            print key, "was never specified in template.",
            quit()

    def get_all_features(self, path):
        path_dict = {}
        path_parts = path.split('/')
        if len(path_parts) == self.last_section_index + 1:
            for key, indices in self.path_parse_indices.iteritems():
                path_dict[key] = "_".join([path_parts[i] for i in range(indices[0], indices[1]+1)])
            return path_dict
        else:
            print "path does not fit to template.",
            return False
