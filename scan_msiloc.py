import pandas as pd
import os
import argparse as apa


def scan_loc(msisensor, reference, bed, out):
    os.system("{0} scan -d {1} -l 10 -o MSI_loc.txt".format(msisensor, reference))
    data = pd.read_table("MSI_loc.txt")
    data["location"] += 1
    data["location1"] = [i + ii * iii - 1 for i, ii, iii in zip(data["location"], data["repeat_unit_length"], data["repeat_times"])]
    data["MSID"] = ["MS" + str(i) for i in range(1, data.shape[0] + 1)]
    data = data[["chromosome", "location", "location1", "repeat_unit_bases", "repeat_times", "MSID"]]
    data.columns = ["chr", "start", "end", "MS", "repeat", "MSID"]
    data.to_csv("all_msi_loc.bed", sep="\t", index=False, header=None)
    os.system("bedtools intersect -a all_msi_loc.bed -b {0} > all_msi_loc1.bed".format(bed))
    data = pd.read_table("all_msi_loc1.bed", names=["chr", "start", "end", "MS", "repeat", "MSID"])
    data = data.loc[data["repeat"] > 3]
    data.to_csv(out, sep="\t", index=False)


def main():
    parser = apa.ArgumentParser(prog="convert")
    parser.add_argument('-msisensor', '--msisensor', required=True, type=str, help='the path of msisensor')
    parser.add_argument("-ref", "--reference", required=True, type=str, help="the path of reference genome, such as hg19")
    parser.add_argument("-bed", "--bed", type=str, required=True, help="your panel bed")
    parser.add_argument("-o", "--out", required=False, default="msi_loc.bed.txt", help="output file")
    args = parser.parse_args()
    scan_loc(args.msisensor, args.reference, args.bed, args.out)


main()