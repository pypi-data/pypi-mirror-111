#!/usr/bin/env python
# coding: utf-8
import codecs

from tronpytool import Tron

# tron = Tron().setNetwork('nile')
tron = Tron().setNetwork('default')
hash_tx_id = "5bad50ba5b1fecab40f8685a808865872310e635be7f5eaa3aea77dc9da209ce"
result = tron.Chain.get_transaction(hash_tx_id)
# res = dict(result)
print(type(result))
# result = tron.Chain.get_transaction_info(hash_tx_id)
for u in result:
    print(u)
if "raw_data" in result:
    print(result["raw_data"])

    result = tron.Chain.get_transaction_info(hash_tx_id)
    # 111111331

    note = result["log"][0]["data"]

    # print(tron.address.from_hex(note))
    print(note)
    print(codecs.decode(codecs.encode(note, 'hex'), 'ascii'))
