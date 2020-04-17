

## Documentation

https://cloud.google.com/translate/docs/basic/translating-text#translate_text_with_model-drest


## Sample translation

IMPORTANT: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials-...eed.json"`

```
curl -X POST \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
-H "Content-Type: application/json; charset=utf-8" \
-d @de-request.json \
https://translation.googleapis.com/language/translate/v2
```

## Sample code

```
"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
from google.cloud import translate_v2 as translate
translate_client = translate.Client()

if isinstance(text, six.binary_type):
    text = text.decode('utf-8')

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
result = translate_client.translate(
    text, target_language=target)

print(u'Text: {}'.format(result['input']))
print(u'Translation: {}'.format(result['translatedText']))
print(u'Detected source language: {}'.format(
    result['detectedSourceLanguage']))
```

Source: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/translate/cloud-client/snippets.py


## Quota 

https://console.developers.google.com/iam-admin/quotas?project=civictechhub&service=translate.googleapis.com

Cloud Translation API
* General model characters per 100 seconds: Limit 1,000,000
* General model characters per day: Limit 1,000,000,000


## Pricing

https://cloud.google.com/translate/pricing
