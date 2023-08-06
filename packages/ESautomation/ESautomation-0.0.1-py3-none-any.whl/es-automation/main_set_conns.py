import os
import ssl
import json
import string
import random
from datetime import date
import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
from mlaas_tools2.feature_tool import FeatureBase
from MailSender import send_mail_mixin

class kibana_conn(FeatureBase):
    """
    Kibana basic funciton class
    """
    def __inti__(self):
        super().__init__()
        BASEDIR = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(BASEDIR)

    def get_kibana_environ(self):
        kibana_url = ""
        env = os.environ['MLAAS_ENV']
        if env == "aicloud":
            kibana_url = "http://kibana-v8.esunaicloud.com/"
        elif env == "swlab":
            kibana_url = "https://ifefkt.swlab.esunbank.com.tw/"
        elif env == "uat":
            kibana_url = "https://ifefku.testesunbank.com.tw/"
        elif env == "production":
            kibana_url = "https://ifefkp.testesunbank.com.tw/"
        return kibana_url

    def call_kibana_api(self, path, method, data):
        URL = self.get_kibana_environ()
        headers = {"kbn-xsrf": "true", "Content-Type":"application/json"}
        acct = os.getenv('ES_ACCT')
        pwd = os.getenv('ES_PWD')
        if method == 'get':
            kibana_response = requests.get(url=URL+path, headers=headers, auth=(acct, pwd), data=data)
        elif method == 'post':
            kibana_response = requests.post(url=URL+path, headers=headers, auth=(acct, pwd), data=data)
        elif method == 'put':
            kibana_response = requests.put(url=URL+path, headers=headers, auth=(acct, pwd), data=data)
        else:
            raise ValueError("Request method error.")
        print(URL+path)
        print(kibana_response)
        self.logger.info(kibana_response)

class ES_basic_conn(FeatureBase):
    """
    Elasticsearchbasic funtion class.
    """
    def __init__(self):
        super().__init__()
        BASEDIR = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(BASEDIR)
        self.es = self.get_es_login()
        self.dtime = date.today().strftime("%Y-%m-%d")

    def read_config(self, path):
        """ Get config information"""
        try:
            with open("es-configs/"+path) as conf:
                data = json.load(conf)
                return data
        except Exception as e:
            self.logger.error("Read configs error.", exc_info=True)
            raise e

    def get_environ(self):
        """ Get environment's URL """
        ip = ""
        env = os.environ['MLAAS_ENV']
        print(env)
        if env == "aicloud":
            ip = "http://elasticsearch-master.logging-v8.svc.cluster.local:9200"
        elif env == "swlab":
            ip = "https://ifefkt-es.swlab.esunbank.com.tw/"
        elif env == "uat":
            ip = "https://ifefku-es.testesunbank.com.tw"
        elif env == "production":
            ip = "https://ifefkp-es.testesunbank.com.tw"
        acct = os.getenv('ES_ACCT')
        pwd = os.getenv('ES_PWD')
        return ip, acct, pwd

    def get_es_login(self):
        """ Get different ES connection based on environments """
        ip, username, pwd = self.get_environ()
        if 'https' in ip:
            ssl_context = create_ssl_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            try:
                es_conn = Elasticsearch(
                    [ip], http_auth=(username, pwd), 
                    verify_certs=False, ssl_context=ssl_context, 
                    timeout=100, max_retries=5, retry_on_timeout=True)
                self.logger.info(f"Success connection, ip={ip}, username={username}")
                return es_conn
            except Exception as e:
                self.logger.error("Connection Error", exc_info=True)
                raise e
        else:
            try:
                es_conn = Elasticsearch([ip], http_auth=(username, pwd),
                                        timeout=100, max_retries=5, retry_on_timeout=True)
                self.logger.info(f"Success connection, ip={ip}, username={username}")
                return es_conn
            except Exception as e:
                self.logger.error("Connection Error", exc_info=True)
                raise e

    def show_es_info(self):
        """check es information"""
        return self.es.info()

class es_index_mixin(ES_basic_conn):
    """
    ES index command class.
    """
    def create_indices(self):
        """ Create the default index """
        try:
            self.es.indices.create(index=self.indexname)
            self.logger.info(f"Create index {self.indexname}")
        except Exception as e:
            raise e

    def search_indices(self):
        """ Check index existed or not """
        return bool(self.es.indices.exists(self.indexname))
    
    def cat_indices(self):
        """ Cat index detail """
        return self.es.cat.indices()

    def es_index_run(self):
        """ES index main run"""
        if not self.search_indices():
            self.create_indices()
        else:
            self.logger.info(f"Check: {self.indexname} exists")

