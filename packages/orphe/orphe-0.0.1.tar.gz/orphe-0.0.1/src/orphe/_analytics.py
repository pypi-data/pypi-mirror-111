# Copyright 2020 Aptpod, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
from json.decoder import JSONDecodeError
import intdash
import numpy as np
import json
import asyncio
import pandas
import time
import queue
from typing import Callable, List
from ._gait import Gait, GaitAnalysis
from ._unit import Unit
    
class AnalyticsValue(object):
    gait : GaitAnalysis

    """ORPHE ANALYTICSから取得されたデータです。
    """
    def __init__(self, gait_analysis : GaitAnalysis) -> None:
        self.gait = gait_analysis

class Analytics(object):
    _queue : queue.Queue = queue.Queue(maxsize=0)
    _current_value : AnalyticsValue = None
    _current_time : int = None
    """intdash REST サーバーに対するアクセスクライアントです。

    Args:
        url (str): ORPHE ANALYTICS REST API サーバーの URL
        token (str): エッジトークン

    .. note::
        認証情報として、 **トークン** が必要です。
    """
    def __init__(self, url : str, token : str=None) -> None:
        self.url : str = url
        self.token : str = token
        
        self._client : intdash.Client = intdash.Client(
            url = url,
            edge_token = token,
        )
        
    # 辞書データ変換
    _json_dict = {
        "quatW": "SHOES_QUATERNION_W",
        "quatX": "SHOES_QUATERNION_X",
        "quatY": "SHOES_QUATERNION_Y",
        "quatZ": "SHOES_QUATERNION_Z",
        "gyroX": "SHOES_ANGULAR_VELOCITY_X",
        "gyroY": "SHOES_ANGULAR_VELOCITY_Y",
        "gyroZ": "SHOES_ANGULAR_VELOCITY_Z",
        "accX": "SHOES_ACC_X",
        "accY": "SHOES_ACC_Y",
        "accZ": "SHOES_ACC_Z",
        "gravityX": "SHOES_ACC_OF_GRAVITY_X",
        "gravityY": "SHOES_ACC_OF_GRAVITY_Y",
        "gravityZ": "SHOES_ACC_OF_GRAVITY_Z",
        "eulerX": "SHOES_EULER_ANGLE_X",
        "eulerY": "SHOES_EULER_ANGLE_Y",
        "eulerZ": "SHOES_EULER_ANGLE_Z"
    }
    
    _specs_filters =  [
        intdash.DataFilter(data_type=intdash.DataType.string.value, data_id='L_SHOES_JSON',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_QUATERNION_W',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_QUATERNION_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_QUATERNION_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_QUATERNION_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ACC_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ACC_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ACC_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ACC_OF_GRAVITY_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ACC_OF_GRAVITY_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ACC_OF_GRAVITY_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_EULER_ANGLE_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_EULER_ANGLE_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_EULER_ANGLE_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ANGULAR_VELOCITY_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ANGULAR_VELOCITY_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SHOES_ANGULAR_VELOCITY_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.string.value, data_id='R_SHOES_JSON',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_QUATERNION_W',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_QUATERNION_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_QUATERNION_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_QUATERNION_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ACC_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ACC_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ACC_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ACC_OF_GRAVITY_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ACC_OF_GRAVITY_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ACC_OF_GRAVITY_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_EULER_ANGLE_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_EULER_ANGLE_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_EULER_ANGLE_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ANGULAR_VELOCITY_X',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ANGULAR_VELOCITY_Y',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SHOES_ANGULAR_VELOCITY_Z',channel=1),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_STRIDE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_CADENCE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SPEED',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_DURATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_STANCEPHASEDURATIONE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_SWINGPHASEDURATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_CONTINUOUSSTANSPHASEDURATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_STRIKEANGLE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_PRONATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_LANDINGFORCE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_STRIDEMAXIMUMVERTICALHEIGHT',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='L_TOEOFFANGLE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_STRIDE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_CADENCE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SPEED',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_DURATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_STANCEPHASEDURATIONE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_SWINGPHASEDURATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_CONTINUOUSSTANSPHASEDURATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_STRIKEANGLE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_PRONATION',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_LANDINGFORCE',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_STRIDEMAXIMUMVERTICALHEIGHT',channel=3),
        intdash.DataFilter(data_type=intdash.DataType.float.value, data_id='R_TOEOFFANGLE',channel=3),
    ]

    def load(self, measurement_uuid : str) -> AnalyticsValue:
        
        # 計測の取得
        print(f'Search measurement uuid: {measurement_uuid}', flush=True)
        m = self._client.measurements.get(
            uuid = measurement_uuid
        )
            
        # 計測がない場合終了
        print(m)
        if m == np.nan:
            print("No measurements were found.", flush=True)
            return
            
        # ユニットの取得（小数点のみ）
        print(f'Load measurement: {measurement_uuid}', flush=True)
        us = self._client.units.list(
            start=m.basetime,
            end=m.basetime + m.duration * 2, # endの時刻時点の計測は検索対象に含まれないので、余分に2倍しておく
            measurement_uuid=m.uuid,
            limit=0,
        )
            
        left_us = [u for u in us if u.channel != 0 and (u.data.data_type.value == intdash.DataType.float.value or u.data.data_type.value == intdash.DataType.string.value) and u.data.data_id[0] == 'L']
        right_us = [u for u in us if u.channel != 0 and (u.data.data_type.value == intdash.DataType.float.value or u.data.data_type.value == intdash.DataType.string.value) and u.data.data_id[0] == 'R']

        start = time.time()
        print(f"Measurement name: {m.name}", flush=True)
        print(f"Start: {start}", flush=True)
        print(f"Length: {len(us)}", flush=True)

        gait_analysis = GaitAnalysis()
        tmp : dict[pandas.Timedelta,Gait] = {}
        for unit in left_us:
            # Skip basetime.
            if unit.data.data_type.value == intdash.DataType.basetime.value:
                continue
        
            # Skip other data.
            if unit.data.data_type.value == intdash.DataType.float.value:
                # センサーデータを取得
                sensor_data = unit.data

                # 計測時間取得
                # total_time_seconds = unit.elapsed_time.total_seconds()
                elapsed_time =unit.elapsed_time
                
                if elapsed_time in tmp:
                    gait = tmp[elapsed_time]
                    gait._set(sensor_data.data_id[2:], sensor_data.value)
                else:
                    gait = Gait(time = elapsed_time)
                    gait._set(sensor_data.data_id[2:], sensor_data.value)
                    tmp[elapsed_time] = gait
            
            elif unit.data.data_type.value == intdash.DataType.string.value:
                
                try:
                    # センサーデータを取得
                    sensor_data = unit.data
                    # Jsonデシリアライズ
                    # print(sensor_data.value)
                    sensor_data_json = json.loads(sensor_data.value)
                    #side = sensor_data.data_id[0]

                    # 計測時間取得
                    # total_time_seconds = unit.elapsed_time.total_seconds()
                    elapsed_time =unit.elapsed_time

                    for key in self._json_dict:
                        if elapsed_time in tmp:
                            gait = tmp[elapsed_time]
                            gait._set(self._json_dict[key], sensor_data_json[key])
                        else:
                            gait = Gait(time = elapsed_time)
                            gait._set(self._json_dict[key], sensor_data_json[key])
                            tmp[elapsed_time] = gait
                    
                except json.JSONDecodeError:
                    continue
        
        gait_analysis.left = sorted(tmp.values(), key=lambda gait:gait.time)
        tmp : dict[pandas.Timedelta,Gait] = {}
                
        for unit in right_us:
            # Skip basetime.
            if unit.data.data_type.value == intdash.DataType.basetime.value:
                continue
        
            # Skip other data.
            if unit.data.data_type.value == intdash.DataType.float.value:
                # センサーデータを取得
                sensor_data = unit.data

                # 計測時間取得
                # total_time_seconds = unit.elapsed_time.total_seconds()
                elapsed_time =unit.elapsed_time
                
                if elapsed_time in tmp:
                    gait = tmp[elapsed_time]
                    gait._set(sensor_data.data_id[2:], sensor_data.value)
                else:
                    gait = Gait( time=elapsed_time)
                    gait._set(sensor_data.data_id[2:], sensor_data.value)
                    tmp[elapsed_time] = gait
            
            elif unit.data.data_type.value == intdash.DataType.string.value:
                
                try:
                    # センサーデータを取得
                    sensor_data = unit.data
                    # Jsonデシリアライズ
                    # print(sensor_data.value)
                    sensor_data_json = json.loads(sensor_data.value)
                    #side = sensor_data.data_id[0]

                    # 計測時間取得
                    # total_time_seconds = unit.elapsed_time.total_seconds()
                    elapsed_time =unit.elapsed_time

                    for key in self._json_dict:
                        if elapsed_time in tmp:
                            gait = tmp[elapsed_time]
                            gait._set(self._json_dict[key], sensor_data_json[key])
                        else:
                            gait = Gait( time=elapsed_time)
                            gait._set(self._json_dict[key], sensor_data_json[key])
                            tmp[elapsed_time] = gait
                    
                except json.JSONDecodeError:
                    continue
                
        gait_analysis.right = sorted(tmp.values(), key=lambda gait:gait.time)
    
        finish = time.time()
        print(f'Finished: {finish}, {finish - start}', flush=True)

        return AnalyticsValue(
            gait_analysis = gait_analysis
        )

        
    def save(self, measurement_uuid : str, units : List[Unit]):
        analysis_result = []
        for unit in units:
            if not isinstance(unit, Unit):
                print(f"It's not a store unit.")
                continue
            analysis_result.append(unit._raw_data)
                
        print(f"Storing reponse data: Length({len(analysis_result)})", flush=True)        
        self._client.units.store(
            measurement_uuid=measurement_uuid,
            units=analysis_result,
        )

    def realtime(self, callback : Callable[[AnalyticsValue], None], measurement_uuid : str = None, edge_uuid : str = None):
        
        # 端末エッジとアナライザーエッジの取得
        if measurement_uuid != None:
            measurement = self._client.measurements.get(uuid=measurement_uuid)
            if measurement == None:
                print(f"Couldn't find the edge: measurement: {measurement_uuid}")
                return
            edge_uuid = measurement.edge_uuid
        elif edge_uuid != None:
            edge = self._search_edge(edge_uuid)
            if edge == None:
                print(f"Couldn't find the edge: {edge_uuid}")
                return
        else:
            print(f"Specify [measurement_uuid] or both [device_edge_uuid] and [analyzer_edge_uuid].")
            return
        
        device_specs = [
            intdash.DownstreamSpec(
                src_edge_uuid = edge_uuid,
                filters = self._specs_filters,
            )
        ]

        loop = asyncio.get_event_loop()
        wsconn = self._client.connect_websocket()
        try:
            print(f"...Waiting for measurement...")
            wsconn.open_downstreams(
                specs = device_specs,
                callbacks = [self._callback_downstream],
            )
            loop.run_until_complete(self._callback_process(callback))
        finally:
            print(f"...Measurement is closed")
            wsconn.close()
            loop.close()



    # エッジの検索
    def _search_edge(self, edge_uuid):
        i = 1
        found = None
        while True:
            edges = self._client.edges.list(type = "device", page = i)
            for edge in edges:
                if edge.uuid == edge_uuid:
                    found = edge
                if found != None:
                    break

            i = i + 1
            if found != None or i > 100:
                break

        if found == None:
            print("Edge not found:" + edge_uuid)
            return None
        else:
            print("Edge found: " + found.name + " " + found.uuid)
            return found

    # 端末エッジから解析エッジを取得
    def _find_analyzer(self, uuid):
        found = self._search_edge(uuid)
        if found == None:
            return None
        return self._client.edges.list(name = found.name.replace("_device", "_analyzer"))[0]
    
    def _callback_downstream(self, unit) -> None:
        try:
            self._queue.put_nowait(unit)
        except queue.Full:
            pass
        
    @asyncio.coroutine
    def _callback_process(self, callback : Callable[[AnalyticsValue], None]):
        while True:
            try:
                unit : intdash.Unit = self._queue.get_nowait()

                if unit.data.data_type.value == intdash.DataType.basetime.value:
                    yield
                    continue
            
                if unit.data.value == None:
                    yield 
                    continue
                
                # Skip other data.
                if unit.data.data_type.value == intdash.DataType.float.value:

                    id : str = unit.data.data_id
                    value : float = unit.data.value
                    side : str = "l" if id[0] == "L" else "r"
                    elapsed_time : pandas.Timedelta = unit.elapsed_time
                    total_time : int = elapsed_time.total_seconds()
                    
                    if total_time != self._current_time:
                        if self._current_value != None:
                            callback(self._current_value)
                        self._current_time = total_time
                        self._reset_current_value(elapsed_time)

                    if side == "l":
                        self._current_value.gait.left._set(
                            key = id[2:], value = value,
                        )
                    else:
                        self._current_value.gait.right._set(
                            key = id[2:], value = value,
                        )
                
                elif unit.data.data_type.value == intdash.DataType.string.value:
                    
                    try:
                        id : str = unit.data.data_id
                        sensor_data_json = json.loads(unit.data.value)
                        side : str = "l" if id[0] == "L" else "r"
                        elapsed_time : pandas.Timedelta = unit.elapsed_time
                        total_time : int = elapsed_time.total_seconds()

                        for key in self._json_dict:
                            if total_time != self._current_time:
                                if self._current_value != None:
                                    callback(self._current_value)
                                self._current_time = total_time
                                self._reset_current_value(elapsed_time)

                            if side == "l":
                                self._current_value.gait.left._set(
                                    key = self._json_dict[key],
                                    value = sensor_data_json[key],
                                )
                            else:
                                self._current_value.gait.right._set(
                                    key = self._json_dict[key],
                                    value = sensor_data_json[key],
                                )
                        
                    except json.JSONDecodeError:
                        continue
                
                yield
                continue

            except queue.Empty:
                yield
    
    def _reset_current_value(self, elapsed_time : pandas.Timedelta):
        self._current_value = AnalyticsValue(
            gait_analysis = GaitAnalysis()
        )
        self._current_value.gait.left = Gait(elapsed_time)
        self._current_value.gait.right = Gait(elapsed_time)


        




