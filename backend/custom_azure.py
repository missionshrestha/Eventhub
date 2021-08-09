from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'eventhubkustorage' # Must be replaced by your <storage_account_name>
    account_key = 'Zf8bQc9jHikf73ELHsjlepTBMdwa16AN1ULvkRy5HwjTa0XPu5kgSjalnfsXmemazs0nQjqwY6ILSSf3Nl4bvQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'eventhubkustorage' # Must be replaced by your storage_account_name
    account_key = 'fbdeyqP6hu10lribv4QjybXXf3PJPkjLKIBy4cmSNurf3pwP5mMbUh+BwhbHVR+/3x6BvL8Smbtk5r58OuQSIQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None