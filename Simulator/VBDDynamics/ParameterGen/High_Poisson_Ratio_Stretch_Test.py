import math

from M01_Parameters import *
from M02_GenRunningParameters import *

import numpy as np
from itertools import product

from os import path

def read_dot_t(filepath):
    verts = []
    with open(filepath, 'r') as f:
        for l in f:
            if "Vertex" in l:
                _, _, x, y, z = l.strip().split()
                x,y,z = float(x), float(y), float(z)
                verts.append([x, y, z])
    return verts

if __name__ == '__main__':
    genFileName = Path(__file__).stem
    repo_root = Path(__file__).parent.parent.parent.parent

    selectedIds = []
    machineName = "manas"
    binaryFile = machines[machineName]["binaryFile"]

    # <CHANGE THIS>
    mesh_file = "Data\\mesh_models\\ModelsDifferentRes\\Cube\\Cube_subdivided.t"
    # mesh_file = "Data\\mesh_models\\ModelsDifferentRes\\Cube\\Cube.t"

    vs = read_dot_t(path.join(repo_root, mesh_file))

    x_coordinates = [vector[0] for vector in vs]

    min_x = min(x_coordinates)
    max_x = max(x_coordinates)

    stiffness = 1000
    # <CHANGE THIS>
    poisson = 0.4995

    fixed = []
    move = []
    speed = 0.1
    endTime = 10
    for i, v in enumerate(vs):
        if v[0] == min_x:
            fixed.append(i)
        elif v[0] == max_x:
            move.append(i)

    models = {
        "Models": [
            {
                "density": 50,
                "dampingGamma": 0.0,
                "hasNoGravZone": False,
                "initialVelocity": [
                    0,
                    0,
                    0
                ],
                "materialName": "NeoHookean",
                "maxVelocityMagnitude": 25,
                "noGravZoneThreshold": 0.0,
                "path": f"${{REPO_ROOT}}\\{mesh_file}",
                "rotation": [
                    0,
                    0,
                    0
                ],
                "scale": [
                    1.0,
                    1.0,
                    1.0
                ],
                "shuffleParallelizationGroup": True,
                "tetsColoringCategoriesPath": f"${{REPO_ROOT}}\\{mesh_file}.tetColoring.json",
                "translation": [
                    2.25,
                    10.0,
                    0.0
                ],
                "translationBeforeScaling": [
                    0.0,
                    0.0,
                    0.0
                ],
                "verticesColoringCategoriesPath": f"${{REPO_ROOT}}\\{mesh_file}.vertexColoring.json",
                "miu": stiffness / 2 / (1 + poisson),
                "lmbd": stiffness * poisson / (1 + poisson) / (1 - 2 * poisson),
                "exponentialVelDamping": 0.9,
                "constantVelDamping": 0.1,
                "frictionDynamic": 0.2,
                "frictionEpsV": 0.01,
                "dampingShear": 1e-07,
                "dampingVolume": 1e-07,
                "frameToAppear": 0,
                "fixedPoints": fixed
            }
        ]
    }

    parameters = {
        "CollisionParams": {
            "allowCCD": True,
            "allowDCD": True,
            "centerShiftLevel": 0.009999999776482582,
            "checkFeasibleRegion": True,
            "checkTetTraverse": True,
            "feasibleRegionEpsilon": 0.009999999776482582,
            "handleSelfCollision": True,
            "loopLessTraverse": False,
            "maxSearchDistanceMultiplier": 1.7999999523162842,
            "rayTriIntersectionEPSILON": 1.000000013351432e-10,
            "restPoseCloestPoint": False,
            "shiftQueryPointToCenter": True,
            "stopTraversingAfterPassingQueryPoint": True,
            "tetrahedralTraverseForNonSelfIntersection": True,
            "useStaticTraverse": True
        },
        "PhysicsParams": {
            "boundaryFrictionDynamic": 0.1,
            "boundaryFrictionStatic": 0.1,
            "bowlCap": False,
            "bowlCenter": [
                0.0,
                0.0,
                0.0
            ],
            "bowlOuterRadius": 1.0499999523162842,
            "bowlRadius": 1.0,
            "ccdBVHRebuildSteps": 7,
            "checkAndUpdateWorldBounds": True,
            "collisionDetectionSubSteps": 1,
            "constantVelDamping": -1.0,
            "dcdSurfaceSceneBVHRebuildSteps": 3,
            "dcdTetMeshSceneBVHRebuildSteps": 16,
            "debug": True,
            "debugVerboseLvl": 1,
            "doCollDetectionOnlyForFirstIteration": True,
            "doStatistics": False,
            "gravity": [
                0.0,
                0.0,
                0.0
            ],
            "iterations": 20,
            "numFrames": 3000,
            "numSubsteps": 20,
            "outputExt": "ply",
            "outputIntermediateState": False,
            "outputRecoveryState": True,
            "outputRecoveryStateStep": 10,
            "outputStatistics": False,
            "outputStatisticsStep": 10,
            "outputT": False,
            "outputVTK": False,
            "perMeshParallelization": True,
            "perTetParallelization": False,
            "saveAllModelsTogether": True,
            "saveSimulationParameters": True,
            "shaderFolderPath": "",
            "showSubstepProgress": False,
            "showTimeConsumption": False,
            "smoothSurfaceNormal": True,
            "stepInvariantVelDamping": False,
            "timeStep": 0.01666666,
            "useBowlGround": False,
            "usePlaneGround": True,
            "worldBounds": [
                [
                    0,
                    0.0,
                    0
                ],
                [
                    0,
                    20.0,
                    0
                ]
            ],
            "useGPU": True,
            "useAccelerator": True,
            "collisionStiffness": 100000.0,
            "collisionSolutionType": 1
        },
        "Deformers": [
            {
                "DeformerName": "Translator",
                "speed": [
                    speed,
                    0,
                    0,
                ],
                "selectedMeshes": [
                    0
                ],
                "deformationEndTime": endTime,
                "selectedVertices": [
                    move
                ]
            }
        ],
        "ViewerParams": {
            "enableViewer": True
        }
    }
    cmd = genRunningParameters2(machineName, genFileName, ".", models, parameters, exeName=binaryFile,
                                runCommand=False)
    # cmd = genRunningParameters2(machineName, genFileName, experimentName, modelsInfo, parameters, exeName=binaryFile, runCommand=run, recoverState=recoveryState)