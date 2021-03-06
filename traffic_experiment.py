#!/usr/bin/python

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
import csv
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic_output import NuPICFileOutput, NuPICPlotOutput
from nupic.swarming import permutations_runner

#import generate_data

# Change this to switch from a matplotlib plot to file output.
PLOT = False
SWARM_DEF = "search_def.json"
SWARM_CONFIG = {
  "includedFields": [
    {
      "fieldName": "traffic",
      "fieldType": "float",
      "maxValue": 1000.0,
      "minValue": 0.0
    }
  ],
  "streamDef": {
    "info": "traffic",
    "version": 1,
    "streams": [
      {
        "info": "p3nlwpweb001.csv",
        "source": "file://p3nlwpweb001.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },
  "inferenceType": "TemporalAnomaly",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "traffic"
  },
  "swarmSize": "medium"
}



def swarm_over_data():
  return permutations_runner.runWithConfig(SWARM_CONFIG,
    {'maxWorkers': 8, 'overwrite': True})



def run_php_experiment():
  input_file = "p3nlwpweb001.csv"
#  generate_data.run(input_file)
  model_params = swarm_over_data()
  if PLOT:
    output = NuPICPlotOutput("php_output", show_anomaly_score=True)
  else:
    output = NuPICFileOutput("php_output", show_anomaly_score=True)
  model = ModelFactory.create(model_params)
  model.enableInference({"predictedField": "traffic"})

  with open(input_file, "rb") as sine_input:
    csv_reader = csv.reader(sine_input)

    # skip header rows
    csv_reader.next()
    csv_reader.next()
    csv_reader.next()

    # the real data
    for row in csv_reader:
        #      angle = float(row[0])
      traffic_value = float(row[1])
      result = model.run({"traffic": traffic_value})
      output.write(traffic_value, result, prediction_step=1)

  output.close()



if __name__ == "__main__":
  run_php_experiment()
