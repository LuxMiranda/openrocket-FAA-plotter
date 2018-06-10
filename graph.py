import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import math
import csv

def main():
    thrustAndPropMassVsTime()
    CnaCPandDragVsMach()
    CpCGandMassVsMach()
    CGandMassVsTimeAtBU()


def CGandMassVsTimeAtBU():
    title       = 'CG and Mass vs. Time at BU'
    xName       = 'Time (seconds)'
    yNames      = ['CG (centimeters)', 'Mass (grams)']
    csvFileName = 'sustainer.csv'
    yAxes       = [ 24, 19 ]
    xAxis       = 0
    xData,yData = readFile(csvFileName, xAxis, yAxes)
    maxX        = 25
    plot(title,xName,yNames,maxX,xData,yData)


def CpCGandMassVsMach():
    title       = 'CP, CG, and Mass vs. Mach'
    xName       = 'Mach Number'
    yNames      = ['CP (centimeters)', 'CG (centimeters)', 'Mass (grams)']
    csvFileName = 'sustainer.csv'
    yAxes       = [ 23, 24, 19 ]
    xAxis       = 26
    xData,yData = readFile(csvFileName, xAxis, yAxes)
    maxX        = max(xData)
    plot(title,xName,yNames,maxX,xData,yData)


def CnaCPandDragVsMach():
    title       = 'Cna, CP, and Drag vs. Mach'
    xName       = 'Mach Number'
    yNames      = ['Cna', 'CP (centimeters)', 'Drag force (Newtons)']
    csvFileName = 'sustainer.csv'
    yAxes       = [ 35, 23, 29 ]
    xAxis       = 26
    xData,yData = readFile(csvFileName, xAxis, yAxes)
    maxX        = max(xData)
    plot(title,xName,yNames,maxX,xData,yData)


def thrustAndPropMassVsTime():
    title       = 'Thrust and Propellent Mass vs. Time'
    xName       = 'Time (seconds)'
    yNames      = ['Thrust (Newtons)', 'Propellant mass (grams)']
    csvFileName = 'sustainer.csv'
    yAxes       = [ 28, 20 ]
    xAxis       = 0
    xData,yData = readFile(csvFileName, xAxis, yAxes)

    # Determine when propellent mass reaches 0 to cut the plot off
    maxX = 0
    for i in range(0, len(yData[1])):
        if yData[1][i] < 1:
            maxX = math.ceil(xData[i]) + 1
            break

    plot(title,xName,yNames,maxX,xData,yData)


def readFile(csvFileName, xAxis, yAxes):
    yData = []
    xData = []

    for x in yAxes:
        yData.append([])

    csvFile = open(csvFileName, 'r')
    reader  = csv.reader(csvFile)
    for i, row in enumerate(reader):
        for j, col in enumerate(row):
            if j == xAxis:
                xData.append(float(col))

            for y in range(0, len(yAxes)):
                if j == yAxes[y]:
                    yData[y].append(float(col))

    csvFile.close()
    return xData, yData


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def plot(title,xName,yNames,maxX,xData,yData):
    third = False
    if  len(yData) == 3:
        third = True

    fig, host = plt.subplots()
    if third:
        fig.subplots_adjust(right=0.75)

    par1 = host.twinx()

    par2 = []

    if third:
        par2 = host.twinx()
        # Offset the right spine of par2.  The ticks and label have already been
        # placed on the right by twinx above.
        par2.spines["right"].set_position(("axes", 1.2))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(par2)
        # Second, show the right spine.
        par2.spines["right"].set_visible(True)

    p1, = host.plot(xData, yData[0], "b-", label=yNames[0], lw=0.5)
    p2, = par1.plot(xData, yData[1], "r-", label=yNames[1], lw=0.5)
    p3 = []
    if third:
        p3, = par2.plot(xData, yData[2], "g-", label=yNames[2], lw=0.5)

    host.set_xlabel(xName)
    host.set_ylabel(yNames[0])
    par1.set_ylabel(yNames[1])
    if third:
        par2.set_ylabel(yNames[2])

    host.set_xlim(0,maxX)

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    if third:
        par2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    if third:
        par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2]
    if third:
        lines.append(p3)

    host.legend(lines, [l.get_label() for l in lines])

    minor_locator = AutoMinorLocator(5)
    host.xaxis.set_minor_locator(minor_locator)
    plt.grid(which='minor')
    host.grid(True)
    host.grid(b=True,which='minor')

    plt.title(title)
    if not third:
        plt.subplots_adjust(right=0.85)
    plt.savefig('plots/' + (title.replace(' ','').replace('.','')) + '.pdf')
    #plt.show()


if __name__ == '__main__':
    main()
