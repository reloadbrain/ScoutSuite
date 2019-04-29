from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.base.resources.base import Resources


class Keys(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, service_account_email: str):
        super(Keys, self).__init__(facade)
        self.project_id = project_id
        self.service_account_email = service_account_email 

    async def fetch_all(self):
        raw_keys = await self.facade.iam.get_keys(self.project_id, self.service_account_email)
        for raw_key in raw_keys:
            key_id, key = self._parse_key(raw_key)
            self[key_id] = key

    def _parse_key(self, raw_key):
        key_dict = {}
        # The name of the key has the following format:
        # projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}/keys/{key}
        # https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.keys
        key_dict['id'] = raw_key['name'].split('/')[-1]
        key_dict['valid_after'] = raw_key['validAfterTime']
        key_dict['valid_before'] = raw_key['validBeforeTime']
        key_dict['key_algorithm'] = raw_key['keyAlgorithm']
        return key_dict['id'], key_dict
