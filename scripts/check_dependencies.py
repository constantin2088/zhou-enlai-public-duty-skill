"""Local deterministic aid; never a factual or model behavior certificate."""
def analyze(p):
 nodes=p['nodes'];d={n['id']:n['depends'] for n in nodes}
 if not nodes or len(d)!=len(nodes):raise ValueError('nonempty unique nodes required')
 visited=set();active=set();order=[]
 def visit(k):
  if k not in d:raise ValueError('missing dependency')
  if k in active:raise ValueError('cyclic dependency')
  if k in visited:return
  active.add(k)
  for dep in d[k]:visit(dep)
  active.remove(k);visited.add(k);order.append(k)
 for k in d:visit(k)
 return {'dependency_order':order,'note':'Order is a structural possibility, not a capacity, safety, priority or profitability assessment.'}

if __name__=='__main__':
 import json,sys
 print(json.dumps(analyze(json.loads(open(sys.argv[1],encoding='utf-8').read())),ensure_ascii=False,indent=2))
