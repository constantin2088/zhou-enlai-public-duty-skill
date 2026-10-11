"""Validate evidence/action packet structure, never certify factual truth."""
import json,sys
def validate(packet):
    if not isinstance(packet,dict):raise ValueError('packet must be an object')
    items=packet.get('items')
    if not isinstance(items,list) or not items:raise ValueError('nonempty items required')
    ids=set()
    for item in items:
        if not isinstance(item,dict):raise ValueError('item must be an object')
        ident=item.get('id')
        if not isinstance(ident,str) or not ident.strip() or ident in ids:raise ValueError('unique nonempty id required')
        ids.add(ident)
        if item.get('status') not in ('supported','inference','unknown'):raise ValueError('explicit epistemic status required')
        if not any(isinstance(item.get(k),str) and item[k].strip() for k in ('source','next_check')):raise ValueError('source or next_check required')
        if item['status']=='unknown' and not (isinstance(item.get('next_check'),str) and item['next_check'].strip()):raise ValueError('unknown needs next_check')
    return len(items)
if __name__=='__main__':
    print('Structurally valid items:',validate(json.loads(open(sys.argv[1],encoding='utf-8').read())))
