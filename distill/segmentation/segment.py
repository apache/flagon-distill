
class Segment():
    """
    Distill's segmentation package. Allows the user to segment User Ale log data.
    """

    def __init__(self, segment_name, start_end_val, num_logs, uids):
        """
        Initializes a Segment object.  This object contains metadata for the associated Segment.

        Parameters:
            segment_name (string): Name associated with the segment
            start_end_val ([(Date/Time, Date/Time)]): A list of tuples (i.e [(start_time, end_time)], where start_time and end_time are Date/Time Objects
            num_logs (int): Number of logs in the segment
            uids ([strings]): A list of strings representing the associated uids of logs within the segment
        """

        self.segment_name = segment_name
        self.start_end_val = start_end_val
        self.num_logs = num_logs
        self.uids = uids

    def get_segment_name(self):
        return self.segment_name
        
    def get_start_end_val(self):
        return self.start_end_val

    def get_num_logs(self):
        return self.num_logs
    
    def get_segment_uids(self):
        return self.uids

    @staticmethod
    def union(segment_name, segment1, segment2):
        """
        Creates a new segment based on the union of given segments' uids.

        Parameters:
            segment_name (string): Name associated with the new segment
            segment1 (Segment): First segment involved in union.
            segment2 (Segment): Second segment involved in union.

        Returns:
            A new segment with the given segment_name, start and end values based on the smallest client time and largest client time of the given segments,
            and a list of the union of the uids of segment1 and segment2. 
        """

        # Union uids
        uids = segment1.uids
        for uid in segment2.uids:
            if uid not in uids:
                uids.append(uid)
        
        # Get earliest starting val and latest end val
        start_time = segment1.start_end_val[0]
        end_time = segment1.start_end_val[1]
        if segment1.start_end_val[0] > segment2.start_end_val[0]:
            start_time = segment2.start_end_val[0]
        if segment1.start_end_val[1] < segment2.start_end_val[1]:
            end_time = segment2.start_end_val[1]

        # Create segment to return
        segment = Segment(segment_name, (start_time, end_time), len(uids), uids)
        return segment
    
    @staticmethod
    def create_segment(target_dict, segment_names, start_end_vals):
        """
        Creates a dictionary of Segment objects representing the metadata
        associated with each defined segment.

        Parameters:
            target_dict ({}): A dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects)
            segment_names ([strings]): A list of segment_names ordered in the same way as the start_end_vals
            start_end_vals ([(Date/Time, Date/Time)]): A list of tuples (i.e [(start_time, end_time)], where start_time and end_time are Date/Time Objects

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
                target_dict ({}): A dictionary of User Ale logs assumed to be ordered by clientTime (Date/Time Objects).
                segment_names ([strings]): A list of segment_names ordered in the same way as the start_end_vals.
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
