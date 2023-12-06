#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# parte1.py
# Descripción: resolver parte1 
# -----------------------------------------------------------------------------
import constraint



def aparcados_mal(*args):
    for i in range(len(args)) :
        if args[i] == 'TSU-C' or args[i] == 'TSU-X':
            for j in range(i+1, len(args)):
                if i != j and args[i] != args[j]:
                    return False
    return True


# main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    problem = constraint.Problem()

    plazas_variables = [
        ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6'],
        ['2.1', '2.2', '2.3', '2.4', '2.5', '2.6'],
        ['3.1', '3.2', '3.3', '3.4', '3.5', '3.6'],
        ['4.1', '4.2', '4.3', '4.4', '4.5', '4.6'],
        ['5.1', '5.2', '5.3', '5.4', '5.5', '5.6']
    ]

    plazas_electricas = ['1.1','1.2','2.1','4.1','5.1','5.2']

    for sublist in plazas_variables:
        for item in sublist:
            if item not in plazas_electricas:
                problem.addVariable(item, ['vacia','TSU-X', 'TNU-X'])
            else:
                problem.addVariable(item, ['vacia','TSU-X', 'TNU-X', 'TSU-C', 'TNU-C'])


    # constraints
    # -------------------------------------------------------------------------
   

    problem.addConstraint(aparcados_mal,('1.1','1.2','1.3','1.4','1.5','1.6'))
    problem.addConstraint(aparcados_mal,('2.1','2.2','2.3','2.4','2.5','2.6'))
    problem.addConstraint(aparcados_mal,('3.1','3.2','3.3','3.4','3.5','3.6'))
    problem.addConstraint(aparcados_mal,('4.1','4.2','4.3','4.4','4.5','4.6'))
    problem.addConstraint(aparcados_mal,('5.1','5.2','5.3','5.4','5.5','5.6'))

    solution = problem.getSolution()

    print("Solución encontrada:")
    print(solution)
    
    