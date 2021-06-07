import json
import src.glsutils as gls

gls.error("reading...")
with open('trials_05242021.json', 'r') as f:
    filedata = f.read()
obj = json.loads(filedata)
gls.error("done.")

docs = obj['hits']['hits']
outdir = "./documents/"
cnt = 0
for doc in docs:
    docstr = json.dumps(doc)
    fname = outdir + str(cnt) + ".json"
    text_file = open(fname, "w")
    n = text_file.write(docstr)
    text_file.close()
    cnt = cnt + 1
    if cnt % 100 == 0: gls.error(cnt)

