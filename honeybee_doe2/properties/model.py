# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*

""" HB-Model Doe2 (eQuest) Properties."""
from collections import defaultdict

from honeybee.model import Model
from honeybee.room import Room
from honeybee.face import Face
from honeybee_energy.construction.opaque import OpaqueConstruction

from .inputils import blocks as fb
from .inputils.compliance import ComplianceData
from .inputils.sitebldg import SiteBldgData as sbd
from .inputils.run_period import RunPeriod
from .inputils.title import Title

from .story import Doe2Story
from .constructions import Construction


class ModelDoe2Properties(object):
    """_summary_

    Args:
        object (_type_): _description_
    """

    def __init__(self, _host):
        self._host = _host

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        """_summary_
        Args:
            new_host (_type_, optional): _description_. Defaults to None.
        Returns:
            _type_: _description_
        """
        # type: (Any) -> ModelDoe2Properties
        _host = new_host or self._host
        new_properties_obj = ModelDoe2Properties(_host)
        return new_properties_obj

    @property
    def _header(self):
        """File header.
        NOTE: The header is currently read-only
        """
        return '\n'.join([fb.top_level, fb.abort_diag])

    @property
    def stories(self):
        # * do tuple, (geom, 'space room whatever') for each 'inpblock' per story
        return self._make_doe_stories(self.host)

    @staticmethod
    def _make_doe_stories(obj):
        grouped = Room.group_by_floor_height(obj.rooms, 0.1)
        stories = []
        for i, story in enumerate(grouped[0]):
            stories.append(Doe2Story(story, i))
        #nl = ''
        # return str(nl.join(str(s) for s in stories))
        return stories

    # @property
    # def polygons(self):
    #    return self._inp_polyblock_maker(self.host)

    # @staticmethod
    # def _inp_polyblock_maker(obj):
        # TODO: for story in stories: for room in story: for face in room.faces:
        #inp_block = '\n'
        #inp_polys = []
        # for room in obj.rooms:
        #    for face in obj.faces:  # eQuest can have interior walls
        #        inp_polys.append(face.properties.doe2.poly)
        #final = inp_block.join(pol for pol in inp_polys)
        ##return final  #

    @property
    def header(self):
        return '\n'.join([fb.top_level, fb.abort_diag])

    @property
    def mats_cons_layers(self):
        return self._make_mats_cons_layers(self.host)

    @staticmethod
    def _make_mats_cons_layers(obj):
        cons = []
        for construction in obj.properties.energy.constructions:
            if isinstance(construction, OpaqueConstruction):
                cons.append(Construction.from_hb_construction(construction).to_inp())

        return '\n'.join([l for l in cons])

    def __str__(self):
        return "Model Doe2 Properties: [host: {}]".format(self.host.display_name)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()
