import os
import oci
import json
from tinydb import Storage

"""
OCIStorage is custom Storage for TinyDB to allow 
store JSON DB files in OCI Object Storage service.
Allows creation of TinyDB instance as follows:
db = TinyDB(oci_config = OCI_CONFIG,
            namespace = OCI_NAMESPACE,
            bucket = OCI_IQT_BUCKET,
            file = OCI_JOBS_DB_FILE,
            storage = OCIStorage)
"""
class OCIStorage(Storage):
    def __init__(self, oci_config, namespace, bucket, file):
        oci_config = json.loads(oci_config)
        self.client = oci.object_storage.ObjectStorageClient(oci_config)
        self.namespace = namespace
        self.bucket = bucket
        self.file = file

    def read(self):
        try:
            obj = self.client.get_object(self.namespace, self.bucket, self.file)
            data = obj.data.raw.data
            return json.loads(data)
        except oci.exceptions.ServiceError as error:
            if error.status == 404:
                self.write({})
            return json.loads('{}')

    def write(self, data):
        self.client.put_object(self.namespace, self.bucket, self.file, json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))

    def close(self):
        pass
