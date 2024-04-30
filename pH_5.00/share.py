#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def loadxvg(fname: str, col: list = [0, 1], dt: int = 1, b: int = 0):
    """Loads an .xvg file into a list of lists.
    May also be used to load float columns from files in general.

    Args:
        fname (str): file name.
        col (list, optional): columns to load. Defaults to [0, 1].
        dt (int, optional): step size. Defaults to 1.
        b (int, optional): starting point. Defaults to 0.

    Returns:
        list of lists : contains the columns that were loaded.
    """

    count = -1
    data = [[] for _ in range(len(col))]
    for stringLine in open(fname).read().splitlines():
        if stringLine[0] in ["@", "#", "&"]:
            continue
        # THIS IS FOR THE dt PART.
        count += 1
        if count % dt != 0:
            continue

        listLine = stringLine.split()
        # AND THIS IS FOR THE b PART.
        if b != 0 and float(listLine[col[0]]) < b:
            continue

        for idx in col:
            data[idx].append(float(listLine[col[idx]]))
    return data


def protonation(xList: list, cutoff: float = 0.8) -> float:
    """Returns the average protonation, i.e. the fraction of frames in which
    the lambda-coordinate is < 1 - cutoff.

    Args:
        xList (list): coordinate list.
        cutoff (float, optional): Defaults to 0.8.

    Returns:
        float: the average protonation.
    """

    lambda_proto = 0
    lambda_deproto = 0

    for x in xList:

        if x > cutoff:
            lambda_deproto += 1

        if x < 1 - cutoff:
            lambda_proto += 1

    if lambda_proto + lambda_deproto == 0:
        fraction = 0
    else:
        fraction = float(lambda_proto) / (lambda_proto + lambda_deproto)

    print(lambda_proto)
    print(lambda_deproto)
    return fraction


def localpKa(pH: float, protonation: float) -> float:
    """Compute the local pKa from the simulation pH and protonation fraction
    using the Henderson-Hasselbalch equation.

    Args:
        pH (float): (solvent) pH.
        protonation (float): protonation fraction.

    Returns:
        float: local/shifted pKa.
    """

    return pH - np.log10(1 / protonation - 1)


if __name__ == "__main__":

    pH = 5.0
    resNames = {37: "HSPT", 44: "ASPT"}
    lambdaCoordNumbers = {37: [1, 5, 9, 13], 44: [4, 8, 12, 16]}

    for resid in [37, 44]:

        xtotal = []
        for num in lambdaCoordNumbers[resid]:

            data = loadxvg(f"./cphmd-coord-{num}.xvg")
            t = [val / 1000.0 for val in data[0]]  # ps to ns.
            x = data[1]

            plt.plot(t, x, label=f"{resNames[resid]} coord-{num}", linewidth=0.5)

            # The interpretation of the (first) HIS coordinate is reversed.
            if resid == 37:
                x = [1 - val for val in x]

            xtotal += x

        protoFrac = protonation(xtotal)
        pKa = localpKa(pH=pH, protonation=protoFrac)

        print(f"{resNames[resid]} mean protofraction of {protoFrac:.4f} at pH {pH} corresponds to a local pKa of {pKa:.4f}")

        plt.title(f"Trajectories for {resNames[resid]}-{resid}")
        plt.xlabel("Time (ns)")
        plt.ylabel("$\lambda$-coordinate")
        plt.legend()
        plt.savefig(f"{resNames[resid]}.png")
        plt.clf()
