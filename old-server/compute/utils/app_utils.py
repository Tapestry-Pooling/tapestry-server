# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=8
if __name__ == '__main__':
  raise ValueError('Run utils/test_app_utils.py. This is a library file.')

import numpy as np
import itertools as it
import string

from core import config
from core.cs import CS
from utils.output_validation_utils import detect_discrepancies_in_test

# Get results given a matrix M and cycle times cts
def get_test_results(M, cts, algo):
  y = get_y_from_cts(cts)
  sure_list, unsure_list, neg_list, x, errors = _get_infected_lists(M, y, algo)
  return sure_list, unsure_list, neg_list, x


# Get y (viral loads in each test) from cycle times
def get_y_from_cts(cts):
  # First get the min cycle time. This corresponds to the test with the
  # maximum viral load. This sample will have the least amount of variance
  # in cycle time, so good to choose this as the baseline
  ctmin = np.min(cts)      

  # Now filter out the positive tests
  # Treat 0 as -ve test as well. This will prevent end-user error such as
  # unchecking "Threshold Not Reached" in the app but not putting a value.
  bool_y = np.logical_and(cts < config.cycle_time_cutoff, cts > 0).astype(np.int32)
  #bool_y = (cts < config.cycle_time_cutoff).astype(np.int32)
  cts = cts * bool_y

  y = (1 + config.p) ** (ctmin - cts)
  y = y * bool_y

  return y

def build_cs_object(M, y):
  assert M is not None

  n = M.shape[1]
  t = M.shape[0]

  assert t == len(y)

  # unused params
  arr = np.zeros(n)
  mr = None
  d = 1
  s = 0.5
  l = 0.1


  cs = CS(n, t, s, d, l, arr, M, mr)
  return cs, t, n

# This function calls the decoding algorithm in class CS
# The algorithm chosen can be configured using config.app_algo
def _get_infected_lists(M, y, algo):
  cs, t, n = build_cs_object(M, y)
  bool_y = (y > 0).astype(np.int32)
  if algo == 'COMP':
    infected, infected_dd, score, tp, fp, fn, surep, unsurep,\
        num_infected_in_test = \
        cs.decode_comp_new(bool_y, compute_stats=False)
    x = np.zeros(n)
  else:
    x, infected, infected_dd, prob1, prob0, score, tp, fp, fn, uncon_negs, determined,\
        overdetermined, surep, unsurep, wrongly_undetected,\
        num_infected_in_test = cs.decode_lasso(y, algo, prefer_recall=False,
            compute_stats=False)

  errors = detect_discrepancies_in_test(t, bool_y, num_infected_in_test)
  sure_list, unsure_list, neg_list = _get_lists_from_infected(infected,
      infected_dd, n)
  
  return sure_list, unsure_list, neg_list, x, errors


# Get list of sure, unsure and negative people
def _get_lists_from_infected(infected, infected_dd, n):
  sure_list = []
  unsure_list = []
  neg_list = []
  for i in range(n):
    if infected_dd[i] == 1:
      sure_list.append(i+1)
    elif infected[i] == 1:
      unsure_list.append(i+1)
    else:
      neg_list.append(i+1)

  return sure_list, unsure_list, neg_list


# Detect errors using COMP and give more conservative results
def detect_errors_and_get_conservative_results(M, cts):
  # Run COMP and get errors
  y = get_y_from_cts(cts)
  bool_y = (y > 0).astype(np.int32)

  cs, t, n = build_cs_object(M, y)

  # Call COMP to get num_infected_in_tests
  _infected, _infected_dd, _score, _tp, _fp, _fn, _surep, _unsurep,\
      num_infected_in_test = \
      cs.decode_comp_new(bool_y, compute_stats=False)

  # Get discrepancies in COMP output
  errors = detect_discrepancies_in_test(t, bool_y, num_infected_in_test)

  # COMP will only output type 1 error
  assert errors['err2'] == 0 and len(errors['err2lst']) == 0
  assert len(errors['err1lst']) == errors['err1']
  total_errors = errors['err1']

  # If there are no errors, then we return
  if total_errors == 0:
    res = {}
    res['errors'] = False
    res['result_string'] = ''
    return res
  else:
    # Now get count of number of positive tests each sample is involved in
    # We will output a categorized list by number of positive tests
    num_positive_tests = cs.count_num_positive_tests(bool_y)

    # XXX: We consider only upto 3-positives. This will need to change later if our
    # matrix has more than 3 positives
    categorized_samples = { i:[] for i in range(4) }
    for sample, num_positive in enumerate(num_positive_tests):
      categorized_samples[num_positive].append(sample)

    # Now build result string
    result_string = get_result_string(errors['err1lst'], categorized_samples, t)
    res = {}
    res['errors'] = True
    res['result_string'] = result_string
    return res

def get_well_for_test(test, t):
  C = [f'{tup[0]}{tup[1]}' for tup in it.product(string.ascii_uppercase,range(1,13))]
  if t < 48:
    return C[test * 2]
  else:
    return C[test]

# Gets end-user-friendly result string in case of error
def get_result_string(err1lst, categorized_samples, t):
  assert len(err1lst) > 0
  header = '\nDiscrepancies were detected in the cycle time (CT) values entered by you.\n'
  header += 'They failed an internal consistency check.\n'
  header += 'Perhaps you forgot to input the CT value for some well(s)?\n'
  header += 'Other causes can be: \n'
  header += '  * contamination of some well from a nearby well\n'
  header += '  * very low viral load in some sample, due to which a mixed sample\n'
  header += '    did not reach cycle time threshold\n'
  header += '\nHere are the errors:\n\n'
  
  # List discrepancies detected by COMP
  errors_str = ''
  for test in err1lst:
    errors_str += f'Well {get_well_for_test(test, t)} is positive but no positive sample found\n'
  
  errors_str += '\n'
  # Give explanation to user about error categories
  explanation_str = ''
  explanation_str += 'We list the samples below, categorized by the number of tests'\
      ' they were positive in.\n\n'
  explanation_str += 'Samples appearing in 3 positive tests are most likely to be positive. \n'
  explanation_str += 'Samples appearing in 2 positive tests may also be positive\n'
  explanation_str += 'Samples appearing in 1 positive test are very unlikely to be positive\n'
  explanation_str += 'Samples appearing in 0 positive tests are negative\n\n'

  # Show categorized samples
  results_str = ''
  for tests in [3, 2, 1, 0]:
    results_str += f'Samples positive in {tests} tests: '
    results_str += ', '.join([str(item + 1) for item in categorized_samples[tests]
        ])
    results_str += '\n\n'

  final_str = header + errors_str + explanation_str + results_str
  return final_str
