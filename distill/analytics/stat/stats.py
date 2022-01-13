#
# Copyright 2022 The Applied Research Laboratory for Intelligence and Security (ARLIS)
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Session Click-Rate
def session_clickrate_dict(data, session):
    """
    Creates clickrate dictionary from user defined dataframe and session
    :param data: Dataframe of logs imported from JSON (SampleLogs2Session)
    :param session: String of session ID of interest
    :return: A session clickrate dictionary
    """

    # turn clientTime into indexable data-time object
    new_dateTime = pd.to_datetime(df['clientTime'], unit='ms', origin='unix')
    df['client_dateTime'] = (new_dateTime - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
    df.set_index('client_dateTime', inplace=True)
    df.sort_values('client_dateTime')
    print('data indexed by time')

    if session != False:
        # filter data by session
        session_segment = (df.groupby(df['sessionID'])).get_group(session)
        print('data filtered')

    # segmentation
    # build filter mask
    # filter rows Events Of Interest (eoi)
    # create list of tuplesthat bound start/stop of each segment
    eoi = ['XMLHttpRequest.open', 'XMLHttpRequest.response']
    segment_events = session_segment.loc[session_segment['type'].isin(eoi)]
    segment_events = segment_events.sort_values('client_dateTime').index
    segment_start_stop = pairwiseStag(segment_events)
    print('segments defined')

    cr_dict = {}
    for i in segment_start_stop:
        segnum = 'Segment' + str(segment_start_stop.index(i) + 1)
        cr_dict[segnum] = {}
        cr_dict[segnum]['Segment'] = str(segnum)
        cr_dict[segnum]['Start_stop'] = i
        cr_dict[segnum]['Duration_ms'] = i[1] - i[0]
        dur_sec = ((i[1] - i[0]) / 1000)
        cr_dict[segnum]['Duration_s'] = dur_sec

        tempdf = session_segment.reset_index()
        segmentClicks = len(tempdf.query('clientTime >= @i[0] & clientTime <= @i[1] & type == "click"').index)
        cr_dict[segnum]['Clicks_c'] = segmentClicks
        cr_dict[segnum]['Clickrate_cs'] = round(segmentClicks / dur_sec, 3)

    return cr_dict
