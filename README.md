poetry init



How to run the local server
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```


Add OmiPay
omipay = {git = "git@github.com:sm-omi/omi-pay.git", rev = "dev"}


If you have directly added dependency in pyproject.toml, you must run
```bash
poetry lock
```
before
```bash
poetry install
```
as this may retrun an error "pyproject.toml changed significantly since poetry.lock was last generated. Run `poetry lock [--no-update]` to fix the lock file."


Valid GCash Notification Payload
```json
{
  "request":{
    "head":{
      "function":"gcash.acquiring.order.finish.notify",
      "clientId":"2022090516090600028604",
      "version":"2.0",
      "reqTime":"2024-11-14T17:21:01+08:00",
      "reqMsgId":"191535a9-6e79-424d-98b9-68e3acd947d3"
    },
    "body":{
      "acquirementId":"20241114121212800110170645602097464",
      "orderAmount":{
          "currency":"PHP",
          "value":"9800"
      },
      "merchantId":"217020000648235345532",
      "merchantTransId":"FB_SMOA_KVMZQ0DAZ1YJ",
      "finishedTime":"2024-11-14T17:21:01+08:00",
      "createdTime":"2024-11-14T17:18:53+08:00",
      "acquirementStatus":"SUCCESS",
      "extendInfo":"{}",
      "transactionId":"605057154"
    }
  },
  "signature":"PBWBv0lXw6DKmGGmhW1iFfGkvxXfe5ZVeDriTBCT/OuSR+OSFkiLWLklugxhrCSKt5ryiZ+28WVjsezKTO1cnVFVf2xjCktViIJ7GILo9kZcduafSgFhR1Fd8XswR23Jkom889Uu7eDpgdl+UThD+nYKdT+920Qp9heFYaHQNPmXHajUNiiQWwzujP6e5qGdUsGd/vRGejBobra+15BkBNm9A/qIN3857l+KJk02zkUq7CkVeL3X17+2gQzPnVwQ2a5hHP52sFN3pCe5MzQS0dbxxju0HdIgfPA21VjysjPe/dzXn+/uI0B6wvvwJq5yTw4GRhMLvCad4htg66Uqdw=="
}
```