
class Segment():
    '''
    Distill's segmentation package. Allows the user to segment User Ale log data.
    '''

    def __init__(self, segment_name, start_end_val, num_logs):
        self.segment_name = segment_name
        self.start_end_val = start_end_val
        self.num_logs = num_logs

    @staticmethod
    def create_segment(target_dict, segment_names, start_end_vals):
        '''
        Creates a dictionary of Segment objects representing the metadata
        associated with each defined segment.

        target_dict: a dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects)
        segment_names: a list of segment_names ordered in the same way as the start_end_vals
        start_end_vals: a list of tuples (i.e [(start_time, end_time)], where start_time and end_time are Date/Time Objects

        Returns a dictionary of segment_name to Segment objects
        '''

        result = {}
        for i in range(len(segment_names)):
            num_logs = 0
            segment_name = segment_names[i]
            start_time = start_end_vals[i][0]
            end_time = start_end_vals[i][1]
            for uid in target_dict:
                log = target_dict[uid]
                if log['clientTime'] >= start_time and log['clientTime'] <= end_time:
                    # Perform data collection on log
                    num_logs += 1
            segment = Segment(segment_name, start_end_vals[i], num_logs)
            result[segment_name] = segment
        return result
        