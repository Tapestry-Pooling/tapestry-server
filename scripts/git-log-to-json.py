import json
import sys
def parse_git_log(ls):
    res = []
    o = {}
    for l in ls:
        if l == "" or l.isspace():
            res.append(o)
            continue
        if l[0] == 'P':
            o = json.loads(l[1:].strip())
        else:
            o['patch_set'] = o.get('patch_set', []) 
            t, p = l[0], l[1:].strip()
            if t == 'R':
                    p = p.split('\t')[1]
            o['patch_set'].append({"path" : p, "type" : t})
    return json.dumps({"commits" : res})
print(parse_git_log((line for line in sys.stdin)))