class es_role_mixin(es_index_mixin, kibana_conn):
    """
    ES role command class.
    """
    def create_role(self):
        """
        Create role with kibana api if it's not existed
        """
        path = "api/security/role/" + self.rolename
        body_dict = {
            "metadata":{
                "version": self.project_dict['version']
            },
            "elasticsearch":{
                "indices": [
                    {
                        "names": [self.indexname],
                        "privileges": ["read", "view_index_metadata", "monitor"]
                    }
                ]
            },
            "kibana": [{
                "base": [],
                "feature":{
                    "discover": ["all"],
                    "visualize": ["all"],
                    "dashboard": ["all"],
                    "dev_tools": ["all"],
                    "indexPatterns": ["all"],
                    "timelion": ["all"]
                },
                "spaces": ["default"]
            }]
        }
        body = json.dumps(body_dict)
        self.call_kibana_api(path=path, method="put", data=body)
        self.logger.info(f"Create role: {self.rolename}")
        
    def update_role(self, rolename):
        """
        Update index to role with kibana api"""
        contain_indices_lst = self.get_contain_indices(rolename)
        contain_indices_lst.append(self.indexname)
        path = "api/security/role/" + self.rolename
        body_dict = {
            "metadata":{
                "version": self.project_dict['version']
            },
            "elasticsearch":{
                "indices": [
                    {
                        "names": contain_indices_lst,
                        "privileges": ["read", "view_index_metadata", "monitor"]
                    }
                ]
            },
            "kibana": [{
                "base": [],
                "feature":{
                    "discover": ["all"],
                    "visualize": ["all"],
                    "dashboard": ["all"],
                    "dev_tools": ["all"],
                    "indexPatterns": ["all"],
                    "timelion": ["all"]
                },
                "spaces": ["default"]
            }]
        }
        body = json.dumps(body_dict)
        self.call_kibana_api(path=path, method="put", data=body)
        self.logger.info(f"Update role: {rolename}")

    def get_contain_indices(self, rolename):
        """Get containing indices list to make sure updated index is in the role"""
        try:
            role_detail = self.cat_roles(rolename)
            contain_indices_lst = role_detail.get(rolename).get('indices')[0].get('names')
            return contain_indices_lst
        except:
            return []

    def search_roles(self):
        """Get current role list"""
        self.es.indices.refresh()
        return list(self.es.security.get_role().keys())

    def cat_roles(self, rolename):
        """List the role detail"""
        return self.es.security.get_role(rolename)

    def es_role_run(self):
        """ES role main run"""
        contain_indices_lst = self.get_contain_indices(self.rolename)
        if self.rolename not in self.search_roles():
            self.logger.info(f"Role {self.rolename} is not exist, so we create it.")
            self.create_role()
        elif (self.rolename in self.search_roles()) and (self.indexname not in contain_indices_lst):
            self.logger.info(f"Role {self.rolename} exists, but the index {self.indexname} is not in roles, so we create index and update role.")
            self.update_role(self.rolename)
        else:
            self.logger.info(f"Nice! Role {self.rolename} exists, and the index {self.indexname} is in roles")
        self.logger.info(f"Final role check, the current role deatils are \n{self.cat_roles(self.rolename)}\n")

class es_user_mixin(es_role_mixin, send_mail_mixin):
    """
    ES user command class
    """
    def create_user(self, ESB_acct: str, name: str):
        """Create certain user"""
        random_str = self.get_random_pwd()
        body={
            "password": random_str,
            "roles": [self.rolename],
            "full_name": name
        }
        self.send_email(ESB_acct)
        self.es.security.put_user(username=ESB_acct, body=body)
        self.logger.info(f"Create username: {ESB_acct} and body={body}")

    def update_user(self, ESB_acct):
        """ Update user's config """
        contain_roles_lst = self.get_contain_roles(ESB_acct)
        contain_roles_lst.append(self.rolename)
        body={
            "roles": contain_roles_lst
        }
        self.es.security.put_user(username=ESB_acct, body=body)
        self.logger.info(f"Create username: {ESB_acct} and body={body}")

    def search_users(self)->list:
        """Get current users'list"""
        self.es.indices.refresh()
        return list(self.es.security.get_user().keys())

    def cat_user(self, ESB_acct):
        """Get certain user's information"""
        return self.es.security.get_user(username=ESB_acct)

    def get_contain_roles(self, ESB_acct):
        """Get containing role list to make sure updated role is in the role"""
        try:
            user_detail = self.cat_user(ESB_acct)
            contain_roles_lst = user_detail.get(ESB_acct).get("roles")
            return contain_roles_lst
        except Exception:
            return []
    def get_random_pwd(self):
        """Get random password"""
        letters = string.ascii_letters
        random_letters = ''.join(random.choice(letters) for i in range(26))
        return random_letters

    def send_email(self, acct: str):
        """send an initial mail, notifying users to change their password"""
        self.send_mail(acct=acct)

    def es_user_run(self):
        """ES user main run"""
        for ESB_acct, name in self.username.items():
            if ESB_acct not in self.search_users():
                self.logger.info(f"User {ESB_acct} is not exist, so we create it.")
                self.create_user(ESB_acct, name)
            elif (ESB_acct in self.search_users()) and (self.rolename not in self.get_contain_roles(ESB_acct)):
                self.logger.info(f"User {ESB_acct} exists, but role {self.rolename} is not, so we create role.")
                self.update_user(ESB_acct)
            else:
                self.logger.info(f"Nice! User {ESB_acct} exists, and the role {self.rolename} exists too.")
        self.logger.info(f"Final User check, the current User list are \n{self.search_users()}\n")
