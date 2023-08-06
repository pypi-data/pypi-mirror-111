from pangaeapy import PanDataSet, PanQuery
totalcount = 10000000000
position = offset = 0
limit = 10
while position+offset < totalcount:
    pq = PanQuery(query='project:OA-ICC', offset =offset, limit=limit)
    totalcount = int(pq.totalcount)
    print('Totalcount'+str(totalcount))
    res = pq.result
    for result in res:
        ds = PanDataSet(result.get('URI'), include_data=False)
    print(ds.title)
    offset = offset + limit