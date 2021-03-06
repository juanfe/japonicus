#!/bin/python

from deap import tools
import numpy as np

epochStatisticsNames = {
    'avg': 'Average profit',
    'std': 'Profit variation',
    'min': 'Minimum profit',
    'max': 'Maximum profit',
    'size': 'Population size',
    'maxsize': 'Max population size',
    'avgTrades': 'Avg trade number',
    'sharpe': 'Avg sharpe ratio',
    'avgExposure': "Avg exposure time",
    'nbElderDies': 'Elder dies count'
}

periodicStatisticsNames = {
    'evaluationScore': "Evaluation Score",
    'evaluationScoreOnSecondary': "Score on Secondary Dataset"
}



def compileStats(locale):
    # --get proper evolution statistics;
    Stats = locale.stats.compile(locale.population)
    Stats['dateRange'] = ' '.join([DR.textDaterange()
                                   for DR in locale.Dataset])\
                                       if not locale.EPOCH else None
    Stats['maxsize'] = locale.POP_SIZE
    Stats['size'] = len(locale.population)
    Stats['avgTrades'] = locale.extraStats['avgTrades']
    Stats['avgExposure'] = locale.extraStats['avgExposure'] 
    #Stats['nbElderDies'] = locale.extraStats['nbElderDies']
    Stats['sharpe'] = np.mean([x.fitness.values[1] for x in locale.population])
    Stats['evaluationScoreOnSecondary'] = locale.lastEvaluationOnSecondary
    Stats['evaluationScore'] = locale.lastEvaluation
    locale.lastEvaluationOnSecondary = None
    locale.lastEvaluation = None
    Stats['id'] = locale.EPOCH
    locale.EvolutionStatistics.append(Stats)
    locale.World.logger.write_evolution_logs(
        locale.EPOCH, locale.EvolutionStatistics, locale.name
    )


def showStatistics(locale):
    # show information;
    Stats = locale.EvolutionStatistics[locale.EPOCH]
    print("EPOCH %i\t&%i" % (locale.EPOCH, locale.extraStats['nb_evaluated']))
    statnames = ['max', 'avg', 'min',
                 'std', 'size', 'maxsize',
                 'avgTrades', 'sharpe', 'avgExposure',
                 # 'nbElderDies'
    ]
    statisticsText = []
    for s in range(len(statnames)):
        SNAME = statnames[s]
        SVAL = Stats[SNAME]
        currentStatisticsText = "%s" % epochStatisticsNames[SNAME]
        if not SVAL % 1:
            currentStatisticsText += " %i" % SVAL
        else:
            currentStatisticsText += " %.3f" % SVAL
        statisticsText.append(currentStatisticsText)

    columnWidth = max([len(STXT) for STXT in statisticsText]) + 3
    for j in range(0, len(statisticsText), 2):
        print(''.join(word.ljust(columnWidth) for word in statisticsText[j:j+2]))

    print()
