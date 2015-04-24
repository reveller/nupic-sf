MODEL_PARAMS = \
{ 'aggregationInfo': { 'days': 0,
                       'fields': [],
                       'hours': 0,
                       'microseconds': 0,
                       'milliseconds': 0,
                       'minutes': 0,
                       'months': 0,
                       'seconds': 0,
                       'weeks': 0,
                       'years': 0},
  'model': 'CLA',
  'modelParams': { 'anomalyParams': { u'anomalyCacheRecords': None,
                                      u'autoDetectThreshold': None,
                                      u'autoDetectWaitRecords': None},
                   'clParams': { 'alpha': 0.08954732795128603,
                                 'clVerbosity': 0,
                                 'regionName': 'CLAClassifierRegion',
                                 'steps': '1,6,24'},
                   'inferenceType': 'TemporalMultiStep',
                   'sensorParams': { 'encoders': { '_classifierInput': { 'classifierOnly': True,
                                                                         'clipInput': True,
                                                                         'fieldname': 'ps_count',
                                                                         'maxval': 750.0,
                                                                         'minval': 0.0,
                                                                         'n': 326,
                                                                         'name': '_classifierInput',
                                                                         'type': 'ScalarEncoder',
                                                                         'w': 21},
                                                   u'ps_count': { 'clipInput': True,
                                                                  'fieldname': 'ps_count',
                                                                  'maxval': 750.0,
                                                                  'minval': 0.0,
                                                                  'n': 402,
                                                                  'name': 'ps_count',
                                                                  'type': 'ScalarEncoder',
                                                                  'w': 21},
                                                   u'timestamp_dayOfWeek': None,
                                                   u'timestamp_timeOfDay': { 'fieldname': 'timestamp',
                                                                             'name': 'timestamp',
                                                                             'timeOfDay': ( 21,
                                                                                            8.974333847576357),
                                                                             'type': 'DateEncoder'},
                                                   u'timestamp_weekend': None,
                                                   u'traffic': None},
                                     'sensorAutoReset': None,
                                     'verbosity': 0},
                   'spEnable': True,
                   'spParams': { 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 0,
                                 'maxBoost': 2.0,
                                 'numActiveColumnsPerInhArea': 40,
                                 'potentialPct': 0.8,
                                 'seed': 1956,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.03874511211683415},
                   'tpEnable': True,
                   'tpParams': { 'activationThreshold': 15,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 9,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 'pamLength': 5,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}