from main_set_conns import ES_basic_conn, es_user_mixin

class es_get_input_data_mixin(ES_basic_conn):
    """
    Get project's configuration and variables.
    """
    def get_project_config(self, path:str)->dict:
        """
        Get user's configuration to setup ES privilege.
        Parameters:
        - path: project's configuration path
        """
        project_dict = self.read_config(path)
        self.validate_config(project_dict)
        return project_dict

    def validate_config(self, project_dict:dict):
        """
        Validate Project's config's format
        Parameters:
        - project_dict: input json file that needs to be validated.
        """
        if project_dict['owner'] not in ['da', 'de']:
            self.logger.error("Your owner colume is invalid")
            raise ValueError("Your owner colume is invalid")

    def get_indexname(self, project_index:str):
        """
        Set self.indexname
        Parameters:
        - project_index: target index_name in configuration
        """
        if self.project_dict['owner'] == 'da' and project_index == "default":
            self.indexname = "up0125_" + self.project_dict['proj_name'] + "_" + self.dtime
        elif self.project_dict['owner'] == 'da' and project_index != "default":
            self.indexname = "up0125_" + project_index + "_" + self.dtime
        elif self.project_dict['owner'] == 'de':
            self.indexname = "de_" + self.project_dict['proj_name'] + "_" + self.dtime
        else:
            self.logger.error("Invalid Project name.")
            raise ValueError("Invalid Project name, plz check your configuration.")

    def get_rolename(self):
        """
        Set self.rolename
        """
        self.rolename = self.project_dict['proj_name']+"_users"

    def get_username(self, project_members):
        """
        Set self.username
        """
        self.username = project_members

class main_mixin(es_user_mixin, es_get_input_data_mixin):
    def read_project_conf_run(self)->dict:
        """
        Read efk_setup.json
        """
        return self.get_project_config("efk_setup.json")

    def check_run(self):
        """
        Check target indices, roles and users are existed.
        """
        if not self.es.indices.exists(self.indexname):
            self.logger.error(f"Target index {self.indexname} is not in Elasticsearch.")
            raise ValueError("index mission failed")
        if self.rolename not in self.search_roles():
            self.logger.error(f"Target role {self.rolename} is not in Elasticsearch.")
            raise ValueError("role mission failed")
        for user in self.username:
            if user not in self.search_users():
                self.logger.error(f"Target user {self.username} is not in Elasticsearch.")
                raise ValueError("user mission failed")

    def main_run(self, project_dict):
        """
        Project's main run
        Deal with operation of create and update to indices, roles and users
        """
        self.logger.info("Main run starting!!!!!!!!")
        self.project_dict = project_dict
        for ele in self.project_dict.get('setting'):
            if isinstance(ele, dict):
                project_index = ele.get("index_name")
                project_members = ele.get("members")
                project_role = ele.get("role_name")
                if project_role == "default":
                    self.get_rolename()
                elif project_role != "default" and project_index == "default":
                    self.logger.error("Warn! You've already had a default rolename, your index_name should be default.")
                    raise ValueError("You don't need a special rolename, plz remove the colume from the configuration.")
                elif project_role != "default" and project_index != "default":
                    self.rolename = ele.get("role_name")

                self.get_indexname(project_index)
                self.get_username(project_members)
                self.es_index_run()
                self.es_role_run()
                self.es_user_run()
                self.check_run()
        self.logger.info("Main run end!!!!!!!!")
        return True
