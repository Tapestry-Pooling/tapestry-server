# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=8

# Helpers to check if output of COMP etc are ok

# Detects discrepancies which can happen due to experimental error or using
# wrong matrix, or poor algorithm performance.
def detect_discrepancies_in_test(t, bool_y, num_infected_in_test, log=True):
  err1 = 0
  err2 = 0
  err1lst = []
  err2lst = []
  for test in range(t):
    if bool_y[test] > 0 and num_infected_in_test[test] == 0:
      if log:
        print('y[%d] is infected but no infected people found' % test)
      err1 += 1
      err1lst.append(test)
    if bool_y[test] == 0 and num_infected_in_test[test] > 0:
      if log:
        print('y[%d] is not infected but infected people found' % test)
      err2 += 1
      err2lst.append(test)
  return {
      'err1' :  err1,
      'err2' : err2,
      'err1lst' : err1lst,
      'err2lst': err2lst,
      }

