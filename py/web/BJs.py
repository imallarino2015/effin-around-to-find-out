import time
import json

import requests


def log_in_api(username, password):
    session = requests.Session()
    login_headers = {
        'content-type': 'application/json'
    }
    login_payload = {
        "deviceProfile": "eyJjb21wb25lbnRzIjpbeyJrZXkiOiJ1c2VyQWdlbnQiLCJ2YWx1ZSI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4N"
                         "l82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwOC4wLjAuMCBTYWZhcmkvNT"
                         "M3LjM2In0seyJrZXkiOiJsYW5ndWFnZSIsInZhbHVlIjoiZW4tVVMifSx7ImtleSI6ImNvbG9yRGVwdGgiLCJ2YWx1ZSI"
                         "6MjR9LHsia2V5IjoiZGV2aWNlTWVtb3J5IiwidmFsdWUiOjh9LHsia2V5IjoiaGFyZHdhcmVDb25jdXJyZW5jeSIsInZh"
                         "bHVlIjo2fSx7ImtleSI6InNjcmVlblJlc29sdXRpb24iLCJ2YWx1ZSI6WzE5MjAsMTA4MF19LHsia2V5IjoiYXZhaWxhY"
                         "mxlU2NyZWVuUmVzb2x1dGlvbiIsInZhbHVlIjpbMTkyMCwxMDUzXX0seyJrZXkiOiJ0aW1lem9uZU9mZnNldCIsInZhbH"
                         "VlIjozMDB9LHsia2V5IjoidGltZXpvbmUiLCJ2YWx1ZSI6IkFtZXJpY2EvS2VudHVja3kvTW9udGljZWxsbyJ9LHsia2V"
                         "5Ijoic2Vzc2lvblN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJsb2NhbFN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0s"
                         "eyJrZXkiOiJpbmRleGVkRGIiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJhZGRCZWhhdmlvdXIiLCJ2YWx1ZSI6ZmFsc2V9L"
                         "Hsia2V5Ijoib3BlbkRhdGFiYXNlIiwidmFsdWUiOnRydWV9LHsia2V5IjoiY3B1Q2xhc3MiLCJ2YWx1ZSI6bnVsbH0sey"
                         "JrZXkiOiJwbGF0Zm9ybSIsInZhbHVlIjoiTGludXggeDg2XzY0In0seyJrZXkiOiJwbHVnaW5zIiwidmFsdWUiOltbIlB"
                         "IalJvMDYiLCJObVRKRWlSbzA2ZE9Iang0Y09IREJBQUFnUUlFaVJvIixbWyIiLCI2OWUiXV1dLFsiQnJvd3NlciBQREYg"
                         "cGx1Zy1pbiIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24veC1nb29nbGUtY2hyb21lLXBkZ"
                         "iIsInBkZiJdXV0sWyJPcGVuU291cmNlIFBERiBhbmQgUFMgZXh0ZW5zaW9uIiwiIixbWyJhcHBsaWNhdGlvbi9wZGYiLC"
                         "JwZGYiXV1dLFsiLiAgICAgICAiLCJxMTZkT256NWNPblRKa3laczJidFdyVnExNjkuIGZQSCIsW1siIiwiR2p4Il1dXV1"
                         "9LHsia2V5Ijoid2ViZ2wiLCJ2YWx1ZSI6WyJkYXRhOmltYWdlL3BuZztiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVV"
                         "Z0FBQVN3QUFBQ1dDQVlBQUFCa1c3WFNBQUFBQVhOU1IwSUFyczRjNlFBQUVSNUpSRUZVZUY3dG5WMklaRWNWeDAvMUlIa"
                         "0lJbmtJb2lGZ3dCQlVvdmlKZ3JLOUNvb29xS0NnS0tpb1lFQUY5VUhCeVBaRlVRajRBUW9LaW9MaUJ5Z29lUWpvZzlOQl"
                         "FWR1MwZDJGV1RJaHU4bkdYVTJFMWF4bTFZMTdwYnJ2elBSMDMrNWJWYmRPMVRsMS8vdTJVQi9uL00rcFg1K3F1WFd2SWZ"
                         "6THBvQWhvbnJUN0owTnNwbU9pV2NLSUVDcEU4RXF6djhQY2VYWEdPc25qY2FZSlN1bTB3QUxRWVlDVU1CTEFWMi84ZW1z"
                         "MVF1c2RCcDVKUm9hUXdFb3dLY0FLN0RBRkw3QVlXUW80S3RBQ2V1UkZWaStncGJYdm9RVUtTOHE4RWl2QW1LQmhhV3VON"
                         "mxnZVJrS1NGeURZb0ZWUnNqaEJSU0FBakVWVUFjc2lkU1BHUkNNQlFXZ3dIb0YxQUVyZlRDQnlQU2FDNXlST3cyNHh4Y2"
                         "9hWWhKcW9HRkdJZUVISDA0RlVCT2Nxbzd2MXVBZjRJVndBSVFIQnlZbGx3QlVjQ0tzamlqREpJOER0RW1ITGo3ampwQ0p"
                         "VZWh4RFVUQlN4eDZzQWdLRkMwQXZyQURXQVZuWkJ3TG84QytrQVFwRk1HTnpNQ0s0TzNRVkZCSnlqQXJRRFdncXZDR1lI"
                         "bGFpTGFRWUVlQ29BRlBjUTc3TW9ubzkvSUFGYVVjR0tRVGdWYzh0S2xUZWRFYUZDU0Fzc3AwUjlZU0xLUzhnTytRQUhSQ"
                         "3ZRSFZyQjdJSjJYZEpETFN5NDBMbE9Cak1EU0lpaEk0UnVwdXFZeEVZMk5vWWx2WDdTSEFwc1VLQXhZZ0l0THVuT3IxQU"
                         "JybTRpT0cwTlRGNXZRQmdxNEtCQVJXTnpMd01VZHRKR2d3TFdhcG9ib21MWEZHRnova2hDVFVteUlDS3hTSklFZmZSVll"
                         "CQllSVmRnYTlsVlVYMyt1OGdYQTJwQUxYS0w3cDU4Y1MxeHN2MVpUdlpSWWdKYUxjR3ZhNklwK0QwY2R1Z0pZRGlJNU5V"
                         "Rld6V1M2V3RONGkyaTdKYkVBTGFkRVFxTUJIYnJuRGJZV1puSGFlYldtNlJiUnNUVy9oRGlFejV1aTZtZEhoYVUraExJY"
                         "zZBQlcyWWZ3bkw4RXNzS2N6Um9BSzVuMGFiSTV6U3pyUlh1cXBucGsvenE0dnNtOXhzeWUwOEkvS09DdEFJRGxMUms2ck"
                         "ZQQW5sOFpvdTA1c0RhaXMvczhLemQ1RVdhUkNnQllJc09pMHlpN0hiVFBYM1ZVV1B2T2RVTkxwd3h5ckM0UStnQ1dTM29"
                         "WR0hnWHQzM2JlQUxMRG85RGVGK1JCOTQrT3JDd3RvZWJVVmViNTY4Y0s2eVpVSGdTWGtxKzZGaTUwWUVsUlg3WWtWWUJl"
                         "MzVGemZOWDdzQ2FMUkljd3FjTkZmOXNqT3dMQmhhalRmeUNZb2JvQ3Z4Nzl2eVZPV2FvSm5kZ0haaUI4NnpvRVNsendHQ"
                         "mdsU2xIUHErMC93RE1nVFYvWURRQVdGWjRRQ3RmK3NtWnVXTWhDQUdXOXVVcUo5NjVMUG5Qd3ZOWGdjQUN0SElGVDlHOF"
                         "FvQ2xTREdZdXFMQWxackdvNFBucjRJckxCekNJN2M2RlFDd09pVksyVUJucFhtbHBzbUk2TVIrWmRXandySmk0eEJlWnh"
                         "va1dTaUtnSVVvZG1aRUpvbXUxRFFkTFR3dzJoTlkyQnAyQmxweUE5NGs5QUlXcnlteGc4QmhMY2VZc2YxT1A5NlZhMVNQ"
                         "ek9GV01BeFlLOXJpRUQ1OUtNWFA2QVdzTUcrd3lNTjBFOWlySlpUMi9NbytmMlVoRldsTHVPZzRvQ1V3RGJ4TWlyejhFd"
                         "0RMeXowMFBsQWdjcVNabFAzWHd2a1ZBN0NzMWJpK3d4UzdmTU9HNXphQWxTOXFSMllPRDJGZUI1NWN1UERNQkN3Y3d1Y0"
                         "5zYWpaQWF6RTRkQUtwblV5UGJsd2Z6QWVzSENlbFRndDFVeTNBVmlsTFMxaE1TbEEzc3NMNzI5bk9zUENlWmF3dE0xdER"
                         "pcXMzQkZRdkRHOFhOTmtpK2lFVGFJRXdMSks0UkJlVkw2bU42WjRZS2t1WklRYmYzbnB3bk84TGVIR2hZQkQrUFNjRURO"
                         "ajhjQVNvM1NCaHZ4ejZmNWdJbURoRUw3QVhISjFxUXhnQ2E5RVhJT2hxWjA5dnpwOGYzdXlMZUcrUk81YlErUkdjRnBKb"
                         "Es0TVlDMkZKRXpvc0Y3QjJhQzhZMnBnMWF0ZjRuR0hsbkt0WTVtZlBjTWpHRkFrc0dJRmVENU9CSlhqR2lSaXRDZGE3Zz"
                         "htMmhMaUw0Y2lNaUNQRVFCV0h0M1Z6L3BFYzM2MUNLbW93R29wcWRhSWhrTjQ5ZG5rN2dDQTVhNFZXallLMk8xZzNYSi9"
                         "NQ3F3UE5UR2h5dzh4RkxlRk1CU0hzQWM1a3NERnA3UHlwRUZlZVlzRDFnNGNtTFBwTDh2bkYreGJRblhlYkYrcTRoRGVQ"
                         "Ykk1NTlBS2JCQXBaeXA4NDgxOXdjNXQ0U09SMXE2b0lVMGRrL2pSaXVsd0hMM0V5M2pLbkNwZVg5NzIzVWNUbUI1ZUlGR"
                         "GVBK3h0RFVGc0pKRnJJeWZVd1hBV3ZpYWRCbWFKMHRSQlJNQldBcUNsTS9FMVFWL3FUbS9FbHhoV2Jsd2ZTZGYwckRPdk"
                         "FGWStIVmlWVjdwNEpjMjNCOWMyUkk2SGp3eFNhSHJQSXRKaE5LR1ZWRmhBWjB5MHM1dUIvZmYzNzZwd3RxU1lhNjF3aGx"
                         "heURFNVFkdGtDUk93d3NJZjFrdUgwQ1ZZNlFxc3NLL21zQ21FUTNnMmFkTVB6QVNzOUk2b20xRWhuZjgyZS84VkhWdjM3"
                         "SldRdnhLdXBBS2VoRmUzT3RZYW5CRllDbGRzT1hFUDhpUW5zSG9laCtFUVBpamk4anBsQkJhZkdFQmhmRzBmYjU2L1duN"
                         "FZjdkluM2NOZGN6N1BDcDhpdENjeTFsVzVJb0hsNmp6YXVTc3dBMVpOMjh0ZmVJNEhyQ1NMVmpDMDNHTXg1SllSZ1pVaz"
                         "RRWVhLeW1xUHU1d2YxRHFHZFpTMGdCYWlsZFJSR0FwVmlHNTZWSXc1TzU0UWNCYWVCTGUzWCswektCQXl6SUJzQUxpY0t"
                         "DalB1NEVlRXRrdDRQN3oxOHBQc05hOUIySDhFR1prTDlUd2NBYUNFMFM1RkNCd0xLcStXME5rVTRKTXExN2ltVEFRcnk3"
                         "ZzdIZm9sT3J6Z2J1YzdtMGZLeW1xV21ldnlxa3d0cDMydzlhTG1LcGFwTTRrU0pva3d4WUVXeFZPNFMrdERncWRjSEE4c"
                         "SswMUdaaEdZWTdBa3Y3a2lzaldNbThXQXIzWTBzdjdPTjUwajFyanVINlRyTGs2amVSSTdENlRTSzNkOVpGSWxlV0Jjc3"
                         "UxalRlSXRxMlN1MXZCM21BbFZVT1pZZnd3OG5iWlU4N2dTVlptbVMySlpzbzY2SnRuZnppVXpUZE1uU3NjR0ROdDRaYk5"
                         "KRVhnYklzYWwxS0h1dXJFMWhseVFWdmZCVzQrTi81aGVjQkFJdW9wc3BjQjJqNTVnaFArM2FLdFFMTEEzZzh0bUpVTVFy"
                         "ODVVbXFsN2VBOGJhRUFqUE5RdXQ2UU1zcEFUT0VEeFdXVTJTRzJlamlaUnFiNW9PcGc2aXdEc044M0R5ZHBzT011bXl2Q"
                         "WF3TXZ4S3lVK0xRdWd1WGFEb3lxKysvaWxkaENWV2lwbnZORGJPbisvRlBtQUtzd1BKaWdWZGpZU29XYXM2Rnh3Y0tMQn"
                         "RQdXpXOEVWdERhYW5OQ2l4cHpzSWVQd1V1L0hWK2ZzVjNodVZuejZ4MXp6ZjVlYzVZbVdjQ1dwNmFSV3J1Y2VnZWFjWjB"
                         "3NkE2aTY3MXhZczBycS9SdGpoZ1JmZTBjOERLM0FSb2RhcVVxTUZTaFZYWXloZm96dHdrZ1lZdEpkeWpqOUIwdEhCL2NH"
                         "Q0g3a2ZWTUhUYzNNeC9DTCthRmZMenhKMVRjWHpCbHRCZDhZT1djYVFQbURoaGwwZlBBbGlMY3B0YlpyOHkrSmRaQVlGQ"
                         "kdBSU9Na2ZkWWZvLzcxRzlXRlZ0ckxCcW91VlhKd3RNTEFldk56YXB6SzNZR3ZZVnNXLy9OSGtGQnZXTlU5TCs1M2RwUE"
                         "RKSDd3OE9la3U0cjc3OXkrSHpBSzJreWJnMFdScGc1ZlFRYzNzcmNQNFVUVWFHVGpoWFdBc1hvL2Y3Rkp0WUZscTNBMXJ"
                         "lU1JXcGcyTmUrWlpJdnUwamVkTU1rM2YydUw3a0dPMzhuK2JuVjZVQUsvcVRFQ002Ym03blA0VFBFWHZwY3pvQ1M3b2Jz"
                         "QyttQXVmdlg3MC9tSFZMS1BBWHlMd0VoL0F4Yzg1MXJHRUNTK0FDY0EwWWQ3dnpmNkF4MmU4UEVzMVdKSjdEV3F2NHZlW"
                         "VZ1TDdEblkvTDR3OFRXQ2xWVmdiSGgzOUxreEhSQ1FETEtVa3E4eXFjWjgxLzJ1ekdtLzhmZ0JWTDQzUXhpMlZ4Nnpqbm"
                         "ZqMS8vMVVXWUVVL2JHS1Zhbi93eXJ3RzBFcWlkRlAxcDVvTDh5aFE0T0ZwKy8zQnJHZFkwbldyNmJnNW51c1F2cEJmU3N"
                         "jWXE2aXdoaFVTeDhneE5EdTdUZVBSbXZ1RHVZRTFMNzdFWmtKbFhvY3FLeXdsL1dLYUdGaCt4b1VKZ0Y2aENwejl4ZUg1"
                         "VlpZdFlhamhlZnRWNWcydXNBckkvNEF1ZWVYZ25UMHhzSGlkd2VqOUZEaDd6L3I3ZzdhNkdWSGQrbGZEdHI4bUZwOVk5Z"
                         "0hTTjVsSnFzUG1mcEVWMkRzUXhNWG5sY0JRaVRYcDNOM3Q5d2UzR29zTC9zeVhlMHdzcU43aVdsRzVEK3ZhTW5DZHV3NH"
                         "Z2aDJBSlQ1RWFRdzgrN1A1Kzl2WFBYdVYrd3dyalFvYlo2bk0yL0tCU29EL0lrd0FzRVNFSWI4UlozOUNZN1Bod3ZOZ2d"
                         "XVXJxbmNBVkh3WjZsY3poZ0hMYnc0M1h6bkdkSnNacllqb29SL04zOStPQ3F0SkJ3dXFkd0ZVMGhaSEdMQ2tlZUZpRDRD"
                         "NFVhV0hmckQ1L3VDQUtxekt2THNGVkFQUEh5bnVEd2RZTGxBYmFKdTk3OU40cTNuK0txakNLdU1GZnBVTnYza3ZxaXJKe"
                         "TJBRHNLUXdsVk0rN1Q3R3NYL3Z1elRlNnJqd1hIU0ZaYmQvSHdDb09GZGFyTEdGVjFoeEZtUU1zYUpZRW1XUUdONGNIV1"
                         "B2VzkzM0J3c0ZWbVUrQkZERnp5aStFWmVBSlhSRjhmbnZPWElhZmRMTWN1ajZnOS9vdmo5WUdMQXFjNGNNVUtXT3RXZkN"
                         "pMnZPV21FaEdPTGl2V0xRM3RmbWp6TzB2ZmRxM1htVzJrL1YyNjNmUjJXQVNuNW15TFNRRDFqY3RPSWVYMmE4b2x1MTk1"
                         "VUJBTXVDNnVOYVFJWEUzcFRrZk1DS3ZyUUdQaUJUSGovd3BVMzNCOVcvY2JReW45UUNxb0hudDZQN3VvREZ0R2dkdFNxe"
                         "TJRTjNIWjVmdVd6MVhMZU9XUlBMVmxTZkFxaEtUTmlzZVNWUlVKbE01TEZxNzRzMHJwdkhHVnhCNU5vdUtMSDZ1bG5UL0"
                         "ZtcXo4U0RWVitUSk9hNFpwdUM4aXFudzBpZ2VPcnZmWTdHTlIwZXVJZFZXUGJGTTZ1dm5ZbWRXQTV2VDY3TVorT0JLcDd"
                         "LR0NtbUFtRjVCV3JFakVHMnNjNU1hRHFxNSs5dmQ2MmNYTnVGSlphREZLc0RWMllDVURrb3A2TkpCMXZZOGtxSE9zTzI4"
                         "c3lkUncvY0R5b3NRelNxUXo3emRWaHRKVWlzeW53ZW9OcVl3UVVXRmdueWF0aFFrT3I5N3AwMEh2M3Y2UHV2d3JhRTdXQ"
                         "mpTeXhEbGZrQ1FDVTFyN2p0WXNzcmJzTXhmajhGZGordERGZ1dWSGZ4Z2FyQVltUWxRVGI3cUVNQkFHc3hyRHBpMW85VV"
                         "RlL2RUOHkzZzlabDRXZFlsZmt5SDZnOFYzVVU3VEZJdUFJQTFvRjJBNklWRWUxK1RDQ3dGclBSVmxSZnRhQWFWbHpDbDN"
                         "JNVBUZEZQQUJZU0NEdHFiSDdFUnBUeSt0a1JKeGhtZVpacXE4bnJLcTBCelNYL1JsUXNBcXNERWJrMG51bzgrNSttTWJV"
                         "UEg4bGJFdFltVzhDVkVQTlN4ZS9BeW9zbDJIUlJySUNwei9ZL3Y2cmpCVldaYjROVUczT21UU1ZSSnBad2xjSGdCV3VuZ"
                         "HFlcDk4dkJGajJuT283QUZYdVJKSU9xZVcvaStYV0MvTW5WT0RVKythUE03UTlzYzVXWWJVOW5mNDlmT2doWWRqZHBsSk"
                         "FMbFJZYnFFc3B0V3A5OUI0MUh4d1lobFFiTUE2Vks4eVAwUkZWVXd5WlhBRXdGb251b0pmbTVCOE9mWE9vL2NIa3h5NjI"
                         "2M2Zqd0dxa0hpaHoxRUZBS3lCWmNTcHR5Y0VsZ1hWVDlPQnF0RGZtSUZsYVBlZkhpRElnQlE0L1ZhcUY2c3FqZ3JMRUZX"
                         "ejdlWFAwOEdxYndnQnU3NEtwdW1QQ2l1TnppSm1PZlZtR2hzNmV1RzVON0RNMGN2UFpLaDYydDBOcUFxZ1FBRXVpTWk5V"
                         "0VaNEFVdEY4TElZbVdWUzd4dzQrY2JWNnppOWdXVXJLWHNmMFZCMTNUMTZLaXB2OGRCQmhBSmV3Qkpoc2FjUk9sRGk2Vl"
                         "JnODVPdmp3OHN1LzI3L3BjQVZXQkkwTTFUZ2VLQjVhbEgvdWFNaEQzNTJ2a0hKMktjWVJGUjlZeGZBVlJKRTRZeE45cjh"
                         "TRHlkazVRQWxwTk0raHZ0akdtODFYTGgyWHRMYUtpNllRcFE2YzhJblI0QVdEcmo1bTMxenF0cHV0Vzh2OTI1d3JLdlNt"
                         "N2VsMlczZmpmK0JxRHlGajVuaCt3bFVud0RBS3ljQ1pWdzdwMVh0dDhmN0txd0xLaWU5VHRlVU1WUDY0VENZaXBXQlpae"
                         "kE4QmlsVnZPNEg5OCtlRUhVNTBxck9hOVZEZjluaGRXY2hRS3R3VEFEZGZPdHllQTVhdVl3dlk3TDZPeFdYUGh1YlhDTW"
                         "xUZGZEOUF4UkpxMEcxVlZnOU41QURMdzJpV1JDcDQwSjBYMHNRUW5YRDRwbUIxeTBtYTRLM0VCU2VEY3Rma0FFdTVrREh"
                         "OajgzdW5lZlQxSkQ5WUtxaEVkVmtqaDZtMi85WHQ1NUdSUlV6aGluR2lwMG5LV3p1T3dlQTFWZkJvUDVwVTIzbnRqWDNC"
                         "dzFWdDUwQnFJSkNpRTVaRkFDd3NzbGVKNWw1NTduejk3Y3ZIYlJYTDNnUW9Fb1NBRXdTVlFFQUs2cWM4Z2E3N3prMEdSR"
                         "2RzSUcyanlpODZOeDZVS1d0KytScEJZdmtLd0JneVk5Ukx3dnZ1NW1tSTBQVEZ6OVNlRVVGMmpybWlXNmgwZ0JyVVNQZG"
                         "VxbjdydWQ5ejZiSlN5OFVEaXZIcFlwbStoVklBeXo5T3NHRGdTcWcvZmUxdExBQldJNFJSZUk2Q29WbVVJQlJBUUNMVVZ"
                         "3TXJWT0I0QituNEk0NmRXcTNtbGVFQUdEeEdsUlM2T0FMRklBQ2NSVUlBRlpjQXpBYUZJQUNmQXFVVmw0QVdIeTVncEdo"
                         "QUJTSXJBQ0FGVmxRREFjRllpdFFXcFhVUjUvL0ExNlJIY1I1VXpGSkFBQUFBRWxGVGtTdVFtQ0MiLCJleHRlbnNpb25zO"
                         "kFOR0xFX2luc3RhbmNlZF9hcnJheXM7RVhUX2JsZW5kX21pbm1heDtFWFRfY29sb3JfYnVmZmVyX2hhbGZfZmxvYXQ7RV"
                         "hUX2Zsb2F0X2JsZW5kO0VYVF9mcmFnX2RlcHRoO0VYVF9zaGFkZXJfdGV4dHVyZV9sb2Q7RVhUX3RleHR1cmVfY29tcHJ"
                         "lc3Npb25fYnB0YztFWFRfdGV4dHVyZV9jb21wcmVzc2lvbl9yZ3RjO0VYVF90ZXh0dXJlX2ZpbHRlcl9hbmlzb3Ryb3Bp"
                         "YztFWFRfc1JHQjtPRVNfZWxlbWVudF9pbmRleF91aW50O09FU19mYm9fcmVuZGVyX21pcG1hcDtPRVNfc3RhbmRhcmRfZ"
                         "GVyaXZhdGl2ZXM7T0VTX3RleHR1cmVfZmxvYXQ7T0VTX3RleHR1cmVfZmxvYXRfbGluZWFyO09FU190ZXh0dXJlX2hhbG"
                         "ZfZmxvYXQ7T0VTX3RleHR1cmVfaGFsZl9mbG9hdF9saW5lYXI7T0VTX3ZlcnRleF9hcnJheV9vYmplY3Q7V0VCR0xfY29"
                         "sb3JfYnVmZmVyX2Zsb2F0O1dFQkdMX2NvbXByZXNzZWRfdGV4dHVyZV9hc3RjO1dFQkdMX2NvbXByZXNzZWRfdGV4dHVy"
                         "ZV9ldGM7V0VCR0xfY29tcHJlc3NlZF90ZXh0dXJlX2V0YzE7V0VCR0xfY29tcHJlc3NlZF90ZXh0dXJlX3MzdGM7V0VCR"
                         "0xfY29tcHJlc3NlZF90ZXh0dXJlX3MzdGNfc3JnYjtXRUJHTF9kZWJ1Z19yZW5kZXJlcl9pbmZvO1dFQkdMX2RlcHRoX3"
                         "RleHR1cmU7V0VCR0xfZHJhd19idWZmZXJzO1dFQkdMX2xvc2VfY29udGV4dDtXRUJHTF9tdWx0aV9kcmF3Iiwid2ViZ2w"
                         "gYWxpYXNlZCBsaW5lIHdpZHRoIHJhbmdlOlsxLCAxXSIsIndlYmdsIGFsaWFzZWQgcG9pbnQgc2l6ZSByYW5nZTpbMSwg"
                         "MTAyM10iLCJ3ZWJnbCBhbHBoYSBiaXRzOjgiLCJ3ZWJnbCBhbnRpYWxpYXNpbmc6eWVzIiwid2ViZ2wgYmx1ZSBiaXRzO"
                         "jgiLCJ3ZWJnbCBkZXB0aCBiaXRzOjI0Iiwid2ViZ2wgZ3JlZW4gYml0czo4Iiwid2ViZ2wgbWF4IGFuaXNvdHJvcHk6MT"
                         "YiLCJ3ZWJnbCBtYXggY29tYmluZWQgdGV4dHVyZSBpbWFnZSB1bml0czo2NCIsIndlYmdsIG1heCBjdWJlIG1hcCB0ZXh"
                         "0dXJlIHNpemU6MTYzODQiLCJ3ZWJnbCBtYXggZnJhZ21lbnQgdW5pZm9ybSB2ZWN0b3JzOjQwOTYiLCJ3ZWJnbCBtYXgg"
                         "cmVuZGVyIGJ1ZmZlciBzaXplOjgxOTIiLCJ3ZWJnbCBtYXggdGV4dHVyZSBpbWFnZSB1bml0czozMiIsIndlYmdsIG1he"
                         "CB0ZXh0dXJlIHNpemU6ODE5MiIsIndlYmdsIG1heCB2YXJ5aW5nIHZlY3RvcnM6MzEiLCJ3ZWJnbCBtYXggdmVydGV4IG"
                         "F0dHJpYnM6MTYiLCJ3ZWJnbCBtYXggdmVydGV4IHRleHR1cmUgaW1hZ2UgdW5pdHM6MzIiLCJ3ZWJnbCBtYXggdmVydGV"
                         "4IHVuaWZvcm0gdmVjdG9yczo0MDk2Iiwid2ViZ2wgbWF4IHZpZXdwb3J0IGRpbXM6WzgxOTIsIDgxOTJdIiwid2ViZ2wg"
                         "cmVkIGJpdHM6OCIsIndlYmdsIHJlbmRlcmVyOldlYktpdCBXZWJHTCIsIndlYmdsIHNoYWRpbmcgbGFuZ3VhZ2UgdmVyc"
                         "2lvbjpXZWJHTCBHTFNMIEVTIDEuMCAoT3BlbkdMIEVTIEdMU0wgRVMgMS4wIENocm9taXVtKSIsIndlYmdsIHN0ZW5jaW"
                         "wgYml0czowIiwid2ViZ2wgdmVuZG9yOldlYktpdCIsIndlYmdsIHZlcnNpb246V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4"
                         "wIENocm9taXVtKSIsIndlYmdsIHVubWFza2VkIHZlbmRvcjpHb29nbGUgSW5jLiAoR29vZ2xlKSIsIndlYmdsIHVubWFz"
                         "a2VkIHJlbmRlcmVyOkFOR0xFIChHb29nbGUsIFZ1bGthbiAxLjMuMCAoU3dpZnRTaGFkZXIgRGV2aWNlIChTdWJ6ZXJvK"
                         "SAoMHgwMDAwQzBERSkpLCBTd2lmdFNoYWRlciBkcml2ZXIpIiwid2ViZ2wgdmVydGV4IHNoYWRlciBoaWdoIGZsb2F0IH"
                         "ByZWNpc2lvbjoyMyIsIndlYmdsIHZlcnRleCBzaGFkZXIgaGlnaCBmbG9hdCBwcmVjaXNpb24gcmFuZ2VNaW46MTI3Iiw"
                         "id2ViZ2wgdmVydGV4IHNoYWRlciBoaWdoIGZsb2F0IHByZWNpc2lvbiByYW5nZU1heDoxMjciLCJ3ZWJnbCB2ZXJ0ZXgg"
                         "c2hhZGVyIG1lZGl1bSBmbG9hdCBwcmVjaXNpb246MTAiLCJ3ZWJnbCB2ZXJ0ZXggc2hhZGVyIG1lZGl1bSBmbG9hdCBwc"
                         "mVjaXNpb24gcmFuZ2VNaW46MTUiLCJ3ZWJnbCB2ZXJ0ZXggc2hhZGVyIG1lZGl1bSBmbG9hdCBwcmVjaXNpb24gcmFuZ2"
                         "VNYXg6MTUiLCJ3ZWJnbCB2ZXJ0ZXggc2hhZGVyIGxvdyBmbG9hdCBwcmVjaXNpb246MTAiLCJ3ZWJnbCB2ZXJ0ZXggc2h"
                         "hZGVyIGxvdyBmbG9hdCBwcmVjaXNpb24gcmFuZ2VNaW46MTUiLCJ3ZWJnbCB2ZXJ0ZXggc2hhZGVyIGxvdyBmbG9hdCBw"
                         "cmVjaXNpb24gcmFuZ2VNYXg6MTUiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgaGlnaCBmbG9hdCBwcmVjaXNpb246MjMiL"
                         "CJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgaGlnaCBmbG9hdCBwcmVjaXNpb24gcmFuZ2VNaW46MTI3Iiwid2ViZ2wgZnJhZ2"
                         "1lbnQgc2hhZGVyIGhpZ2ggZmxvYXQgcHJlY2lzaW9uIHJhbmdlTWF4OjEyNyIsIndlYmdsIGZyYWdtZW50IHNoYWRlciB"
                         "tZWRpdW0gZmxvYXQgcHJlY2lzaW9uOjEwIiwid2ViZ2wgZnJhZ21lbnQgc2hhZGVyIG1lZGl1bSBmbG9hdCBwcmVjaXNp"
                         "b24gcmFuZ2VNaW46MTUiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgbWVkaXVtIGZsb2F0IHByZWNpc2lvbiByYW5nZU1he"
                         "DoxNSIsIndlYmdsIGZyYWdtZW50IHNoYWRlciBsb3cgZmxvYXQgcHJlY2lzaW9uOjEwIiwid2ViZ2wgZnJhZ21lbnQgc2"
                         "hhZGVyIGxvdyBmbG9hdCBwcmVjaXNpb24gcmFuZ2VNaW46MTUiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgbG93IGZsb2F"
                         "0IHByZWNpc2lvbiByYW5nZU1heDoxNSIsIndlYmdsIHZlcnRleCBzaGFkZXIgaGlnaCBpbnQgcHJlY2lzaW9uOjAiLCJ3"
                         "ZWJnbCB2ZXJ0ZXggc2hhZGVyIGhpZ2ggaW50IHByZWNpc2lvbiByYW5nZU1pbjozMSIsIndlYmdsIHZlcnRleCBzaGFkZ"
                         "XIgaGlnaCBpbnQgcHJlY2lzaW9uIHJhbmdlTWF4OjMwIiwid2ViZ2wgdmVydGV4IHNoYWRlciBtZWRpdW0gaW50IHByZW"
                         "Npc2lvbjowIiwid2ViZ2wgdmVydGV4IHNoYWRlciBtZWRpdW0gaW50IHByZWNpc2lvbiByYW5nZU1pbjoxNSIsIndlYmd"
                         "sIHZlcnRleCBzaGFkZXIgbWVkaXVtIGludCBwcmVjaXNpb24gcmFuZ2VNYXg6MTQiLCJ3ZWJnbCB2ZXJ0ZXggc2hhZGVy"
                         "IGxvdyBpbnQgcHJlY2lzaW9uOjAiLCJ3ZWJnbCB2ZXJ0ZXggc2hhZGVyIGxvdyBpbnQgcHJlY2lzaW9uIHJhbmdlTWluO"
                         "jE1Iiwid2ViZ2wgdmVydGV4IHNoYWRlciBsb3cgaW50IHByZWNpc2lvbiByYW5nZU1heDoxNCIsIndlYmdsIGZyYWdtZW"
                         "50IHNoYWRlciBoaWdoIGludCBwcmVjaXNpb246MCIsIndlYmdsIGZyYWdtZW50IHNoYWRlciBoaWdoIGludCBwcmVjaXN"
                         "pb24gcmFuZ2VNaW46MzEiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgaGlnaCBpbnQgcHJlY2lzaW9uIHJhbmdlTWF4OjMw"
                         "Iiwid2ViZ2wgZnJhZ21lbnQgc2hhZGVyIG1lZGl1bSBpbnQgcHJlY2lzaW9uOjAiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZ"
                         "XIgbWVkaXVtIGludCBwcmVjaXNpb24gcmFuZ2VNaW46MTUiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgbWVkaXVtIGludC"
                         "BwcmVjaXNpb24gcmFuZ2VNYXg6MTQiLCJ3ZWJnbCBmcmFnbWVudCBzaGFkZXIgbG93IGludCBwcmVjaXNpb246MCIsInd"
                         "lYmdsIGZyYWdtZW50IHNoYWRlciBsb3cgaW50IHByZWNpc2lvbiByYW5nZU1pbjoxNSIsIndlYmdsIGZyYWdtZW50IHNo"
                         "YWRlciBsb3cgaW50IHByZWNpc2lvbiByYW5nZU1heDoxNCJdfSx7ImtleSI6IndlYmdsVmVuZG9yQW5kUmVuZGVyZXIiL"
                         "CJ2YWx1ZSI6Ikdvb2dsZSBJbmMuIChHb29nbGUpfkFOR0xFIChHb29nbGUsIFZ1bGthbiAxLjMuMCAoU3dpZnRTaGFkZX"
                         "IgRGV2aWNlIChTdWJ6ZXJvKSAoMHgwMDAwQzBERSkpLCBTd2lmdFNoYWRlciBkcml2ZXIpIn0seyJrZXkiOiJhZEJsb2N"
                         "rIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRMYW5ndWFnZXMiLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiaGFz"
                         "TGllZFJlc29sdXRpb24iLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiaGFzTGllZE9zIiwidmFsdWUiOmZhbHNlfSx7Imtle"
                         "SI6Imhhc0xpZWRCcm93c2VyIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6InRvdWNoU3VwcG9ydCIsInZhbHVlIjpbIjAiLC"
                         "JmYWxzZSIsImZhbHNlIl19LHsia2V5IjoiYXVkaW8iLCJ2YWx1ZSI6IjEyMy4wNDM1NjYyNTE3OTkzNSJ9XX0=",
        "keepMeSignedIn": "Y",
        "logonId": username,
        "logonPassword": password
    }
    response = session.post(
        "https://api.bjs.com/digital/live/api/v1.4/storeId/10201/login",
        data=json.dumps(login_payload),
        headers=login_headers
    )
    print(response)
    return session, json.loads(response.content)


