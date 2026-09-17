import json

BASE = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/_scan_tmpdir/'
pre = json.load(open(BASE + 'audit_results_g43pre.json'))
post = json.load(open(BASE + 'audit_results_g43post.json'))

def pkey(page, p):
    w = p.get('where') or {}
    return (page, p.get('cat'), p.get('type'), w.get('tag'), w.get('id'),
            str(w.get('row'))[:24], str(w.get('text'))[:16], str(p.get('detail'))[:24])

# (1) page counts equal and == 133
c1 = (len(pre) == len(post) == 133)

# (2) post pages with problems>0 == 0
post_prob_pages = [i['page'] for i in post if len(i.get('problems') or []) > 0]
c2 = (len(post_prob_pages) == 0)

# (3) dead_links all 0 (both snapshots)
pre_dl = sum(len(i.get('dead_links') or []) for i in pre)
post_dl = sum(len(i.get('dead_links') or []) for i in post)
c3 = (pre_dl == 0 and post_dl == 0)

# (4) js_errors excluding net::ERR_ offline-class == 0 (both snapshots)
def nonnet(jelist):
    return [e for e in (jelist or []) if 'net::ERR_' not in str(e.get('text', ''))]
pre_nonnet = [(i['page'], e) for i in pre for e in nonnet(i.get('js_errors'))]
post_nonnet = [(i['page'], e) for i in post for e in nonnet(i.get('js_errors'))]
pre_exempt = sum(len(i.get('js_errors') or []) for i in pre) - len(pre_nonnet)
post_exempt = sum(len(i.get('js_errors') or []) for i in post) - len(post_nonnet)
c4 = (len(pre_nonnet) == 0 and len(post_nonnet) == 0)

# (5) problem-key diff: new keys in post vs pre == 0
pre_keys = set(pkey(i['page'], p) for i in pre for p in (i.get('problems') or []))
post_keys = set(pkey(i['page'], p) for i in post for p in (i.get('problems') or []))
new_keys = post_keys - pre_keys
c5 = (len(new_keys) == 0)

print(f"(1) pages pre={len(pre)} post={len(post)} equal_and_133={c1}")
print(f"(2) post pages with problems>0: {len(post_prob_pages)} -> {c2}")
print(f"(3) dead_links pre={pre_dl} post={post_dl} all_zero={c3}")
print(f"(4) js_errors non-net::ERR_ pre={len(pre_nonnet)} post={len(post_nonnet)} (exempt net::ERR_: pre={pre_exempt} post={post_exempt}) -> {c4}")
print(f"(5) problem-key diff pre={len(pre_keys)} post={len(post_keys)} NEW-in-post={len(new_keys)} -> {c5}")
for k in sorted(map(str, new_keys)):
    print("  NEW:", k)
overall = all([c1, c2, c3, c4, c5])
print(f"GATE2 OVERALL: {'PASS' if overall else 'FAIL'} ({sum([c1,c2,c3,c4,c5])}/5)")
