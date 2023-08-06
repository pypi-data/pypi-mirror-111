"""
Delete operation for efk team.
"""
from main_set_conns import es_user_mixin, es_role_mixin

class es_get_input_data_mixin(es_user_mixin):
    """
    Get efk team's configuration and variables.
    """
    def get_efkteam_file(self, path: str)->dict:
        """
        Get EFK team's configs and validation.
        Paramrs:
        Return:
        - maintain_dict: (dict) efk team's configuration
        """
        maintain_dict = self.read_config(path)
        self.validate_config(maintain_dict)
        return maintain_dict

    def validate_config(self, maintain_dict: dict):
        """
        Validate EFK team's config's format
        Params:
        - maintain_dict: (dict) input json file that needs to be validated.
        """
        if maintain_dict.get('platform') != "EFK":
            self.logger.error("Check maintain_dict, it might be wrong path or wrong user_tag ")
            self.logger.info(f"maintain_dict: {maintain_dict}")
            raise ValueError("plz check ur mapping of user_tag and config files")

class es_delete_role_mixin(es_role_mixin):
    """
    ES delete role command class.
    """
    def delrole_run(self):
        """ 
        ES delete role main run 
        """
        del_roles = self.maintain_dict['del_role']
        if len(del_roles) > 0:
            for rolename in del_roles:
                try:
                    self.delete_role(rolename)
                except Exception:
                    self.logger.error("The role was not existed", exc_info=True)
        else:
            self.logger.info("There is no role to ba deleted.")

    def delete_role(self, rolename):
        """ 
        Delete role
        """
        self.es.security.delete_role(rolename)
        self.logger.info(f"Role {rolename} was deleted.")

class es_delete_user_mixin(es_user_mixin):
    """
    ES delete user command class.
    """
    def deluser_run(self, deltag):
        """
        Delete user's operation, there are 2 situations: initiate or efk-team's work.(optional)
        Params:
        - deltag: if it is efk-team's work to delete specific users, then deltag='certain', if you want to kill all ESB users, then deltag='all'
        """
        self.validate_inputparams(deltag)
        if deltag == "all":
            self.delete_all_ESB_users()
        elif deltag == "certain":
            self.delete_certain_ESB_users()

    def validate_inputparams(self, deltag):
        """
        Validate input params
        params:
        - deltag: tag that decides delete all users or delete certain user 
        """
        if deltag not in ["all", "certain"]:
            self.logger.error("InputError: deltag is invalid")
            raise ValueError("InputError: deltag is invalid")

    def delete_all_ESB_users(self):
        """ 
        Delete all ESB users
        """
        delete_namelst = self.get_all_delete_namelst()
        if len(delete_namelst) == 0:
            self.logger.info("No one to be deleted")
        elif len(delete_namelst) > 0:
            self.logger.info(f"Someone was deleted, deleted list: "+''.join(x for x in delete_namelst))
            for item in delete_namelst:
                self.es.security.delete_user(item)

    def delete_certain_ESB_users(self):
        """
        Delete specific ESB users
        """
        efk_del_namelist = self.maintain_dict['del_user']
        for item in efk_del_namelist:
            try:
                self.logger.info(f"User {item} was deleted.")
                self.es.security.delete_user(item)
            except Exception as e:
                self.logger.error("User is not found in ES Users.", exc_info=True)
                raise e

    def get_all_delete_namelst(self):
        """
        Get the namelist that needs to delete
        """
        delete_namelst = []
        for currentuser in self.search_users():
            if "ESB" in currentuser or "esb" in currentuser:
                delete_namelst.append(currentuser)
            self.logger.info(f"Here is list that is going to be deleted, {delete_namelst}")
            return delete_namelst


class main_mixin(es_get_input_data_mixin, es_delete_user_mixin, es_delete_role_mixin):
    def read_config_run(self)->dict:
        """
        Read efk_team.json
        """
        return self.get_efkteam_file("efk_team.json")

    def main_run(self, maintain_dict, deltag):
        """
        EFK team's main run.
        Only delete operation, if you want to add system account, u need to setup manually.
        """
        self.maintain_dict = maintain_dict
        if deltag is not None:
            self.deluser_run(deltag)
        else:
            self.logger.info("We don't do any deleting things.")
            return True
        self.delrole_run()
        return True
