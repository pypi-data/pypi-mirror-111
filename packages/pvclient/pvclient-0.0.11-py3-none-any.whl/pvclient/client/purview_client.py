from pyapacheatlas.core import PurviewClient, AtlasException
import requests
import time
import json
class ExtendedPurviewClient(PurviewClient):
    """
    Provides communication between your application and the Azure Purview
    service. Simplifies the requirements for knowing the endpoint url and
    requires only the Purview account name.

    :param str account_name:
        Your Purview account name.
    :param authentication:
        The method of authentication.
    :type authentication:
        :class:`~pyapacheatlas.auth.base.AtlasAuthBase`
    """

    def __init__(self, account_name, authentication=None):
        super().__init__(account_name, authentication)
    
    def delete_glossary_term(self, termguid):
        """
        Delete one or many termguid from your Apache Atlas server.

        :param termguid: The termguid you want to remove.
        :type guid: Union(str,list(str))
        :return:
            204 No Content OK. If glossary term delete was successful.
            404 Not Found
            If glossary term guid in invalid.
        :rtype: int
        """
        atlas_endpoint = self.endpoint_url + \
            "/glossary/term/{termguid}".format(termguid=termguid)
        delete_response = requests.delete(
            atlas_endpoint,
            headers=self.authentication.get_authentication_headers())

        try:
            delete_response.raise_for_status()
            return delete_response.status_code
        except requests.RequestException:
            if "errorCode" in delete_response:
                raise AtlasException(delete_response.text)
            else:
                raise requests.RequestException(delete_response.text)

    def delete_all_terms(self, termguids):
        """
        Delete one or many termguid from your Apache Atlas server.

        :param termguids: List of termguid you want to remove.
        :type termguids: Union(str,list(str))
        :return:
            204 No Content OK. If glossary term delete was successful.
            404 Not Found
            If glossary term guid in invalid.
        :rtype: int
        """
        for termguid in termguids:
            self.delete_glossary_term(termguid)
            time.sleep(3)

    def get_all_term_templates(self):
        atlas_endpoint = self.endpoint_url + "/types/typedefs"
        # TODO: Implement paging with offset and limit
        getResult = requests.get(
            atlas_endpoint,
            params={"type": "term_template"},
            headers=self.authentication.get_authentication_headers()
        )
        return self._handle_response(getResult)

    def import_term_templates(self, term_templates):
        atlas_endpoint = self.endpoint_url + "/types/typedefs"
        # TODO: Implement paging with offset and limit
        import json
        getResult = requests.post(
            atlas_endpoint,
            data=json.dumps(term_templates),
            headers=self.authentication.get_authentication_headers()
        )
        return self._handle_response(getResult)
    
    def delete_term_templates(self, term_templates):
        atlas_endpoint = self.endpoint_url + "/types/typedefs"
        # TODO: Implement paging with offset and limit
        import json
        delete_response = requests.delete(
            atlas_endpoint,
            data=json.dumps(term_templates),
            headers=self.authentication.get_authentication_headers()
        )
        try:
            delete_response.raise_for_status()
            return delete_response.status_code
        except requests.RequestException:
            if "errorCode" in delete_response:
                raise AtlasException(delete_response.text)
            else:
                raise requests.RequestException(delete_response.text)
    
    def create_glossary(self, name):
        atlas_endpoint = self.endpoint_url + "/glossary"
        import json
        res = requests.post(
            atlas_endpoint,
            data=json.dumps(
                {"qualifiedName": name, "name": name,
                "terms": []}),
            headers=self.authentication.get_authentication_headers()
        )
        return self._handle_response(res)
    
    def wait_for_operation(self, import_response):
        operation_id = import_response.get('id')
        if operation_id:
            status = 'INIT'
            results = None
            while(status in ['INIT', 'RUNNING']):
                import time
                time.sleep(3)
                atlas_endpoint = self.endpoint_url + \
                    f"/glossary/terms/import/{operation_id}"
                operation_response = requests.get(
                    atlas_endpoint,
                    headers=self.authentication.get_authentication_headers()
                )
                results = self._handle_response(operation_response)
                status = results.get('status')

            return results
                

    def import_terms(self, csv_path, glossary_name="Glossary", glossary_guid=None):
        """
        Bulk import terms from an existing csv file. If you are using the system
        default, you must include the following headers:
        Name,Definition,Status,Related Terms,Synonyms,Acronym,Experts,Stewards

        For custom term templates, additional attributes must include
        [Attribute][termTemplateName]attributeName as the header.

        :param str csv_path: Path to CSV that will be imported.
        :param str glossary_name:
            Name of the glossary. Defaults to 'Glossary'. Not used if
            glossary_guid is provided.
        :param str glossary_guid:
            Guid of the glossary, optional if glossary_name is provided.
            Otherwise, this parameter takes priority over glossary_name.

        :return:
            A dict that contains an `id` that you can use in
            `import_terms_status` to get the status of the import operation.
        :rtype: dict
        """
        results = None
        if glossary_guid:
            atlas_endpoint = self.endpoint_url + \
                f"/glossary/{glossary_guid}/terms/import"
        elif glossary_name:
            atlas_endpoint = self.endpoint_url + \
                f"/glossary/name/{glossary_name}/terms/import"
        else:
            raise ValueError(
                "Either glossary_name or glossary_guid must be defined.")

        headers = self.authentication.get_authentication_headers()
        # Pop the default of application/json so that request can fill in the
        # multipart/form-data; boundary=xxxx that is automatically generated
        # when using the files argument.
        headers.pop("Content-Type")

        postResp = requests.post(
            atlas_endpoint,
            params={"includeTermHierarchy": "True"},
            files={'file': ("file", open(csv_path, 'rb'))},
            headers=headers
        )

        import_response = self._handle_response(postResp)
        return self.wait_for_operation(import_response)