def get_avail_offers_api(session):
    offer_header = {
        'Content-Type': 'application/json',
        'Referer': 'https://www.bjs.com/',
    }
    offer_payload = {
        'brand': "",
        'category': "",
        'indexForPagination': 0,
        'pagesize': 1000,
        'isNext': True,
        'isPrev': False,
        'searchString': "",
    }
    response = session.post(
        "https://api.bjs.com/digital/live/api/v1.0/member/available/offers",
        headers=offer_header,
        data=json.dumps(offer_payload)
    )
    print(response)
    print(response.content)
    return json.loads(response.content)


def get_clipped_offers_api(session):
    offer_header = {
        'content-type': 'application/json',
    }
    offer_payload = {
        'brand': "",
        'category': "",
        'indexForPagination': 0,
        'pagesize': 100,
        'isNext': True,
        'isPrev': False,
        'searchString': "",
    }
    response = session.post(
        "https://api.bjs.com/digital/live/api/v1.0/member/activated/offers",
        headers=offer_header,
        data=json.dumps(offer_payload)
    )
    print(response)
    return json.loads(response.content)


def get_redeemed_offers_api(session):
    offer_header = {
        'content-type': 'application/json',
    }
    offer_payload = {
        'brand': "",
        'category': "",
        'indexForPagination': 0,
        'pagesize': 100,
        'isNext': True,
        'isPrev': False,
        'searchString': "",
    }
    response = session.post(
        "https://api.bjs.com/digital/live/api/v1.0/member/redeemed/offers",
        headers=offer_header,
        data=json.dumps(offer_payload)
    )
    print(response)
    return json.loads(response.content)


def clip_coupon(session, offer_id):
    params = {
        "offerId": offer_id
    }
    response = session.get("https://api.bjs.com/digital/live/api/v1.0/store/10201/coupons/activate", params=params)
    print(response)
    return json.loads(response.content)


def main():
    credentials = {
        "un": "",  # user username
        "pw": ""  # user password
    }
    session, member_info = log_in_api(credentials["un"], credentials["pw"])
    avail_offers = get_avail_offers_api(session)
    print(avail_offers[0]["currentCount"])
    for offer in avail_offers[0]["availableOffers"]:
        print(offer["offerId"])
        clip_result = clip_coupon(session, offer["offerId"])
        print(clip_result)
        time.sleep(2)
    # redeemed_offers = get_redeemed_offers_api(session)
    # print(redeemed_offers["offer"]["currentCount"])
    # clipped_offers = get_clipped_offers_api(session)
    # print(clipped_offers["currentCount"])
    return


if __name__ == "__main__":
    main()
