
class Segment():
    """
    Distill's segmentation package. Allows the user to segment User Ale log data.
    """

    def __init__(self, segment_name, start_end_val, num_logs, uids):
        self.segment_name = segment_name
        self.start_end_val = start_end_val
        self.num_logs = num_logs
        self.uids = uids

    @staticmethod
    def create_segment(target_dict, segment_names, start_end_vals):
        """
        Creates a dictionary of Segment objects representing the metadata
        associated with each defined segment.

        Parameters:
            target_dict ({}): a dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects)
            segment_names ([strings]): a list of segment_names ordered in the same way as the start_end_vals
            start_end_vals ([(Date/Time, Date/Time)]): a list of tuples (i.e [(start_time, end_time)], where start_time and end_time are Date/Time Objects

        Returns:
            A dictionary of segment_name to Segment objects
        """

        result = {}
        for i in range(len(segment_names)):
            num_logs = 0
            segment_name = segment_names[i]
            start_time = start_end_vals[i][0]
            end_time = start_end_vals[i][1]
            uids = []
            for uid in target_dict:
                log = target_dict[uid]
                if log['clientTime'] >= start_time and log['clientTime'] <= end_time:
                    # Perform data collection on log
                    num_logs += 1
                    uids.append(uid)
            segment = Segment(segment_name, start_end_vals[i], num_logs, uids)
            result[segment_name] = segment
        return result

    @staticmethod
    def write_segment(target_dict, segment_names, start_end_vals):
        """
        Creates a nested dictionary of segment names to UIDs which then map to individual
        logs (i.e result['segment_name'][uid] --> log).  This assists with easy iteration over
        defined segments.

            Parameters:
                target_dict ({}): a dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects).
                segment_names ([strings]): a list of segment_names ordered in the same way as the start_end_vals.
                start_end_vals ([(Date/Time, Date/Time)]): A list of tuples (i.e [(start_time, end_time)]), where start_time and end_time are Date/Time Objects.
            
            Returns:
                A nested dictionary of segment_names to uids to individual logs.
        """
        result = {}
        create_result = Segment.create_segment(target_dict, segment_names, start_end_vals)

        # Iterate through segments to get logs
        for segment_name in create_result:
            result[segment_name] = {}
            for uid in create_result[segment_name].uids:
                result[segment_name][uid] = target_dict[uid]

        return result
        