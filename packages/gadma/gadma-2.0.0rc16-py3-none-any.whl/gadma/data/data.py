from ..utils import check_file_existence, ensure_file_existence


class DataHolder(object):
    """
    Class for data holding.

    : param filename: name of file with data
    : param outgroup: information if there is outgroup in data
    : type outgroup: bool
    : params pop_labels: labels of populations in data
    : param seq_len: length of sequence that was used to build data
    """
    def __init__(self, filename, projections,
                 outgroup, population_labels, sequence_length):
        self.data = None
        self.filename = filename
        self.projections = projections
        self.outgroup = outgroup
        self.population_labels = population_labels
        self.sequence_length = sequence_length

        if self.filename is not None and check_file_existence(self.filename):
            self.filename = ensure_file_existence(self.filename)


class SFSDataHolder(DataHolder):
    """
    Class for SFS data holding.
    if any parameter is None then it will be taken from the file
    """
    def __init__(self, sfs_file, projections=None, outgroup=None,
                 population_labels=None, sequence_length=None):
        super(SFSDataHolder, self).__init__(
            filename=sfs_file,
            projections=projections,
            outgroup=outgroup,
            population_labels=population_labels,
            sequence_length=sequence_length
        )


class VCFDataHolder(DataHolder):
    """
    Class for VCF data holding.
    """
    def __init__(self, vcf_file, popmap_file, projections=None, outgroup=None,
                 population_labels=None, sequence_length=None,  bed_file=None):
        super(VCFDataHolder, self).__init__(
            filename=vcf_file,
            projections=projections,
            outgroup=outgroup,
            population_labels=population_labels,
            sequence_length=sequence_length
        )
        self.popmap_file = popmap_file
        self.bed_file = bed_file
