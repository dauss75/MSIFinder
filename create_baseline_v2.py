import pandas as pd
from numpy import std, array, mean, median
import os
import argparse as apa
from collections import defaultdict


def plot(pex, result):
    result = result.loc[result["qcs"] == "pass"]
    fig, axs = plt.subplots(nrows=len(result), ncols=1, figsize=(3 * len(result), 12))
    for i, info in enumerate(result["IndelLength:AlleleFraction:SupportingCalls"]):
        ax = axs[i]
        x = []
        for peak in info.split(" "):
            x += [int(peak.split(":")[0])] * int(peak.split(":")[2])
        sns.kdeplot(x, bw=.5, ax=ax)
    plt.savefig(pex + "MSI.pdf")


def _make_control(files, loc):
    info1 = defaultdict(list)
    info2 = defaultdict(list)
    for file in files:
        data = pd.read_table(file)
        mss = data["MSID"]
        # data = data.loc[data["qcs"] == "pass"]
        for name, qc, peak, reads in zip(data["MSID"], data["qcs"], data["Number_of_Peaks"], data["Total_Reads"]):
            if loc == "all":
                if qc == "pass":
                    info1[name].append(peak)
                    info2[name].append(reads)
            else:
                if name == loc:
                    info1[name].append(peak)
                    info2[name].append(reads)

    result = {"MSID": [], "qcs": [], "Standard_Deviation": [], "Average_Number_Peaks": [],
              "Average_Total_Reads": [], "Count": []}
    for position_name, peak_list in info1.items():
        result["MSID"].append(position_name)
        result["Standard_Deviation"].append(std(array(peak_list)))
        result["Average_Number_Peaks"].append(mean(array(peak_list)))
        result["Average_Total_Reads"].append(mean(array(info2[position_name])))
        if median(array(info2[position_name])) >= 30:
            result["qcs"].append("pass")
        else:
            result["qcs"].append("fail")
        result["Count"].append(len(peak_list))
    data = pd.DataFrame(result)
    data = data[["MSID", "qcs", "Standard_Deviation", "Average_Number_Peaks", "Average_Total_Reads", "Count"]]
    return data, mss


def make_control(args):
    files = args.dir
    outfile = args.outfile
    loc = "all"
    data, mss = _make_control(files, loc)
    for ms in mss.tolist():
        if ms not in data["MSID"].tolist():
            _data, _ = _make_control(files, ms)
            data = pd.concat([data, _data])
    data.to_csv(outfile, sep="\t", index=False)


if __name__ == "__main__":
    usage = "\n\tmake MSI control file"
    parser = apa.ArgumentParser(prog="convert")
    parser.add_argument("-d", "--dir", required=True, nargs='*',
                        help="the dir of containing MSIdetect_v2.py stat result file,(such as your_path/*_MSIscore.xls)")
    parser.add_argument('-o', '--outfile', required=False, default="MSI_BASELINE_v2.txt",
                        help='output file name, default is MSI_BASELINE_v2.txt')
    args = parser.parse_args()
    make_control(args)