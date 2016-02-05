# 2015.12.21 17:51:54 CST
import sys
import json
from elasticsearch import Elasticsearch

class BasicPeeker:
    def __init__(self, ips):
        self.es = Elasticsearch(ips)

    def queryprimaries(self, indexname, bid, messageid):
        query = {
            'query': {
                'bool': {
                    'must': [
                        {
                            "term": {
                                bid+"-modification.result":messageid
                            }
                        }
                    ]
                }
            },
            'from': 0,
            'size': 200
        }
        return self.es.search(index=indexname, doc_type=bid + '-modification', body=query)

    def querydetails(self, indexname, bid, messageid):
        query = {
            'query':{
                'bool':{
                    'should':[
                        {
                            'term':{
                                bid+'-assembler.messageId':messageid
                            }
                        },
                        {
                            'term':{
                                bid+'-modification.messageId':messageid
                            }
                        }
                    ]
                }
            }
        }
        return self.es.search(index=indexname, body=query)

    def actions(self, indexname, bid, messageId):
        rawhits = self.querydetails(indexname, bid, messageId)
        ans = {}
        for hit in rawhits['hits']['hits']:
            dt = {}
            doc = hit['_source']
            action = doc['action']
            dt["timestamp"] = doc["@timestamp"]
            if 'content' in doc:
                dt['content'] = doc['content']
            if 'result' in doc:
                dt['result'] = doc['result']
            ans[action] = dt
        return ans

    def bid2index(self, bid, date):
        if bid == 'sxitem':
            return 'deltadump-ms2-'+date
        return 'deltadump-'+date

    def clean(self, actions):
        if 'ModificationRunner.messageId' in actions:
            del actions['ModificationRunner.messageId']
        if 'FormatTransformer.transform' in actions and 'ModificationRunner.basicHandle.throwOut' in actions:
            del actions['ModificationRunner.basicHandle.throwOut']
        if 'AssembleWrapper.run' in actions and 'FormatTransformer.transform' in actions:
            del actions['FormatTransformer.transform']
        return actions

    def search(self, bid, date, key):
        return 'mock data'
        # indexname = self.bid2index(bid, date)
        # ans = []
        # rawhits = self.queryprimaries(indexname, bid, key)
        # for hit in rawhits['hits']['hits']:
        #     active = {}
        #     messageId = hit['_source']['messageId']
        #     active['messageId'] = messageId
        #     actions = self.actions(indexname, bid, messageId)
        #     active['actions'] = self.clean(actions)
        #     ans.append(active)
        # ans.sort(cmp, lambda x: x['messageId'], True)
        # return ans


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '{bid} {date} {messageid} should be specified,\nusage: python', sys.argv[0]
        print 'realtimeitem|mainsearch|sxitem|traderate 20160122 256327644'
    else:
        bid = sys.argv[1]
        date = sys.argv[2]
        messageid = sys.argv[3]
        rtip = BasicPeeker(['10.11.3.190:1024'])
        data = rtip.search(bid, date, messageid)
        print data
