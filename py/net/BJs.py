import time
import json

import requests


def log_in(username, password) -> [requests.Session, dict]:
    session = requests.Session()
    login_headers = {
        'content-type': 'application/json'
    }
    login_payload = {
        "deviceProfile": "ewogICJjb21wb25lbnRzIjogWwogICAgewogICAgICAia2V5IjogIndlYmdsIiwKICAgICAgInZhbHVlIjogWwogICAgI"
                         "CAgICJkYXRhOmltYWdlL3BuZztiYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQVN3QUFBQ1dDQVlBQUFCa1c3WF"
                         "NBQUFBQVhOU1IwSUFyczRjNlFBQUVSNUpSRUZVZUY3dG5WMklaRWNWeDAvMUlIa0lJbmtJb2lGZ3dCQlVvdmlKZ3JLOUN"
                         "vb29xS0NnS0tpb1lFQUY5VUhCeVBaRlVRajRBUW9LaW9MaUJ5Z29lUWpvZzlOQlFWR1MwZDJGV1RJaHU4bkdYVTJFMWF4"
                         "bTFZMTdwYnJ2elBSMDMrNWJWYmRPMVRsMS8vdTJVQi9uL00rcFg1K3F1WFd2SWZ6THBvQWhvbnJUN0owTnNwbU9pV2NLS"
                         "UVDcEU4RXF6djhQY2VYWEdPc25qY2FZSlN1bTB3QUxRWVlDVU1CTEFWMi84ZW1zMVF1c2RCcDVKUm9hUXdFb3dLY0FLN0"
                         "RBRkw3QVlXUW80S3RBQ2V1UkZWaStncGJYdm9RVUtTOHE4RWl2QW1LQmhhV3VONmxnZVJrS1NGeURZb0ZWUnNqaEJSU0F"
                         "BakVWVUFjc2lkU1BHUkNNQlFXZ3dIb0YxQUVyZlRDQnlQU2FDNXlST3cyNHh4Y29hWWhKcW9HRkdJZUVISDA0RlVCT2Nx"
                         "bzd2MXVBZjRJVndBSVFIQnlZbGx3QlVjQ0tzamlqREpJOER0RW1ITGo3ampwQ0pVZWh4RFVUQlN4eDZzQWdLRkMwQXZyQ"
                         "URXQVZuWkJ3TG84QytrQVFwRk1HTnpNQ0s0TzNRVkZCSnlqQXJRRFdncXZDR1lIbGFpTGFRWUVlQ29BRlBjUTc3TW9ubz"
                         "kvSUFGYVVjR0tRVGdWYzh0S2xUZWRFYUZDU0Fzc3AwUjlZU0xLUzhnTytRQUhSQ3ZRSFZyQjdJSjJYZEpETFN5NDBMbE9"
                         "Cak1EU0lpaEk0UnVwdXFZeEVZMk5vWWx2WDdTSEFwc1VLQXhZZ0l0THVuT3IxQUJybTRpT0cwTlRGNXZRQmdxNEtCQVJX"
                         "TnpMd01VZHRKR2d3TFdhcG9ib21MWEZHRnova2hDVFVteUlDS3hTSklFZmZSVllCQllSVmRnYTlsVlVYMyt1OGdYQTJwQ"
                         "UxYS0w3cDU4Y1MxeHN2MVpUdlpSWWdKYUxjR3ZhNklwK0QwY2R1Z0pZRGlJNU5VRld6V1M2V3RONGkyaTdKYkVBTGFkRV"
                         "FxTUJIYnJuRGJZV1puSGFlYldtNlJiUnNUVy9oRGlFejV1aTZtZEhoYVUraExJYzZBQlcyWWZ3bkw4RXNzS2N6Um9BSzV"
                         "uMGFiSTV6U3pyUlh1cXBucGsvenE0dnNtOXhzeWUwOEkvS09DdEFJRGxMUms2ckZQQW5sOFpvdTA1c0RhaXMvczhLemQ1"
                         "RVdhUkNnQllJc09pMHlpN0hiVFBYM1ZVV1B2T2RVTkxwd3h5ckM0UStnQ1dTM29WR0hnWHQzM2JlQUxMRG85RGVGK1JCO"
                         "TQrT3JDd3RvZWJVVmViNTY4Y0s2eVpVSGdTWGtxKzZGaTUwWUVsUlg3WWtWWUJlMzVGemZOWDdzQ2FMUkljd3FjTkZmOX"
                         "NqT3dMQmhhalRmeUNZb2JvQ3Z4Nzl2eVZPV2FvSm5kZ0haaUI4NnpvRVNsendHQmdsU2xIUHErMC93RE1nVFYvWURRQVd"
                         "GWjRRQ3RmK3NtWnVXTWhDQUdXOXVVcUo5NjVMUG5Qd3ZOWGdjQUN0SElGVDlHOFFvQ2xTREdZdXFMQWxackdvNFBucjRJ"
                         "ckxCekNJN2M2RlFDd09pVksyVUJucFhtbHBzbUk2TVIrWmRXandySmk0eEJlWnhva1dTaUtnSVVvZG1aRUpvbXUxRFFkT"
                         "FR3dzJoTlkyQnAyQmxweUE5NGs5QUlXcnlteGc4QmhMY2VZc2YxT1A5NlZhMVNQek9GV01BeFlLOXJpRUQ1OUtNWFA2QV"
                         "dzTUcrd3lNTjBFOWlySlpUMi9NbytmMlVoRldsTHVPZzRvQ1V3RGJ4TWlyejhFd0RMeXowMFBsQWdjcVNabFAzWHd2a1Z"
                         "BN0NzMWJpK3d4UzdmTU9HNXphQWxTOXFSMllPRDJGZUI1NWN1UERNQkN3Y3d1Y05zYWpaQWF6RTRkQUtwblV5UGJsd2Z6"
                         "QWVzSENlbFRndDFVeTNBVmlsTFMxaE1TbEEzc3NMNzI5bk9zUENlWmF3dE0xdERpcXMzQkZRdkRHOFhOTmtpK2lFVGFJR"
                         "XdMSks0UkJlVkw2bU42WjRZS2t1WklRYmYzbnB3bk84TGVIR2hZQkQrUFNjRUROajhjQVNvM1NCaHZ4ejZmNWdJbURoRU"
                         "w3QVhISjFxUXhnQ2E5RVhJT2hxWjA5dnpwOGYzdXlMZUcrUk81YlErUkdjRnBKbEs0TVlDMkZKRXpvc0Y3QjJhQzhZMnB"
                         "nMWF0ZjRuR0hsbkt0WTVtZlBjTWpHRkFrc0dJRmVENU9CSlhqR2lSaXRDZGE3ZzhtMmhMaUw0Y2lNaUNQRVFCV0h0M1Z6"
                         "L3BFYzM2MUNLbW93R29wcWRhSWhrTjQ5ZG5rN2dDQTVhNFZXallLMk8xZzNYSi9NQ3F3UE5UR2h5dzh4RkxlRk1CU0hzQ"
                         "WM1a3NERnA3UHlwRUZlZVlzRDFnNGNtTFBwTDh2bkYreGJRblhlYkYrcTRoRGVQYkk1NTlBS2JCQXBaeXA4NDgxOXdjNX"
                         "Q0U09SMXE2b0lVMGRrL2pSaXVsd0hMM0V5M2pLbkNwZVg5NzIzVWNUbUI1ZUlGRGVBK3h0RFVGc0pKRnJJeWZVd1hBV3Z"
                         "pYWRCbWFKMHRSQlJNQldBcUNsTS9FMVFWL3FUbS9FbHhoV2Jsd2ZTZGYwckRPdkFGWStIVmlWVjdwNEpjMjNCOWMyUkk2"
                         "SGp3eFNhSHJQSXRKaE5LR1ZWRmhBWjB5MHM1dUIvZmYzNzZwd3RxU1lhNjF3aGxheURFNVFkdGtDUk93d3NJZjFrdUgwQ"
                         "1ZZNlFxc3NLL21zQ21FUTNnMmFkTVB6QVNzOUk2b20xRWhuZjgyZS84VkhWdjM3SldRdnhLdXBBS2VoRmUzT3RZYW5CRl"
                         "lDbGRzT1hFUDhpUW5zSG9laCtFUVBpamk4anBsQkJhZkdFQmhmRzBmYjU2L1duNFZjdkluM2NOZGN6N1BDcDhpdENjeTF"
                         "sVzVJb0hsNmp6YXVTc3dBMVpOMjh0ZmVJNEhyQ1NMVmpDMDNHTXg1SllSZ1pVazRRWVhLeW1xUHU1d2YxRHFHZFpTMGdC"
                         "YWlsZFJSR0FwVmlHNTZWSXc1TzU0UWNCYWVCTGUzWCswektCQXl6SUJzQUxpY0tDalB1NEVlRXRrdDRQN3oxOHBQc05hO"
                         "UIySDhFR1prTDlUd2NBYUNFMFM1RkNCd0xLcStXME5rVTRKTXExN2ltVEFRcnk3ZzdIZm9sT3J6Z2J1YzdtMGZLeW1xV2"
                         "1ldnlxa3d0cDMydzlhTG1LcGFwTTRrU0pva3d4WUVXeFZPNFMrdERncWRjSEE4cSswMUdaaEdZWTdBa3Y3a2lzaldNbTh"
                         "XQXIzWTBzdjdPTjUwajFyanVINlRyTGs2amVSSTdENlRTSzNkOVpGSWxlV0Jjc3UxalRlSXRxMlN1MXZCM21BbFZVT1pZ"
                         "Znd3OG5iWlU4N2dTVlptbVMySlpzbzY2SnRuZnppVXpUZE1uU3NjR0ROdDRaYk5KRVhnYklzYWwxS0h1dXJFMWhseVFWd"
                         "mZCVzQrTi81aGVjQkFJdW9wc3BjQjJqNTVnaFArM2FLdFFMTEEzZzh0bUpVTVFyODVVbXFsN2VBOGJhRUFqUE5RdXQ2UU"
                         "1zcEFUT0VEeFdXVTJTRzJlamlaUnFiNW9PcGc2aXdEc044M0R5ZHBzT011bXl2QWF3TXZ4S3lVK0xRdWd1WGFEb3lxKys"
                         "vaWxkaENWV2lwbnZORGJPbisvRlBtQUtzd1BKaWdWZGpZU29XYXM2Rnh3Y0tMQnRQdXpXOEVWdERhYW5OQ2l4cHpzSWVQ"
                         "d1V1L0hWK2ZzVjNodVZuejZ4MXp6ZjVlYzVZbVdjQ1dwNmFSV3J1Y2VnZWFjWjB3NkE2aTY3MXhZczBycS9SdGpoZ1JmZ"
                         "TBjOERLM0FSb2RhcVVxTUZTaFZYWXloZm96dHdrZ1lZdEpkeWpqOUIwdEhCL2NHQ0g3a2ZWTUhUYzNNeC9DTCthRmZMen"
                         "hKMVRjWHpCbHRCZDhZT1djYVFQbURoaGwwZlBBbGlMY3B0YlpyOHkrSmRaQVlGQkdBSU9Na2ZkWWZvLzcxRzlXRlZ0ckx"
                         "CcW91VlhKd3RNTEFldk56YXB6SzNZR3ZZVnNXLy9OSGtGQnZXTlU5TCs1M2RwUERKSDd3OE9la3U0cjc3OXkrSHpBSzJr"
                         "eWJnMFdScGc1ZlFRYzNzcmNQNFVUVWFHVGpoWFdBc1hvL2Y3Rkp0WUZscTNBMXJlU1JXcGcyTmUrWlpJdnUwamVkTU1rM"
                         "2YydUw3a0dPMzhuK2JuVjZVQUsvcVRFQ002Ym03blA0VFBFWHZwY3pvQ1M3b2JzQyttQXVmdlg3MC9tSFZMS1BBWHlMd0"
                         "VoL0F4Yzg1MXJHRUNTK0FDY0EwWWQ3dnpmNkF4MmU4UEVzMVdKSjdEV3F2NHZlWVZ1TDdEblkvTDR3OFRXQ2xWVmdiSGg"
                         "zOUxreEhSQ1FETEtVa3E4eXFjWjgxLzJ1ekdtLzhmZ0JWTDQzUXhpMlZ4NnpqbmZqMS8vMVVXWUVVL2JHS1Zhbi93eXJ3"
                         "RzBFcWlkRlAxcDVvTDh5aFE0T0ZwKy8zQnJHZFkwbldyNmJnNW51c1F2cEJmU3NjWXE2aXdoaFVTeDhneE5EdTdUZVBSb"
                         "XZ1RHVZRTFMNzdFWmtKbFhvY3FLeXdsL1dLYUdGaCt4b1VKZ0Y2aENwejl4ZUg1VlpZdFlhamhlZnRWNWcydXNBckkvNE"
                         "F1ZWVYZ25UMHhzSGlkd2VqOUZEaDd6L3I3ZzdhNkdWSGQrbGZEdHI4bUZwOVk5Z0hTTjVsSnFzUG1mcEVWMkRzUXhNWG5"
                         "sY0JRaVRYcDNOM3Q5d2UzR29zTC9zeVhlMHdzcU43aVdsRzVEK3ZhTW5DZHV3NHZ2aDJBSlQ1RWFRdzgrN1A1Kzl2WFBY"
                         "dVYrd3dyalFvYlo2bk0yL0tCU29EL0lrd0FzRVNFSWI4UlozOUNZN1Bod3ZOZ2dXVXJxbmNBVkh3WjZsY3poZ0hMYnc0M"
                         "1h6bkdkSnNacllqb29SL04zOStPQ3F0SkJ3dXFkd0ZVMGhaSEdMQ2tlZUZpRDRDNFVhV0hmckQ1L3VDQUtxekt2THNGVk"
                         "FQUEh5bnVEd2RZTGxBYmFKdTk3OU40cTNuK0txakNLdU1GZnBVTnYza3ZxaXJKeTJBRHNLUXdsVk0rN1Q3R3NYL3Z1elR"
                         "lNnJqd1hIU0ZaYmQvSHdDb09GZGFyTEdGVjFoeEZtUU1zYUpZRW1XUUdONGNIV1B2VzkzM0J3c0ZWbVUrQkZERnp5aStF"
                         "WmVBSlhSRjhmbnZPWElhZmRMTWN1ajZnOS9vdmo5WUdMQXFjNGNNVUtXT3RXZkNpMnZPV21FaEdPTGl2V0xRM3RmbWp6T"
                         "zB2ZmRxM1htVzJrL1YyNjNmUjJXQVNuNW15TFNRRDFqY3RPSWVYMmE4b2x1MTk1VUJBTXVDNnVOYVFJWEUzcFRrZk1DS3"
                         "ZyUUdQaUJUSGovd3BVMzNCOVcvY2JReW45UUNxb0hudDZQN3VvREZ0R2dkdFNxeTJRTjNIWjVmdVd6MVhMZU9XUlBMVmx"
                         "TZkFxaEtUTmlzZVNWUlVKbE01TEZxNzRzMHJwdkhHVnhCNU5vdUtMSDZ1bG5UL0ZtcXo4U0RWVitUSk9hNFpwdUM4aXFu"
                         "dzBpZ2VPcnZmWTdHTlIwZXVJZFZXUGJGTTZ1dm5ZbWRXQTV2VDY3TVorT0JLcDdLR0NtbUFtRjVCV3JFakVHMnNjNU1hR"
                         "HFxNSs5dmQ2MmNYTnVGSlphREZLc0RWMllDVURrb3A2TkpCMXZZOGtxSE9zTzI4c3lkUncvY0R5b3NRelNxUXo3emRWaH"
                         "RKVWlzeW53ZW9OcVl3UVVXRmdueWF0aFFrT3I5N3AwMEh2M3Y2UHV2d3JhRTdXQmpTeXhEbGZrQ1FDVTFyN2p0WXNzcmJ"
                         "zTXhmajhGZGordERGZ1dWSGZ4Z2FyQVltUWxRVGI3cUVNQkFHc3hyRHBpMW85VVRlL2RUOHkzZzlabDRXZFlsZmt5SDZn"
                         "OFYzVVU3VEZJdUFJQTFvRjJBNklWRWUxK1RDQ3dGclBSVmxSZnRhQWFWbHpDbDNJNVBUZEZQQUJZU0NEdHFiSDdFUnBUe"
                         "St0a1JKeGhtZVpacXE4bnJLcTBCelNYL1JsUXNBcXNERWJrMG51bzgrNSttTWJVUEg4bGJFdFltVzhDVkVQTlN4ZS9BeW"
                         "9zbDJIUlJySUNwei9ZL3Y2cmpCVldaYjROVUczT21UU1ZSSnBad2xjSGdCV3VuZHFlcDk4dkJGajJuT283QUZYdVJKSU9"
                         "xZVcvaStYV0MvTW5WT0RVKythUE03UTlzYzVXWWJVOW5mNDlmT2doWWRqZHBsSkFMbFJZYnFFc3B0V3A5OUI0MUh4d1lo"
                         "bFFiTUE2Vks4eVAwUkZWVXd5WlhBRXdGb251b0pmbTVCOE9mWE9vL2NIa3h5NjI2M2Zqd0dxa0hpaHoxRUZBS3lCWmNTc"
                         "HR5Y0VsZ1hWVDlPQnF0RGZtSUZsYVBlZkhpRElnQlE0L1ZhcUY2c3FqZ3JMRUZXejdlWFAwOEdxYndnQnU3NEtwdW1QQ2"
                         "l1TnppSm1PZlZtR2hzNmV1RzVON0RNMGN2UFpLaDYydDBOcUFxZ1FBRXVpTWk5V0VaNEFVdEY4TElZbVdWUzd4dzQrY2J"
                         "WNnppOWdXVXJLWHNmMFZCMTNUMTZLaXB2OGRCQmhBSmV3Qkpoc2FjUk9sRGk2VlJnODVPdmp3OHN1LzI3L3BjQVZXQkkw"
                         "TTFUZ2VLQjVhbEgvdWFNaEQzNTJ2a0hKMktjWVJGUjlZeGZBVlJKRTRZeE45cjhTRHlkazVRQWxwTk0raHZ0akdtODFYT"
                         "GgyWHRMYUtpNllRcFE2YzhJblI0QVdEcmo1bTMxenF0cHV0Vzh2OTI1d3JLdlNtN2VsMlczZmpmK0JxRHlGajVuaCt3bF"
                         "Vud0RBS3ljQ1pWdzdwMVh0dDhmN0txd0xLaWU5VHRlVU1WUDY0VENZaXBXQlpaekE4QmlsVnZPNEg5OCtlRUhVNTBxck9"
                         "hOVZEZjluaGRXY2hRS3R3VEFEZGZPdHllQTVhdVl3dlk3TDZPeFdYUGh1YlhDTWxUZGZEOUF4UkpxMEcxVlZnOU41QURM"
                         "dzJpV1JDcDQwSjBYMHNRUW5YRDRwbUIxeTBtYTRLM0VCU2VEY3Rma0FFdTVrREhOajgzdW5lZlQxSkQ5WUtxaEVkVmtqa"
                         "DZtMi85WHQ1NUdSUlV6aGluR2lwMG5LV3p1T3dlQTFWZkJvUDVwVTIzbnRqWDNCdzFWdDUwQnFJSkNpRTVaRkFDd3NzbG"
                         "VKNWw1NTduejk3Y3ZIYlJYTDNnUW9Fb1NBRXdTVlFFQUs2cWM4Z2E3N3prMEdSR2RzSUcyanlpODZOeDZVS1d0KytScEJ"
                         "ZdmtLd0JneVk5Ukx3dnZ1NW1tSTBQVEZ6OVNlRVVGMmpybWlXNmgwZ0JyVVNQZGVxbjdydWQ5ejZiSlN5OFVEaXZIcFlw"
                         "bStoVklBeXo5T3NHRGdTcWcvZmUxdExBQldJNFJSZUk2Q29WbVVJQlJBUUNMVVZ3TXJWT0I0QituNEk0NmRXcTNtbGVFQ"
                         "UdEeEdsUlM2T0FMRklBQ2NSVUlBRlpjQXpBYUZJQUNmQXFVVmw0QVdIeTVncEdoQUJTSXJBQ0FGVmxRREFjRllpdFFXcF"
                         "hVUjUvL0ExNlJIY1I1VXpGSkFBQUFBRWxGVGtTdVFtQ0MiLAogICAgICAgICJleHRlbnNpb25zOkFOR0xFX2luc3RhbmN"
                         "lZF9hcnJheXM7RVhUX2JsZW5kX21pbm1heDtFWFRfY29sb3JfYnVmZmVyX2hhbGZfZmxvYXQ7RVhUX2Zsb2F0X2JsZW5k"
                         "O0VYVF9mcmFnX2RlcHRoO0VYVF9zaGFkZXJfdGV4dHVyZV9sb2Q7RVhUX3RleHR1cmVfY29tcHJlc3Npb25fYnB0YztFW"
                         "FRfdGV4dHVyZV9jb21wcmVzc2lvbl9yZ3RjO0VYVF90ZXh0dXJlX2ZpbHRlcl9hbmlzb3Ryb3BpYztFWFRfc1JHQjtPRV"
                         "NfZWxlbWVudF9pbmRleF91aW50O09FU19mYm9fcmVuZGVyX21pcG1hcDtPRVNfc3RhbmRhcmRfZGVyaXZhdGl2ZXM7T0V"
                         "TX3RleHR1cmVfZmxvYXQ7T0VTX3RleHR1cmVfZmxvYXRfbGluZWFyO09FU190ZXh0dXJlX2hhbGZfZmxvYXQ7T0VTX3Rl"
                         "eHR1cmVfaGFsZl9mbG9hdF9saW5lYXI7T0VTX3ZlcnRleF9hcnJheV9vYmplY3Q7V0VCR0xfY29sb3JfYnVmZmVyX2Zsb"
                         "2F0O1dFQkdMX2NvbXByZXNzZWRfdGV4dHVyZV9hc3RjO1dFQkdMX2NvbXByZXNzZWRfdGV4dHVyZV9ldGM7V0VCR0xfY2"
                         "9tcHJlc3NlZF90ZXh0dXJlX2V0YzE7V0VCR0xfY29tcHJlc3NlZF90ZXh0dXJlX3MzdGM7V0VCR0xfY29tcHJlc3NlZF9"
                         "0ZXh0dXJlX3MzdGNfc3JnYjtXRUJHTF9kZWJ1Z19yZW5kZXJlcl9pbmZvO1dFQkdMX2RlcHRoX3RleHR1cmU7V0VCR0xf"
                         "ZHJhd19idWZmZXJzO1dFQkdMX2xvc2VfY29udGV4dDtXRUJHTF9tdWx0aV9kcmF3IgogICAgICBdCiAgICB9CiAgXQp9",
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


def get_avail_offers(session) -> dict:
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
    return json.loads(response.content)


def get_clipped_offers(session) -> dict:
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


def get_redeemed_offers(session) -> dict:
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


def clip_coupon(session, offer_id) -> dict:
    params = {
        "offerId": offer_id
    }
    response = session.get("https://api.bjs.com/digital/live/api/v1.0/store/10201/coupons/activate", params=params)
    print(response)
    return json.loads(response.content)


def main():
    credentials = json.load(open("config.json", "r"))  # {"un": <username>, "pw": <password>}
    session, member_info = log_in(credentials["un"], credentials["pw"])
    avail_offers = get_avail_offers(session)
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
