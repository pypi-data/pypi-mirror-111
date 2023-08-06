import json
import os
import pandas as pd
import requests
import zipfile

class EasieUsertb():
    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except:
            return None

    def __init__(self, username, developer_key, url_api="https://api.easiedata.com", workspace_abs_path=None):
        self.url_api = url_api
        self.username = username
        self.developer_key = developer_key

        if workspace_abs_path is None:
            workspace_abs_path = os.getcwd()

        self.path = workspace_abs_path + '/'
        self.headers = {
            'Authorization': json.dumps({
                'username': self.username,
                'developer_key':self.developer_key
            })
        }

        return None

    def post_easieusertb(
        self, action, table_name, params={}, df=None):

        files = None
        if df is not None:
            timedelta_cols = [col for col in df.columns if df[col].dtype == 'timedelta64[ns]']
            df[timedelta_cols] = df[timedelta_cols].astype(str)

            file_name = table_name + 'temp'
            zip_name = file_name + '.zip'
            file_name += '.json'

            filepath = self.path + file_name
            zip_path = self.path + zip_name

            df.to_json(filepath, orient='table')

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(os.path.join(self.path, file_name), file_name)

            with open(zip_path, 'rb') as f:
                files = {'data': ('df', f, 'application/json')}

                r = requests.post(
                    self.url_api + '/developer/easie_usertb',
                    headers=self.headers,
                    data={'action':action, 'front_tablename': table_name, 'params':json.dumps(params)},
                    files=files
                )
        else:
            r = requests.post(
                self.url_api + '/developer/easie_usertb',
                headers=self.headers,
                data={'action':action, 'front_tablename': table_name, 'params':json.dumps(params)},
                files=files
            )

        if df is not None:
            try:
                os.remove(zip_path)
                os.remove(filepath)
            except Exception as e:
                print('Created files couldn\'t be removed')
                print(e)
            
        self.res = r.json()
        self.http_status = r.status_code

        return self

    def get_easieusertb(self, table_name):
        r = requests.get(
            self.url_api + '/developer/easie_usertb_get',
            headers=self.headers,
            data={'action':'get_df', 'front_tablename': table_name}
        )

        self.http_status = r.status_code

        if self.http_status == 200:
            zip_path = self.path + 'temp_zip.zip'
            zip_file = r.content

            with open(zip_path, 'wb') as z:
                z.write(zip_file)

            with zipfile.ZipFile(zip_path, 'r') as zf:
                name_list = zf.namelist()
                zf.extractall(self.path)

            filepath = self.path + name_list[0]
            with open(filepath, 'rb') as f:
                self.df = pd.read_json(f, orient='table')
                self.res = {
                    'success': True,
                    'front_msg': 'Success!'
                }
            try:
                os.remove(zip_path)
                os.remove(filepath)
            except Exception as e:
                print('Created files couldn\'t be removed')
                print(e)
            

        else:
            if isinstance(r.json(), dict):
                self.res = r.json()
            else:
                self.res = {
                    'success': True,
                    'front_error': True,
                    'front_msg': 'Erro ao enviar o df, consulte o suporte'
                }

        return self
