# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.use('agg')
from matplotlib.testing.compare import compare_images
from tempfile import NamedTemporaryFile
import os.path
import pygenometracks.plotTracks


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "test_data")

browser_tracks = """
[macs2 broadPeak]
file = broadPeak.broadPeak
title = broadPeak
file_type = bed

[spacer]

[macs2 gappedPeak]
file = gappedPeak.gappedPeak
title = gappedPeak
file_type = bed

[spacer]

[macs2 filteredbed]
file = filtered.results.bed
title = filtered.results.bed (strange format)
file_type = bed
"""
with open(os.path.join(ROOT, "bed_unusual_formats.ini"), 'w') as fh:
    fh.write(browser_tracks)

browser_tracks = """
[strange_strand]
file = strange_strand.bed
"""
with open(os.path.join(ROOT, "strange_strand.ini"), 'w') as fh:
    fh.write(browser_tracks)


browser_tracks = """
[invalid_strand]
file = invalid_strand.bed
"""
with open(os.path.join(ROOT, "invalid_strand.ini"), 'w') as fh:
    fh.write(browser_tracks)

browser_tracks = """
[invalid_rgb]
file = invalid_rgb.bed
title = first line valid but neg invalid
color = bed_rgb

[invalid_rgb2]
file = invalid_rgb2.bed
title = first line invalid
color = bed_rgb
"""
with open(os.path.join(ROOT, "invalid_rgb.ini"), 'w') as fh:
    fh.write(browser_tracks)

browser_tracks = """
[invalid_blockCount]
file = invalid_blockCount.bed
title = invalid block count in first line
color = bed_rgb

[spacer]

[invalid_blockCount]
file = invalid_blockCount2.bed
title = invalid block count in not first line -> bedtools raised an error
style = UCSC
height = 2
"""
with open(os.path.join(ROOT, "invalid_blockCount.ini"), 'w') as fh:
    fh.write(browser_tracks)

tolerance = 13  # default matplotlib pixed difference tolerance


def test_plot_tracks_bed_unusual_format():

    outfile = NamedTemporaryFile(suffix='.png', prefix='pyGenomeTracks_test_',
                                 delete=False)
    ini_file = os.path.join(ROOT, "bed_unusual_formats.ini")
    region = "X:20000-40000"
    expected_file = os.path.join(ROOT, 'master_bed_unusual_formats.png')
    args = f"--tracks {ini_file} --region {region} "\
           "--trackLabelFraction 0.2 --width 38 --dpi 130 "\
           f"--outFileName {outfile.name}".split()
    pygenometracks.plotTracks.main(args)
    res = compare_images(expected_file,
                         outfile.name, tolerance)
    assert res is None, res

    os.remove(outfile.name)


def test_plot_tracks_bed_strange_strand():

    outfile = NamedTemporaryFile(suffix='.png', prefix='pyGenomeTracks_test_',
                                 delete=False)
    ini_file = os.path.join(ROOT, "strange_strand.ini")
    region = "chr1:0-500"
    expected_file = os.path.join(ROOT, 'master_strange_strand.png')
    args = f"--tracks {ini_file} --region {region} "\
           "--trackLabelFraction 0.2 --width 38 --dpi 130 "\
           f"--outFileName {outfile.name}".split()
    pygenometracks.plotTracks.main(args)
    res = compare_images(expected_file,
                         outfile.name, tolerance)
    assert res is None, res

    os.remove(outfile.name)


def test_plot_tracks_bed_invalid_strand():

    tolerance = 5

    outfile = NamedTemporaryFile(suffix='.png', prefix='pyGenomeTracks_test_',
                                 delete=False)
    ini_file = os.path.join(ROOT, "invalid_strand.ini")
    region = "chr1:0-500"
    expected_file = os.path.join(ROOT, 'master_strange_strand.png')
    args = f"--tracks {ini_file} --region {region} "\
           "--trackLabelFraction 0.2 --width 38 --dpi 130 "\
           f"--outFileName {outfile.name}".split()
    pygenometracks.plotTracks.main(args)
    res = compare_images(expected_file,
                         outfile.name, tolerance)
    assert res is None, res

    os.remove(outfile.name)
    os.remove(ini_file)


# For the moment this is failing but it should not
# def test_plot_tracks_bed_invalid_blockCount():

#     outfile = NamedTemporaryFile(suffix='.png', prefix='pyGenomeTracks_test_',
#                                  delete=False)
#     ini_file = os.path.join(ROOT, "invalid_blockCount.ini")
#     region = "chrX:15000-24000"
#     expected_file = os.path.join(ROOT, 'master_invalid_blockCount.png')
#     args = f"--tracks {ini_file} --region {region} "\
#            "--trackLabelFraction 0.2 --width 38 --dpi 130 "\
#            f"--outFileName {outfile.name}".split()
#     pygenometracks.plotTracks.main(args)
#     res = compare_images(expected_file,
#                          outfile.name, tolerance)
#     assert res is None, res

#     os.remove(outfile.name)

# def test_plot_tracks_bed_invalid_rgb():

#     outfile = NamedTemporaryFile(suffix='.png', prefix='pyGenomeTracks_test_',
#                                  delete=False)
#     ini_file = os.path.join(ROOT, "invalid_rgb.ini")
#     region = "chr1:0-500"
#     expected_file = os.path.join(ROOT, 'master_invalid_rgb.png')
#     args = f"--tracks {ini_file} --region {region} "\
#            "--trackLabelFraction 0.2 --width 38 --dpi 130 "\
#            f"--outFileName {outfile.name}".split()
#     pygenometracks.plotTracks.main(args)
#     res = compare_images(expected_file,
#                          outfile.name, tolerance)
#     assert res is None, res

#     os.remove(outfile.name)
