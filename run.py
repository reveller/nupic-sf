#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Prediction Tutorial.)
"""
import importlib
import sys
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

import nupic_output


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
GYM_NAME = "rec-center-hourly_out"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
# '7/2/10 0:00'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_METRIC_SPECS = (
    MetricSpec(field='traffic', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='traffic', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='traffic', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
    MetricSpec(field='traffic', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
)

def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "traffic"})
  return model



def getModelParamsFromName(gymName):
  import ipdb; ipdb.set_trace() # BREAKPOINT
  importName = "model_params.%s_model_params" % (
    gymName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % gymName)
  return importedModelParams



def runIoThroughNupic(inputData, model, gymName, plot):
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_output.NuPICPlotOutput([gymName])
  else:
    output = nupic_output.NuPICFileOutput([gymName])

  metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
                                  model.getInferenceType())

  for each in xrange(60):
    print("Training...{0}".format(each))
    # reset the file to position zero again
    inputFile.seek(0)
    csvReader.next()  # skip the header rows
    csvReader.next()
    csvReader.next()

    for row in csvReader:
      timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
      consumption = float(row[1])
      result = model.run({
        "timestamp": timestamp,
        "traffic": consumption
      })

  # reset the file to position zero again
  inputFile.seek(0)
  csvReader.next()  # skip the header rows
  csvReader.next()
  csvReader.next()

  counter = 0
  for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    consumption = float(row[1])
    result = model.run({
      "timestamp": timestamp,
      "traffic": consumption
    })
    result.metrics = metricsManager.update(result)

    if counter % 100 == 0:
      print("Read {0} lines...".format(counter))
      print("After {0} records, 1-step altMAPE={1}", counter,
              result.metrics["multiStepBestPredictions:multiStep:"
                             "errorMetric='altMAPE':steps=1:window=1000:"
                             "field=traffic"])
 
    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    output.write([timestamp], [consumption], [prediction])

  inputFile.close()
  output.close()



def runModel(gymName, plot=False):
  print "Creating model from %s..." % gymName
  model = createModel(getModelParamsFromName(gymName))
  inputData = "%s/%s.csv" % (DATA_DIR, gymName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, gymName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(GYM_NAME, plot=plot)
