"""
This is a MODULE docstring
"""
from .export import all_bursts_export, offsets_export
from .burst_class import Bursts, detect_bursts


class BurstMixin():

    def __init__(self):
        self.offset_dict: dict
        self.lookup: dict
        self.from_svo: bool

    def burst_detection(self, s: float = 2, gamma: float = 1):
        """Returns an object of the class `bursts`.

        This method is used to detect bursts for _all_ of the term-term pairs
        in the offset dictionary generated when this class (`edge_burst`) was
        instantiated.

        This method is best employed as an exploratory tool for identifying
        unusually bursty term pairs, or groups of term pairs with correlated
        burst patterns.

        Since calling this method on an entire dataset can consume significant
        amounts of time and memory, this method only allows for one value of
        s and one value of gamma.

        If you wish to detect bursts using a variety of different values for
        the s and gamma parameters, instead utilize the `multi_bursts` method
        contained in this class.

        Args:
            s (float, optional): s parameter for tuning Kleinberg algorithm.
                Higher values make it more difficult for bursts to move up the
                burst hierarchy. Defaults to 2.
            gamma (float, optional): gamma parameter for tuning Kleinberg
                algorithm. Higher values make it more difficult for activity to
                be considered a burst. Defaults to 1.

        Returns:
            Dict: The object's `offset_dict`, with integer keys converted
                to strings.
            Dict: A dictionary with string representations of terms as keys
                and lists of burst data as values.
            float: The s value passed as a parameter.
            float: The gamma value passed as a parameter.
            Bool: A flag passed to other functions in the pipeline to configure
                it for SVO data.
            Dict: A dictionary that maps integer representations of terms
                (as keys) to string representations as values.
        """

        # use offsets_export to return a dictionary with terms as keys in string format and list of time offsets as values
        offset_dict_strings = offsets_export(self.offset_dict, self.lookup,
                                             self.from_svo)

        # use detect_bursts to return a dictionary with terms as keys in integer format and list of nested burst data as values
        edge_burst_dict_int = detect_bursts(self.offset_dict, s, gamma)

        # same as above, but convert keys from integers to the string values they represent
        edge_burst_dict_strings = all_bursts_export(edge_burst_dict_int,
                                                    self.lookup, self.from_svo)

        return offset_dict_strings, edge_burst_dict_strings, s, gamma, self.from_svo, self.lookup

    # def multi_burst(self, token_pairs, s, gamma):
    #     """
    #     The lists passed to s and gamma must be exactly the same length.

    #     Returns a dictionary where keys are strings containing two numbers separated by an underscore, corresponding to the s and gamma values for the run, respectively.
    #     The values of each entry in the dictionary consists of {SOMETHING}
    #     """
    #     assert len(s) == len(gamma)

    #     run_dict = {}
    #     offset_subset_dict = {}

    #     for token_pair in token_pairs:
    #         offset_subset_dict[token_pair] = self.offset_dict[token_pair]

    #     for i in range(0,len(s)):
    #         run_name = "{}_{}".format(str(s[i]), str(gamma[i]))
    #         run_result = Bursts(self.offset_dict,self.lookup, s[i], gamma[i], self.from_svo, self.lookup)
    #         run_dict[run_name] = run_result

    #     return run_dict
