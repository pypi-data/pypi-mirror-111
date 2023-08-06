from __init__ import * 
from pprint import pprint

import solana

conn = Connection()
pubkey = "AwqwB1CehyuriGiZLXueyo7PmKwHwf23a77SY9GSwpAe"

# signatures= conn.get_signatures(pubkey, limit=50)['result']
# last_sig = signatures[-1]['signature']

# signature_data = conn.get_transaction_data(last_sig)

# print('>>> LAST SIGNATURE')
# print(signature_data) 


token_accs = conn.get_token_accounts(pubkey)
print(token_accs)