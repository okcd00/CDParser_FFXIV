# -*- coding: UTF-8 -*-
# =====================================================
#   Copyright (C) since 2022 All rights reserved.
#
#   filename : acglogs_console.py
#   author   : okcd00 / okcd00@qq.com
#   date     : 2022-03-30
#   desc     : for actlogs.
# =====================================================
import ctypes
import pandas as pd
from pprint import pprint
from Triggernometry.id_mapping import ACTION_ID_MAPPING, STATUS_FLAG_ID_MAPPING


def hex2float(s):
    if not s.startswith('0x'):
        s = f"0x{s}"
    cp = ctypes.pointer(ctypes.c_longlong(s))
    fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_double))
    return fp.contents.value


def float2hex(s):
    fp = ctypes.pointer(ctypes.c_double(s))
    cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_longlong))
    return hex(cp.contents.value)


def leftpad(s):
    return f"{s:0>8}"


class ActLogs(object):
    def __init__(self, path=None, show_form='dict'):
        if path is None:
            path = "./data/hdl.log"
        self.job_name = 'summoner'
        self.show_form = show_form  # raw/dict
        self.raw_lines = [line.strip() for line in open(path, 'r')]
        self.raw_indexes = list(range(len(self.raw_lines)))
        self.lines = self.parse(self.raw_lines)

        # drop un-focused logs
        action_ids = ['14', '15', '16', '17', '18', '19', '1A', '1E', '1F', '25', '26', '29']
        action_names = None  # ['弗萝北']
        self.focus(action_ids, action_names)

    def __getitem__(self, key):
        if self.show_form == 'dict':
            return self.lines[key]
        return self.raw_lines[self.raw_indexes[key]]

    def __len__(self):
        return len(self.raw_indexes)

    def parse_job(self, feat_a, feat_b, feat_c, feat_d):
        info = {}
        if self.job_name in ['summoner']:
            # hex_b = eval(f"0x{feat_b}")
            hex_c = eval(f"0x{feat_c}")
            active = {
                'Ruby': 0x4,
                'Topaz': 0x8,
                'Emerald': 0xC
            }.get(hex_c & 0xC, "None")
            summon_stack = int(feat_b[1])
            summon = [
                'Ruby' if hex_c & 0x20 else '', 
                'Topaz' if hex_c & 0x40 else '', 
                'Emerald' if hex_c & 0x80 else '', 
            ]
            info = {
                'feat_a': feat_a,
                'feat_b': feat_b,
                'feat_c': feat_c,
                'feat_d': feat_d,
                'active': active,
                'summon': summon,
                'summon_stack': summon_stack,
                'next_attach': 'Phoenix' if hex_c & 0x10 else 'Bahamut',
                'aetherflow': hex_c & 0x3,
            }
        return info

    def parse_detail(self, items):
        info = {}
        action_id = items[0]
        if action_id == '03':  # AddCombatant
            info = {
                'source_id': items[1],  # '4000B9AA' 
                'source_name': items[2],  # '幻日' 
                # 00 
                # 59
                'combatant_owner': items[5], # 0000
                # 00
                # ''
                # 8-9 10451 13553
                'source_hp': items[10],  # '40917'
                'source_maxhp': items[11],  # '40917'
                'source_mp': items[12],  # '10000'
                'source_maxmp': items[13],  # '10000'
                # 14-15 ''
                # 16-19 100.00 100.00 0.00 0.00
            }
        elif action_id == '04':  # RemoveCombatant
            info = {
                'source_id': items[1],  # '4000B888' 
                'source_name': items[2],  # '宝石兽' 
                # 00 
                # 59
                'source_owner': items[5], # 10195F52
                # 00
                # ''
                # 8-9 10261 13498
                'source_hp': items[10],  # '0'
                'source_maxhp': items[11],  # '39066'
                'source_mp': items[12],  # '0'
                'source_maxmp': items[13],  # '10000'
                # 14-15 ''
                'source_position': items[16:20],  # 99.75 88.55 0.00 -2.71
            }
        elif action_id == '14':  # StartsCasting
            info = {
                'source_id': items[1],  # '10195F52' 
                'source_name': items[2],  # '弗萝北' 
                'skill_id': items[3],  # 'DFB'
                'skill_name': items[4],  # '毁荡'
                'target_id': items[5],  # '4000B887'
                'target_name': items[6],  # '海德林'
                'cast_time': items[7],  # '1.46'
                'source_position': items[8:12],  # 99.47 113.76 0.00 3.12
            }
        elif action_id == '15':  # ActionEffect
            info = {
                'source_id': items[1],  # '10195F52' 
                'source_name': items[2],  # '弗萝北' 
                'skill_id': items[3],  # 'DFB'
                'skill_name': items[4],  # '毁荡'
                'target_id': items[5],  # '4000B887'
                'target_name': items[6],  # '海德林'
                # 750003
                # 18E30000
                # 1B
                # DFB8000
                # 11-22 0
                'target_hp': items[23],  # '13065478'
                'target_maxhp': items[24],  # '13065478'
                'target_mp': items[25],  # '10000'
                'target_maxmp': items[26],  # '10000'
                # 27-28 ''
                'target_position': items[29:33],  # 99.99 90.00 0.00 0.00
                'source_hp': items[33],  # '40917'
                'source_maxhp': items[34],  # '40917'
                'source_mp': items[35],  # '10000'
                'source_maxmp': items[36],  # '10000'
                # 37-38 ''
                'source_position': items[39:43],  # 99.47 113.76 0.00 3.12
                # 0000640D
                # 0
                # 1
            }
        elif action_id == '16':  # AOEActionEffect
            info = {
                'source_id': items[1],  # '10195F52' 
                'source_name': items[2],  # '弗萝北' 
                'skill_id': items[3],  # '61F9'
                'skill_name': items[4],  # '光之心'
                'target_id': items[5],  # '4000B886'
                'target_name': items[6],  # '桑克瑞德'
                # F60E
                # 72F0000
                # 9-22 0
                'target_hp': items[23],  # '56180'
                'target_maxhp': items[24],  # '63976'
                'target_mp': items[25],  # '34464'
                'target_maxmp': items[26],  # '10000'
                # 27-28 ''
                'target_position': items[29:33],  # 99.99 90.00 0.00 0.00
                'source_hp': items[33],  # '56180'
                'source_maxhp': items[34],  # '63976'
                'source_mp': items[35],  # '34464'
                'source_maxmp': items[36],  # '10000'
                # 37-38 ''
                'source_position': items[39:43],  # 99.47 113.76 0.00 3.12
                # 00006459
                # 0
                # 3
            }
        elif action_id == '17':  # CancelAction
            info = {
                'source_id': items[1],  # '10195F52' 
                'source_name': items[2],  # '弗萝北' 
                'skill_id': items[3],  # '6264'
                'skill_name': items[4],  # '血盟骇水'
                'is_canceled': items[5],  # 'Cancelled'
            }
        elif action_id == '18':  # DoTHoT
            info = {
                'source_id': items[1],  # '10195F52' 
                'source_name': items[2],  # '弗萝北' 
                'dot_or_hot': items[3],  # 'HoT'
                # 0
                # '1102'
                'target_hp': items[6],  # '56180'
                'target_maxhp': items[7],  # '63976'
                'target_mp': items[8],  # '34464'
                'target_maxmp': items[9],  # '10000'
                # 27-28 ''
                'target_position': items[29:33],  # 100.02 88.27 0.00 -0.02
            }
        elif action_id == '19':  # Death
            info = {
                'source_id': items[1],  # '4000BB0E'
                'source_name': items[2],  # '光之水晶'
                'target_id': items[3],  # '4000B885'
                'target_name': items[4],  # '古·拉哈·提亚'
            }
        elif action_id == '1A':  # StatusAdd
            info = {
                'skill_id': items[1],  # '7AC' 
                'skill_name': items[2],  # '发动技能待命II' 
                'dur_time': items[3],  # 30.00
                'source_id': items[4],  # '4000B888'
                'source_name': items[5],  # '宝石兽'
                'target_id': items[6],  # '4000B888'
                'target_name': items[7],  # '宝石兽'
                'status_flag': STATUS_FLAG_ID_MAPPING.get(items[8], items[8]), # 00/01/1E/4B
                'target_maxhp': items[9],  # '40155'
                'source_maxhp': items[10],  # '63976'
            }
        elif action_id == '1E':  # StatusRemove
            info = {
                'skill_id': items[1],  # '7AC' 
                'skill_name': items[2],  # '发动技能待命II' 
                'dur_time': items[3],  # 0.00
                'source_id': items[4],  # '4000B886'
                'source_name': items[5],  # '桑克瑞德'
                'target_id': items[6],  # '4000B881'
                'target_name': items[7],  # '雅·修特拉'
                'status_flag': STATUS_FLAG_ID_MAPPING.get(items[8], items[8]), # 00/01/1E/4B
                'target_maxhp': items[9],  # '40155'
                'source_maxhp': items[10],  # '63976'
            }
        elif action_id == '1F':  # Gauge
            info = {
                'source_id': leftpad(items[1]),  # '10195F52'
            }
            info.update(self.parse_job(
                leftpad(items[2]),  # 1B
                leftpad(items[3]),  # 00
                leftpad(items[4]),  # '10195F52'
                leftpad(items[5]),  # 00
            ))
        elif action_id == '24':  # LimitBreak
            info = {
                # 0096
                'limit_burst_level': items[2],
            }
        elif action_id == '25':  # EffectResult
            info = {
                'source_id': items[1],  # '4000B887' 
                'source_name': items[2],  # '海德林' 
                # 0000640D 
                # 13059107
                # 5-9 ''
                'source_position': items[10:14],  # 99.99 90.00 0.00 0.00
            }
        elif action_id == '26':  # StatusList
            info = {
                'source_id': items[1],  # '4000B888' 
                'source_name': items[2],  # '宝石兽' 
                # 00595900 
                'source_hp': items[4],  # '39066'
                'source_maxhp': items[5],  # '39066'
                'source_mp': items[6],  # '10000'
                'source_maxmp': items[7],  # '10000'
                # 0
                # ''
                'source_position': items[10:14],  # 99.75 88.55 0.00 -2.71
                # 5C44
                # DE
                # 0
            }
        elif action_id == '27':  # UpdateHp
            info = {
                'source_id': items[1],  # '10195F52' 
                'source_name': items[2],  # '弗萝北' 
                'source_hp': items[3],  # '40917'
                'source_maxhp': items[4],  # '40917'
                'source_mp': items[5],  # '10000'
                'source_maxmp': items[6],  # '10000'
                # 7-8 ''
                'source_position': items[9:13],  # 99.47 113.76 0.00 3.12
            }
        info.update({'action_id': items[0]})
        return info

    def parse(self, line):
        if isinstance(line, list):
            return [self.parse(_line) for _line in line]
        sys_time = line.split(' ')[0].strip('[]')
        action_type = line.split(' ')[1]
        items = line.split(' ')[2].split(':')
        results = {
            'time': sys_time,
            'action_id': items[0],
            'action_type': action_type,
            # 'other_items': list(enumerate(items))
        }
        try:
            results.update(self.parse_detail(items))
        except Exception as e:
            print(e)
            print(items)
        return results

    def focus(self, focus_action_ids=None, focus_action_names=None):
        _raw_indexes, _lines = [], []
        for line_id, line in zip(self.raw_indexes, self.lines):
            if focus_action_ids:
                if line['action_id'] not in focus_action_ids:
                    continue
            source_name = line.get('source_name')
            if focus_action_names:
                if source_name and source_name not in focus_action_names:
                    continue
            _raw_indexes.append(line_id)
            _lines.append(line)
        self.raw_indexes = _raw_indexes
        self.lines = _lines

    def dump(self, dump_path):
        with open(dump_path, 'w') as f:
            print(f"Now writing {len(self.raw_indexes)} lines into {dump_path}")
            for line_id in self.raw_indexes:
                f.write(f"{self.raw_lines[line_id]}\n")