# djangoldp-webpushnotification

Enable [Web Push](https://developers.google.com/web/fundamentals/push-notifications) notifications for DjangoLDP.

## Install

```bash
$ python -m pip install djangoldp_webpushnotification
```

Then add the app to your `settings.yml` like so:

```yaml
ldppackages:
  - djangoldp_webpushnotification
```

## Management commands

- `gen_vapid_key`: Generate VAPID key pair

- `show_vapid_key`: Show VAPID public key

- `delete_subscriptions`: Clears existing subscriptions

## Test

```bash
$ python -m unittest djangoldp_webpushnotification.tests.runner
```
